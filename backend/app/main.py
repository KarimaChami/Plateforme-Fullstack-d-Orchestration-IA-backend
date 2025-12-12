from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base,get_db
from app.gemini_client import generate_contextual_summary
from app.schemas import UserCreate, Token, AnalyzeRequest, AnalyzeResponse
# from app.gemini_client import generate_contextual_summary
from app.models import User
from app.auth import create_access_token, get_user_by_username, create_user, verify_password,get_current_user
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from datetime import timedelta
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



@app.post('/analyze', response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
 """
    Orchestration complète :
    1. Analyse Zero-Shot avec Hugging Face
    2. Passer la catégorie à Gemini pour résumé + ton
    3. Retour structuré
    """
 # Hugging Face
 try:
       hf_result =  zero_shot_classify(req.text)
 except Exception as e:
        print("Erreur HF:", e)
        raise HTTPException(status_code=500, detail="Erreur Hugging Face:{e}")
   # Vérification format
 if not isinstance(hf_result, list):
        raise HTTPException(status_code=500, detail=f"Réponse HF invalide : {hf_result}")

 try:
        predicted_label = hf_result[0]["label"]
        score = hf_result[0]["score"]

 except Exception as e:
        raise HTTPException(status_code=500, detail=f"Format inattendu HF : {hf_result}")



# 2. Gemini
 try:
        gemini_res = generate_contextual_summary(
            text=req.text,
            categories=[predicted_label]
        )
 except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur API Gemini : {e}")

 summary = gemini_res.get("summary", "Aucun résumé généré")
 tone = gemini_res.get("tone", "Neutre")

 return AnalyzeResponse(
        category=predicted_label,
        score=score,
        summary=summary,
        tone=tone
    )






#  summary = gemini_res.get("summary")
#  tone = gemini_res.get("tone")
#  return AnalyzeResponse(
#       category = predicted_label,
#       score = score,
#       summary = summary,
#       tone = tone 
#       )



