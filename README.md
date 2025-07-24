# Agent Hub Python

A FastAPI application providing AI agent chat capabilities powered by Azure AI Agent Service with Azure Semantic Kernel.

## Features

- **REST API** - FastAPI web framework with automatic documentation
- **AI Chat Agent** - Conversational AI powered by Azure AI Agent Service  
- **Image Analysis** - AI-powered image analysis capabilities
- **Health Monitoring** - Status endpoint for service health checks
- **Thread Management** - Conversation continuity with thread IDs
- **File Processing** - Support for file uploads and processing

## Quick Start

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Run the application:**
   ```bash
   uv run python main.py
   ```

3. **Access the API:**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/status

## API Endpoints

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/status` | GET | Health check endpoint |
| `/chat` | POST | Chat with AI agent |
| `/chat/stream` | POST | Stream chat responses |
| `/image-analysis` | POST | Analyze images with AI |
| `/docs` | GET | Interactive API documentation |

### Chat Example

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how can you help me?"}'
```

## Development

### Run with auto-reload:
```bash
uv run uvicorn api:app --reload
```

### Run tests:
```bash
uv run pytest
```

### VS Code Tasks
Use `Ctrl+Shift+P` → "Tasks: Run Task" to access:
- Install Dependencies
- Run FastAPI Development Server  
- Run Tests
- Run Tests with Coverage

## Configuration

The application supports Azure AI Agent Service integration. Configure via environment variables:

```bash
AZURE_AI_AGENT_ID=your_agent_id
AZURE_AI_AGENT_ENDPOINT=https://your-endpoint.cognitiveservices.azure.com/
```

## Requirements

- Python 3.10+
- UV package manager
- Azure AI Agent Service (for chat functionality)