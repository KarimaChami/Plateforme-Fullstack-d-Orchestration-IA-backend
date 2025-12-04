from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from schemas import UserCreate, Token
from models import User
from auth import create_access_token, get_user_by_username, create_user, verify_password,get_current_user
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from datetime import timedelta
from schemas import AnalyzeRequest, AnalyzeResponse
from .hf_client import zero_shot_classify



Base.metadata.create_all(bind=engine)
app = FastAPI()

# CORS - Autoriser le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hybrid-Analyzer Backend API"}


@app.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = create_user(db, user)
    access_token = create_access_token({"sub": new_user.username})
    return {"access_token": access_token,"token_type": "bearer"}



@app.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, username=form_data.username)
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401,detail="Incorrect username or password")

    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Analyze
CANDIDATE_LABELS = ["Finance", "RH", "IT", "Operations", "Marketing", "Legal"]


@app.post('/analyze', response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest, db: Session = Depends(get_db),current_user=Depends(get_current_user)):
 """
    Orchestration complète :
    1. Analyse Zero-Shot avec Hugging Face
    2. Passer la catégorie à Gemini pour résumé + ton
    3. Retour structuré
    """
 # STEP 1 — Hugging Face
 try:
       hf_result = await zero_shot_classify(req.text)
 except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur Hugging Face.")
 predicted_label = hf_result.get("label")
 score = hf_result.get("score")

 if not predicted_label:
            raise HTTPException(status_code=500, detail="Classification HF invalide.")

# STEP 2 — Gemini
 try:
        gemini_res = await generate_contextual_summary(
            text=req.text,
            category=predicted_label
        )
 except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur API Gemini.")
 summary = gemini_res.get("summary")
 tone = gemini_res.get("tone")
 return AnalyzeResponse(
      category = predicted_label,
      score = score,
      summary = summary,
      tone = tone 
      )



