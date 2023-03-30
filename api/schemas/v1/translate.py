from typing import Optional, List, Dict
from pydantic import BaseModel

class TranslateTextRequestSchema(BaseModel):
    src: str
    trg: str
    text: str
    
class TranslateTextResponseSchema(BaseModel):
    translation: List[str]