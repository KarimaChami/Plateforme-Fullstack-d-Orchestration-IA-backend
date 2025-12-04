from pydantic import BaseModel, Field


####
class UserCreate(BaseModel):
    username: str 
    password: str 

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AnalyzeRequest(BaseModel):
    text: str


class AnalyzeResponse(BaseModel):
    category: str
    score: float
    summary: str
    tone: str