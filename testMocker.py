

# import requests
# import os

# API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-fr"
# HEADERS = {"Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}"}

# def translate_text(input_text):

#     payload = {
#         "inputs": input_text
#     }
    
#     response = requests.post(API_URL, headers=HEADERS, json=payload)
#     response.raise_for_status() # Vérifie que la requête a réussi
#     result_list = response.json() # Récupère la réponse JSON
#     return result_list[0]["translation_text"]
# translate_text("Hello world")
# '''
# [
#   {
#     "translation_text": "Bonjour le monde"
#   }
# ]
# '''

# def test_translate(mocker):
#     expected_output = [{"translation_text": "Bonjour le monde"}]
#     fake = mocker.Mock()
#     fake.status_code = 200 
#     fake.json.retun_value = expected_output

#     mocker.patch(
#         "requests.post", # Le chemin vers la fonction à remplacer
#         return_value=fake)
#     res = translate_text("hello world")
#     assert res


    




















# ############################## fichier test ##########################

# # from module import translate_text 
# import pytest



# def test_translation_success(mocker):

#     # input_text = "Hello world"
#     # expected_output = "Bonjour le monde"

#     expected_hf_output = [{"translation_text": "Bonjour le monde"}]

#     fake_response = mocker.Mock()
#     fake_response.status_code = 200
#     fake_response.json.return_value = expected_hf_output
# # mocker.patch(cible, [arguments de configuration]) / return_value (Le Résultat Attendu)

#     mocker.patch(
#         "requests.post", # Le chemin vers la fonction à remplacer
#         return_value=fake_response 
#     )
#     result = translate_text("Hello world")

#     assert result == "Bonjour le monde"

# [
#   {
#     "translation_text": "Bonjour le monde"
#   }
# ]