from models.api_models import ChatRequest, ChatResponse, ChatThreadRequest
from agents.chat_agent import ChatAgentService
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import sys
import os

# Add the parent directory to the path so we can import from agents and models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


app = FastAPI(
    title="Agent Hub Python API",
    description="FastAPI application with status endpoint and AI agent chat capabilities",
    version="0.1.0",
)

# Initialize the chat agent service
chat_agent_service = ChatAgentService()


@app.get("/status")
async def get_status():
    """
    Status endpoint that returns 200 OK with basic health information.
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "message": "Service is running",
            "version": "0.1.0"
        }
    )


@app.get("/")
async def root():
    """
    Root endpoint with basic information.
    """
    return {
        "message": "Welcome to Agent Hub Python API",
        "status_endpoint": "/status",
        "chat_endpoint": "/chat",
        "docs": "/docs"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """
    Chat with the AI agent.
    """
    try:
        # Create the chat thread request
        chat_request = ChatThreadRequest(
            message=request.message,
            thread_id=request.thread_id,
            file=request.file
        )

        # Call the chat agent service
        result = await chat_agent_service.run_chat_sk(chat_request)

        # Return the response
        return ChatResponse(
            content=result.content,
            thread_id=result.thread_id,
            sources=[{
                "quote": source.quote,
                "title": source.title,
                "url": source.url,
                "start_index": source.start_index,
                "end_index": source.end_index
            } for source in result.sources],
            files=[{"id": file_ref.id} for file_ref in result.files],
            intermediate_steps=result.intermediate_steps,
            code_content=result.code_content
        )

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")
