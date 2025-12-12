import pytest
from backend.app.utils.hf_client import zero_shot_classify

def test_mock_hf(mocker):
    input_text = "Le marché boursier a connu une hausse significative aujourd'hui en raison des nouvelles économiques positives"
    expected_hf_output = [{"label": "Marketing", "score": 0.95},{"label": "Finance", "score": 0.25}]

    fake_response = mocker.Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = expected_hf_output

    # Mock de requests.post
    mocker.patch("app.hf_client.requests.post",return_value=fake_response)
    
    result = zero_shot_classify(input_text)
    assert result == expected_hf_output
    assert result[0] == expected_hf_output[0]
    