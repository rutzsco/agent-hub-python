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
