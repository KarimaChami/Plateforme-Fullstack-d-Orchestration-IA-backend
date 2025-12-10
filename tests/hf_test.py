import pytest
from app.hf_client import zero_shot_classify

def test_mock_hf(mocker):
    input_text = "Le marché boursier a connu une hausse significative aujourd'hui en raison des nouvelles économiques positives"
    expected_hf_output = [{"label": "Marketing", "score": 0.95}]

    # Création d'un faux objet réponse
    fake_response = mocker.Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = expected_hf_output

    # Mock de requests.post
    mocker.patch(
        "app.hf_client.requests.post",
        return_value=fake_response
    )

    # Appel de la fonction réelle
    result = zero_shot_classify(input_text)

    # Assertions
    assert result == expected_hf_output
    assert result[0] == expected_hf_output[0]
    
    # assert result == expected_hf_output[0]
    # assert result["label"] == "Marketing"
    # assert result["score"] == 0.95
