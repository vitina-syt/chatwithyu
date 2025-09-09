from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class QuestionRequest(BaseModel):
    question: str

class PDFFileResponse(BaseModel):
    filename: str
    file_size: int
    processed_text: str
    created_at: datetime
    success: bool
    message: Optional[str] = None

class PDFFileCreate(BaseModel):
    filename: str
    file_size: int
    processed_text: str
    created_at: datetime