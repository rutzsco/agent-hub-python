import os
import logging
import base64
from typing import Optional, AsyncGenerator, List, Dict, Any, Union
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
import openai
from openai import AzureOpenAI

from ..models.api_models import ChatThreadRequest, ImageFile


class ImageAnalysisAgent:
    """Agent for analyzing images and extracting serial numbers from equipment labels"""

    def __init__(self):
        load_dotenv()

        self.logger = logging.getLogger(__name__)

        # Azure OpenAI configuration
        self.azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
        self.chat_deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-4o")

        # Azure Blob Storage configuration (optional)
        blob_connection_string = os.getenv("AZURE_BLOB_CONNECTION_STRING")
        self.blob_container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME", "images")
        self.blob_service_client = None
        if blob_connection_string:
            self.blob_service_client = BlobServiceClient.from_connection_string(
                blob_connection_string
            )

        # Initialize Azure OpenAI client
        if not self.azure_openai_endpoint or not self.azure_openai_api_key:
            raise ValueError(
                "Azure OpenAI endpoint and API key must be configured")

        self.client = AzureOpenAI(
            azure_endpoint=self.azure_openai_endpoint,
            api_key=self.azure_openai_api_key,
            api_version=self.azure_openai_api_version
        )

    def _get_system_prompt(self) -> str:
        """Get the system prompt for image analysis"""
        return """You are an expert image analysis agent specialized in extracting serial numbers from equipment labels and plates.

Your primary task is to:
1. Analyze images of equipment, machinery, or devices
2. Identify and extract serial numbers, model numbers, and part numbers from labels, nameplates, or stickers
3. Provide accurate transcription of alphanumeric codes
4. Note the location and context of the identified numbers

When analyzing images:
- Look for metallic plates, adhesive labels, engraved text, or printed information
- Pay attention to common label formats (barcode labels, QR codes with text, manufacturer plates)
- Extract all visible serial numbers, model numbers, part numbers, and asset tags
- If text is partially obscured or unclear, indicate uncertainty
- Provide the extracted information in a structured format

Response format:
- Serial Number: [extracted number]
- Model Number: [if visible]
- Part Number: [if visible]
- Manufacturer: [if visible]
- Additional Notes: [any relevant observations]

If no serial numbers are visible or the image quality is insufficient, clearly state this limitation."""

    async def _process_image_file(self, image_file: ImageFile) -> Optional[tuple[bytes, str]]:
        """Process an image file and return image data and media type"""
        try:
            image_data = None
            media_type = None

            # Handle data URL
            if image_file.data_url:
                if image_file.data_url.startswith("data:"):
                    data_parts = image_file.data_url.split(',')
                    if len(data_parts) == 2:
                        # e.g., "data:image/jpeg;base64"
                        header_part = data_parts[0]
                        base64_data = data_parts[1]

                        # Extract media type
                        media_type = header_part.split(
                            ';')[0].replace("data:", "")

                        # Convert base64 to bytes
                        image_bytes = base64.b64decode(base64_data)
                        image_data = image_bytes

                        self.logger.info(
                            f"Processed data URL for image {image_file.name} ({media_type}, {len(image_bytes)} bytes)"
                        )

            # Handle blob name
            elif image_file.blob_name:
                if not self.blob_service_client:
                    self.logger.warning(
                        f"Blob storage service not configured, skipping blob {image_file.blob_name} for file {image_file.name}"
                    )
                    return None

                # Check if blob exists and download
                try:
                    blob_client = self.blob_service_client.get_blob_client(
                        container=self.blob_container_name,
                        blob=image_file.blob_name
                    )

                    # Download blob content
                    blob_data = blob_client.download_blob()
                    image_data = blob_data.readall()

                    # Get content type from blob properties
                    blob_properties = blob_client.get_blob_properties()
                    media_type = blob_properties.content_settings.content_type or "image/jpeg"

                    self.logger.info(
                        f"Downloaded blob {image_file.blob_name} for image {image_file.name} ({media_type}, {len(image_data)} bytes)"
                    )
                except Exception as blob_ex:
                    self.logger.warning(
                        f"Failed to download blob {image_file.blob_name}: {blob_ex}"
                    )
                    return None

            else:
                self.logger.warning(
                    f"File {image_file.name} has neither data_url nor blob_name specified"
                )
                return None

            if image_data and media_type:
                return image_data, media_type

        except Exception as ex:
            self.logger.warning(
                f"Failed to process image file {image_file.name}: {ex}")

        return None

    async def analyze_images(self, request: ChatThreadRequest) -> AsyncGenerator[str, None]:
        """Analyze images for serial number extraction"""

        if not request.files:
            yield "No images provided for analysis."
            return

        # Build messages for the chat completion
        messages = [
            {
                "role": "system",
                "content": self._get_system_prompt()
            }
        ]

        # Build user message content
        user_content = [
            {
                "type": "text",
                "text": request.message or "Please analyze the provided images and extract any serial numbers, model numbers, or part numbers from equipment labels."
            }
        ]

        # Process each image file
        for image_file in request.files:
            image_result = await self._process_image_file(image_file)
            if image_result:
                image_data, media_type = image_result

                # Convert image data to base64 for API
                image_base64 = base64.b64encode(image_data).decode('utf-8')

                # Add image to user content
                user_content.append({  # type: ignore
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{media_type};base64,{image_base64}"
                    }
                })

                self.logger.info(
                    f"Added image {image_file.name} to analysis request")

        # Add user message with text and images
        messages.append({  # type: ignore
            "role": "user",
            "content": user_content
        })

        try:
            # Execute chat completion with streaming - use type: ignore for complex message structure
            response = self.client.chat.completions.create(
                model=self.chat_deployment_name,
                messages=messages,  # type: ignore
                max_tokens=1000,
                temperature=0.1,  # Low temperature for accurate extraction
                stream=True
            )

            # Stream the response
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            error_msg = f"Error during image analysis: {str(e)}"
            self.logger.error(error_msg)
            yield error_msg

    async def reply_planner_async(self, request: ChatThreadRequest) -> AsyncGenerator[str, None]:
        """Main entry point for the image analysis agent (compatible with C# interface)"""
        async for chunk in self.analyze_images(request):
            yield chunk
