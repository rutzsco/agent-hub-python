# Agents

This folder contains AI agent implementations for the Agent Hub Python API.

## ChatAgent

The `ChatAgent` is based on Azure AI Agent Service and Semantic Kernel. It provides:

- Chat interactions with Azure OpenAI models
- Thread management for conversation continuity
- File upload and processing capabilities
- Vector store integration for file search
- Streaming responses with intermediate steps

### Configuration

To use the ChatAgent, you need to set up the following environment variables in your `.env` file:

```env
# Azure AI Agent Configuration
AZURE_AI_AGENT_ID=your_agent_id_here
AZURE_AI_AGENT_ENDPOINT=https://your-agent-endpoint.cognitiveservices.azure.com/

# Azure Blob Storage Configuration (optional, for file processing)
AZURE_BLOB_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=your_account;AccountKey=your_key;EndpointSuffix=core.windows.net
```

### Usage

The ChatAgent can be used through the FastAPI endpoint:

```python
# POST /chat
{
    "message": "Your message here",
    "thread_id": "optional_thread_id_for_conversation_continuity",
    "file": "optional_file_path_in_blob_storage"
}
```

### Features

1. **Conversation Threads**: Maintains conversation context across multiple messages
2. **File Processing**: Can process files from Azure Blob Storage and integrate them into conversations
3. **Vector Search**: Uses Azure AI's vector store for semantic file search
4. **Streaming**: Supports streaming responses with intermediate steps
5. **Source Citations**: Provides source references and annotations for responses

### Dependencies

The ChatAgent requires the following packages:
- `azure-ai-projects`
- `azure-storage-blob`
- `azure-identity`
- `semantic-kernel`
- `opentelemetry-api`
- `python-dotenv`

These are included in the project's `pyproject.toml` file.

## ImageAnalysisAgent

The `ImageAnalysisAgent` is specialized for extracting serial numbers, model numbers, and part numbers from equipment labels and nameplates using Azure OpenAI's vision capabilities.

### Features

- **Serial Number Extraction**: Automatically identifies and extracts serial numbers from equipment labels
- **Multi-format Support**: Handles various label formats including metallic plates, adhesive labels, and engraved text
- **Structured Output**: Provides organized results with serial numbers, model numbers, part numbers, and manufacturer information
- **Image Processing**: Supports both base64 data URLs and Azure Blob Storage references
- **Streaming Response**: Real-time analysis results via streaming API

### Configuration

The ImageAnalysisAgent requires the following environment variables:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-openai-endpoint.openai.azure.com/
AZURE_OPENAI_API_KEY=your_openai_api_key
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o

# Azure Blob Storage Configuration (optional, for blob-based images)
AZURE_BLOB_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=your_account;AccountKey=your_key;EndpointSuffix=core.windows.net
```

### Usage

The ImageAnalysisAgent can be used through the FastAPI endpoint:

```python
# POST /image-analysis
{
    "message": "Extract serial numbers from this equipment label",
    "files": [
        {
            "name": "equipment_label.jpg",
            "data_url": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
        }
    ]
}
```

### Supported Input Formats

#### Data URL Format
```json
{
  "message": "Extract serial numbers from this equipment label",
  "files": [
    {
      "name": "equipment_label.jpg", 
      "data_url": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
    }
  ]
}
```

#### Azure Blob Storage Format
```json
{
  "message": "Analyze equipment labels",
  "files": [
    {
      "name": "equipment_label.jpg",
      "blob_name": "images/equipment_label.jpg"
    }
  ]
}
```

### Response Format

The agent returns structured information about identified serial numbers and equipment details:

```
Serial Number: ABC123456789
Model Number: XJ-2000
Part Number: PT-9876-X
Manufacturer: ACME Corp
Additional Notes: Label located on the left side panel, barcode visible below serial number
```

### Image Analysis Capabilities

The agent is trained to:

1. **Identify Common Label Types**:
   - Metallic nameplates
   - Adhesive labels
   - Engraved text
   - Barcode labels with text
   - QR code labels

2. **Extract Key Information**:
   - Serial numbers
   - Model numbers
   - Part numbers
   - Asset tags
   - Manufacturer information

3. **Handle Edge Cases**:
   - Partially obscured text
   - Poor image quality
   - Multiple labels in one image
   - Rotated or angled labels

### Dependencies

The ImageAnalysisAgent requires the following packages:
- `openai`
- `azure-storage-blob`
- `azure-identity`
- `python-dotenv`

These are included in the project's `pyproject.toml` file.
