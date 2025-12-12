from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy import JSON, Text
from backend.app.database import Base
 



class AnalysisLog(Base):
    __tablename__ = "analysis_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    input_text = Column(Text)
    hf_response = Column(JSON)
    gemini_response = Column(JSON)
    createdat = Column(DateTime(timezone=True), server_default=func.now())