from pydantic import BaseModel
from typing import Optional, Any, List

class CreateRequestIn(BaseModel):
    workspace_id: Optional[int] = 1

class RequestOut(BaseModel):
    id: int
    status: str
    created_at: Optional[str]

class ExtractedFieldOut(BaseModel):
    id: int
    key: str
    value: Optional[Any]
    confidence: Optional[float]
    source: Optional[str]
    evidence_page: Optional[int]
    evidence_text: Optional[str]

class RequestDetailOut(BaseModel):
    id: int
    status: str
    extracted_fields: List[ExtractedFieldOut] = []
