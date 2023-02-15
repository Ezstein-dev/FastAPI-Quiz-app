from datetime import datetime
from pydantic import BaseModel


class QuizCreate(BaseModel):
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    answer: str

class QuizOut(BaseModel):
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    created_at: datetime
    
    class Config:
        orm_mode = True
    
class ResponseIn(BaseModel):
    answer: str