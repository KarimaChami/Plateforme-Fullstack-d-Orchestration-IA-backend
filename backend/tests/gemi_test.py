
from backend.app.utils.gemini_client import generate_contextual_summary
import json 

def test_mock_gemini(mocker):
    input_text = "Le marché boursier a connu une hausse significative aujourd'hui en raison des nouvelles économiques positives"
    expected_gemini_output = {'summary': 'Le marché boursier a fortement progressé suite à de bonnes nouvelles économiques.',
                           'tone': 'positif'}
    # Création d'un faux objet qui ressemble à la vraie réponse Gemini
    fake_part = mocker.Mock()
    fake_part.text = f"```json\n{json.dumps(expected_gemini_output)}\n```"

    fake_content = mocker.Mock()
    fake_content.parts = [fake_part]

    fake_candidate = mocker.Mock()
    fake_candidate.content = fake_content

    fake_response = mocker.Mock()
    fake_response.candidates = [fake_candidate]

    # Patch du client Gemini
    fake_client = mocker.Mock()
    fake_client.models.generate_content.return_value = fake_response
    
    mocker.patch(
    "app.gemini_client.genai.Client",
    return_value = fake_client
    )

    result = generate_contextual_summary(input_text,categories = ["Finance", "RH", "IT", "Operations", "Marketing"])

    assert result == expected_gemini_output
    assert result["summary"] == expected_gemini_output["summary"]
    assert result["tone"] == expected_gemini_output["tone"]