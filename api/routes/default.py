from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/status")
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


@router.get("/")
async def root():
    """
    Root endpoint with basic information.
    """
    return {
        "message": "Welcome to Agent Hub Python API",
        "status_endpoint": "/status",
        "chat_endpoint": "/chat",
        "image_analysis_endpoint": "/image-analysis",
        "docs": "/docs"
    }
