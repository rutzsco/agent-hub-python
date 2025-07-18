# agent-hub-python

A FastAPI application with status endpoint and AI agent chat capabilities powered by Azure AI Agent Service.

## Project Structure

```
agent-hub-python/
├── .vscode/                # VS Code configuration
│   ├── launch.json        # Debug/run configurations
│   ├── settings.json      # Project settings
│   ├── tasks.json         # Build and test tasks
│   └── extensions.json    # Recommended extensions
├── agents/                 # AI agent implementations
│   ├── __init__.py        # Package initialization
│   ├── chat_agent.py      # ChatAgent implementation
│   └── README.md          # Agent documentation
├── api/                    # API package containing FastAPI application
│   ├── __init__.py        # Package initialization
│   └── main.py            # FastAPI app definition
├── models/                 # Data models and schemas
│   ├── __init__.py        # Package initialization
│   └── api_models.py      # Pydantic models for API
├── main.py                # Main entry point
├── run.py                 # Development server script
├── test_main.py           # Unit tests
├── test_api.http          # HTTP requests for testing API
├── .env.example           # Environment variables template
├── pyproject.toml         # Project configuration and dependencies
└── README.md              # This file
```

## Features

- FastAPI web framework
- Status endpoint at `/status` that returns 200 OK
- AI chat endpoint at `/chat` powered by Azure AI Agent Service
- Automatic API documentation at `/docs`
- Package management with uv
- Azure AI integration with Semantic Kernel
- Conversation thread management
- File processing capabilities
- Vector store integration for semantic search

## Setup

1. Install uv (if not already installed):
   ```bash
   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # On macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Configure Azure AI (for chat functionality):
   ```bash
   # Copy the example environment file
   copy .env.example .env
   
   # Edit .env and add your Azure AI Agent configuration:
   # AZURE_AI_AGENT_ID=your_agent_id_here
   # AZURE_AI_AGENT_ENDPOINT=https://your-agent-endpoint.cognitiveservices.azure.com/
   ```

## Running the Application

### Using uv:
```bash
uv run python main.py
```

### Using the run script:
```bash
uv run python run.py
```

### Direct uvicorn:
```bash
uv run uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

## VS Code Development

This project includes VS Code configuration for an optimal development experience:

### Launch Configurations (F5 to debug):
- **FastAPI: Debug** - Debug the main application
- **FastAPI: Run (Development)** - Run with hot reload
- **FastAPI: Uvicorn Direct** - Run using uvicorn directly  
- **FastAPI: Production Mode** - Run in production mode
- **Python: Current File** - Debug the currently open file
- **Python: Run Tests** - Debug pytest tests

### Tasks (Ctrl+Shift+P → "Tasks: Run Task"):
- **Install Dependencies** - Run `uv sync`
- **Run FastAPI Server** - Start the server
- **Run FastAPI Development Server** - Start with hot reload
- **Run FastAPI with Uvicorn** - Direct uvicorn execution
- **Run Tests** - Execute pytest
- **Run Tests with Coverage** - Run tests with coverage report

### Recommended Extensions:
The project includes recommended VS Code extensions for Python, FastAPI, and TOML development. Install them when prompted or manually via the Extensions panel.

## API Endpoints

- `GET /` - Root endpoint with basic information
- `GET /status` - Status endpoint that returns 200 OK with health information
- `POST /chat` - Chat with AI agent (requires Azure AI configuration)
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

### Chat Endpoint

The chat endpoint allows you to interact with the Azure AI Agent:

```json
POST /chat
{
  "message": "Hello, how can you help me today?",
  "thread_id": "optional_thread_id_for_conversation_continuity",
  "file": "optional_file_path_in_blob_storage"
}
```

Response:
```json
{
  "content": "Hello! I'm here to help you with any questions or tasks you might have...",
  "thread_id": "thread_12345",
  "sources": [],
  "files": [],
  "intermediate_steps": [],
  "code_content": ""
}
```

## Testing

Run tests with:
```bash
uv run pytest
```

## Example Response

The `/status` endpoint returns:
```json
{
  "status": "healthy",
  "message": "Service is running",
  "version": "0.1.0"
}
```