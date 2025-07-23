from fastapi import FastAPI
from .routes import default, agents

app = FastAPI(
    title="Agent Hub Python API",
    description="FastAPI application with status endpoint and AI agent chat capabilities",
    version="0.1.0",
)

# Include route modules
app.include_router(default.router)
app.include_router(agents.router)
