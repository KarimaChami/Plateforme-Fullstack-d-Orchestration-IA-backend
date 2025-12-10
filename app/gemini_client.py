import os
from dotenv import load_dotenv
from google import genai
 # Assurez-vous que la dernière version est installée
# from app.hf_client import zero_shot_classify 

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
def generate_contextual_summary(text, categories):
    label = categories[0]

    prompt = f"""
Tu dois OBLIGATOIREMENT répondre en JSON strict.
Aucun texte hors du JSON.
Même si le texte est court, donne un résumé et un ton.

Répond EXACTEMENT comme ceci :

{{
    "summary": "...",
    "tone": "positif" 
}}

Texte : {text}
"""

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        raw = response.candidates[0].content.parts[0].text.strip()

        import json

        # Si Gemini entoure de ```json ... ``` => on nettoie
        if raw.startswith("```"):
            raw = raw.split("```")[1].replace("json", "").strip()

        return json.loads(raw)

    except Exception as e:
        return {"summary": "Résumé indisponible", "tone": "neutre", "error": str(e)}


# Exemple d'utilisation
# text_example = "Le marché boursier a connu une hausse significative aujourd'hui en raison des nouvelles économiques positives."
# categories = ["Finance", "RH", "IT", "Operations", "Marketing"]
# result = generate_contextual_summary(text_example, categories)
# print(result)
