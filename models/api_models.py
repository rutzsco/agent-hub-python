from typing import List, Optional
from pydantic import BaseModel


class Source(BaseModel):
    """Model for source information"""
    quote: str = ''
    title: str = ''
    url: str = ''
    start_index: str = ''
    end_index: str = ''


class FileReference(BaseModel):
    """Model for file reference"""
    id: str = ''


class ChatThreadRequest(BaseModel):
    """Model for chat thread request"""
    message: str
    thread_id: Optional[str] = None
    file: Optional[str] = None


class RequestResult(BaseModel):
    """Model for request result"""
    content: str
    sources: List[Source] = []
    files: List[FileReference] = []
    intermediate_steps: List[str] = []
    thread_id: str = ''
    code_content: str = ''


class ChatRequest(BaseModel):
    """Model for API chat request"""
    message: str
    thread_id: Optional[str] = None
    file: Optional[str] = None


class ChatResponse(BaseModel):
    """Model for API chat response"""
    content: str
    thread_id: str
    sources: List[dict] = []
    files: List[dict] = []
    intermediate_steps: List[str] = []
    code_content: str = ""
