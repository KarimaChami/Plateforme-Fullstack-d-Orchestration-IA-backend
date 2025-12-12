# from fastapi.testclient import TestClient
# from app.main import app
# from app.hf_client import zero_shot_classify
# from app.gemini_client import generate_contextual_summary

# client = TestClient(app)

# def test_analyze_endpoint(mocker):
#     input_text = "Le marché boursier a connu une hausse significative aujourd'hui."

#     # Mock Hugging Face
#     hf_mock_output = [{"label": "Finance", "score": 0.95}]
#     mocker.patch("app.hf_client.zero_shot_classify", return_value=hf_mock_output)

#     # Mock Gemini
#     gemini_mock_output = {
#         "summary": "Le marché boursier a fortement progressé suite à de bonnes nouvelles économiques.",
#         "tone": "positif"
#     }
#     mocker.patch("app.gemini_client.generate_contextual_summary", return_value=gemini_mock_output)

#     # Mock utilisateur authentifié
#     from app.auth import get_current_user
#     from app.models import User
#     fake_user = User(username="testuser", email="test@test.com")
#     mocker.patch("app.dependencies.get_current_user", return_value=fake_user)

#     # Test endpoint
#     response = client.post("/analyze", json={"text": input_text})
#     assert response.status_code == 200

#     data = response.json()
#     assert data["category"] == "Finance"
#     assert data["score"] == 0.95
#     assert data["summary"] == gemini_mock_output["summary"]
#     assert data["tone"] == gemini_mock_output["tone"]


  