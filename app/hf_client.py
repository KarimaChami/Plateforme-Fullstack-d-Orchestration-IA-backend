import os
import httpx
import asyncio
from dotenv import load_dotenv
import requests

load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"


# Your async function remains the same
def zero_shot_classify(text):
        categories = ["Finance", "RH", "IT", "Operations", "Marketing", "Legal","Sales", "Support", "Logistique", "Production", "Recherche et Développement", "Achats", "Communication", "Juridique", "Gestion de Projet"]
        headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
        def query(payload):
         response = requests.post(API_URL, headers=headers, json=payload)
         return response.json()
        try:
            if not text.strip():
                raise ValueError("Le texte ne peut pas être vide.")
            
            output = query({
                    "inputs": text,
                    "parameters": {"candidate_labels": categories},
                })
            
            return output  # affiche l'erreur complète de l'API

        except requests.exceptions.ConnectionError:
            return "erreur de connexion"
        except Exception as e:
            return f"erreur inattendue : {e}"
# Example usage
# result = zero_shot_classify(
#     "Le marché boursier a connu une hausse significative aujourd'hui en raison des nouvelles économiques positives.",
#     categories
# )
# print(result)