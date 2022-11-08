from fastapi.testclient import TestClient

from fast_api_recipes.main import get_app

app = get_app(testing=True)

client = TestClient(app)


def test_main():
    response = client.get('/recipes')
    assert response.status_code == 200

