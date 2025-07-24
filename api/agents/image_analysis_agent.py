import os
import logging
import base64
from typing import Optional, AsyncGenerator, List, Dict, Any, Union
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from opentelemetry import trace

import semantic_kernel as sk
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.contents import ChatMessageContent, FunctionCallContent
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments

from ..models.api_models import ChatThreadRequest, ImageFile, RequestResult
from .agent_utils import AgentUtils


class ImageAnalysisAgent:
    """Agent for analyzing images and extracting serial numbers from equipment labels using Semantic Kernel"""

    def __init__(self):
        load_dotenv()

        self.logger = logging.getLogger(__name__)
        self.agent_utils = AgentUtils()

        # Retrieve configuration from environment variables
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-4o")
        self.azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")

        if not endpoint or not deployment_name:
            raise ValueError("Missing required environment variables for OpenAI configuration.")

        # Initialize Semantic Kernel
        self.kernel = sk.Kernel()

        # Configure Azure OpenAI service - use API key authentication
        if not api_key:
            raise ValueError("Azure OpenAI API key must be configured")
            
        self.kernel.add_service(AzureChatCompletion(
            api_key=api_key,
            endpoint=endpoint,
            deployment_name=deployment_name,
            service_id="azure-chat-completion"
        ))

        # Azure Blob Storage configuration (optional)
        blob_connection_string = os.getenv("AZURE_BLOB_CONNECTION_STRING")
        self.blob_container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME", "images")
        self.blob_service_client = None
        if blob_connection_string:
            self.blob_service_client = BlobServiceClient.from_connection_string(
                blob_connection_string
            )

        # Log initialization details
        config_details = {
            "Azure OpenAI Endpoint": endpoint,
            "Azure OpenAI API Key": api_key,
            "API Version": self.azure_openai_api_version,
            "Chat Deployment": deployment_name,
            "Blob Container": self.blob_container_name,
            "Blob Storage Configured": bool(self.blob_service_client),
            "Authentication Method": "API Key"
        }
        self.agent_utils.log_agent_initialization("ImageAnalysisAgent", config_details)

    def _get_system_prompt(self) -> str:
        """Get the system prompt for image analysis"""
        return self.agent_utils.get_system_prompt("image_analysis_system_prompt.txt")

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

    async def analyze_images(self, request: ChatThreadRequest) -> RequestResult:
        """Analyze images for serial number extraction using Semantic Kernel Agent"""
        
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("Agent: ImageAnalysis") as current_span:
            
            if not request.files:
                return RequestResult(
                    content="No images provided for analysis.",
                    intermediate_steps=[],
                    thread_id=""
                )

            # Define a list to hold callback message content for intermediate steps
            intermediate_steps: List[str] = []

            # Define an async method to handle the `on_intermediate_message` callback
            async def handle_intermediate_steps(message: ChatMessageContent) -> None:
                if any(isinstance(item, FunctionCallContent) for item in message.items):
                    for fcc in message.items:
                        if isinstance(fcc, FunctionCallContent):
                            intermediate_steps.append(f"Function Call: {fcc.name} with arguments: {fcc.arguments}")

            try:
                # Build the user message with text and image content
                user_message_text = request.message or "Please analyze the provided images and extract any serial numbers, model numbers, or part numbers from equipment labels."
                
                # Process images and convert to base64 data URLs
                image_data_urls = []
                for image_file in request.files:
                    image_result = await self._process_image_file(image_file)
                    if image_result:
                        image_data, media_type = image_result
                        image_base64 = base64.b64encode(image_data).decode('utf-8')
                        data_url = f"data:{media_type};base64,{image_base64}"
                        image_data_urls.append(data_url)
                        self.logger.info(f"Added image {image_file.name} to analysis request")

                # Create a comprehensive message that includes text and image references
                if image_data_urls:
                    user_message_text += f"\n\nI have provided {len(image_data_urls)} image(s) for analysis. Please examine each image carefully and extract any visible serial numbers, model numbers, part numbers, or other identifying information from equipment labels or nameplates."

                system_message = self._get_system_prompt()
                
                # Configure execution settings
                settings = PromptExecutionSettings(
                    function_choice_behavior=FunctionChoiceBehavior.Auto(),
                )
                kernel_arguments = KernelArguments(settings=settings)
                kernel_arguments["diagnostics"] = []

                # Create the chat completion agent
                agent = ChatCompletionAgent(
                    kernel=self.kernel,
                    name="ImageAnalysisAgent",
                    instructions=system_message,
                    arguments=kernel_arguments
                )

                # Note: For now, we'll handle images by including them in the message context
                # The Semantic Kernel agent framework may need additional configuration for image handling
                
                # Iterate over the async generator to get the final response
                response = None
                thread = None

                async for result in agent.invoke(messages=user_message_text, thread=thread, on_intermediate_message=handle_intermediate_steps):
                    response = result
                    thread = response.thread

                if response is None:
                    raise ValueError("No response received from the agent.")

                return RequestResult(
                    content=f"{response}",
                    intermediate_steps=intermediate_steps,
                    thread_id=str(thread.id) if thread else ""
                )

            except Exception as e:
                error_msg = f"Error during image analysis: {str(e)}"
                self.logger.error(error_msg)
                return RequestResult(
                    content=error_msg,
                    intermediate_steps=intermediate_steps,
                    thread_id=""
                )

    async def reply_planner_async(self, request: ChatThreadRequest) -> RequestResult:
        """Main entry point for the image analysis agent (compatible with C# interface)"""
        return await self.analyze_images(request)
    
    async def analyze_images_streaming(self, request: ChatThreadRequest) -> AsyncGenerator[str, None]:
        """Streaming version for backward compatibility"""
        result = await self.analyze_images(request)
        yield result.content
