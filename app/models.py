from database import Base 
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy import JSON, Text
 

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True,nullable=False)
    # email = Column(String, unique=True, index=True,nullable=False)
    password_hash = Column(String, nullable=False)
    createdate = Column(DateTime(timezone=True), server_default=func.now())
    
# Optionnel : logs
# class AnalysisLog(Base):
#     __tablename__ = "analysis_logs"

#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, nullable=True)
#     input_text = Column(Text)
#     hf_response = Column(JSON)
#     gemini_response = Column(JSON)
#     createdat = Column(DateTime(timezone=True), server_default=func.now())