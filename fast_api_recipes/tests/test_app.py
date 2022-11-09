import pytest
from fast_api_recipes.tests.conftest import PAYLOAD_DATA

pytestmark = pytest.mark.asyncio


async def test_get_recipes(client):
    response = await client.get('/recipes')
    assert response.status_code == 200
    assert response.read() == PAYLOAD_DATA
