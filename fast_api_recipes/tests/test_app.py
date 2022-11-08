from fastapi.testclient import TestClient

from fast_api_recipes.main import app

client = TestClient(app)
