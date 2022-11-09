import pytest
from httpx import AsyncClient

from fast_api_recipes.schemas import RecipeSchemaIn
from fast_api_recipes.tests.conftest import PAYLOAD_DATA

pytestmark = pytest.mark.asyncio


async def test_get_recipes(client: AsyncClient):
    response = await client.get('/recipes')
    assert response.status_code == 200

    recipes = response.json()

    assert len(recipes) == 2

    for counter in range(len(recipes)):
        for recipe_attr in PAYLOAD_DATA[0]:
            assert recipes[counter].get(recipe_attr) == PAYLOAD_DATA[counter].get(recipe_attr)


async def test_post_recipes(client: AsyncClient):
    response_recipes = []
    for recipe in PAYLOAD_DATA:
        response = await client.post('/recipes', json=recipe)
        assert response.status_code == 201
        new_recipe = response.json()
        response_recipes.append(new_recipe)

    for counter in range(len(response_recipes)):
        for recipe_attr in PAYLOAD_DATA[0]:
            assert response_recipes[counter].get(recipe_attr) == PAYLOAD_DATA[counter].get(recipe_attr)
        assert response_recipes[counter].get('views_counter') == 0


async def test_post_recipes_incorrect_data(client: AsyncClient):
    incorrect_data = {'hello': 'world'}
    response = await client.post('/recipes', json=incorrect_data)
    assert response.status_code == 422

    desired_error = {
        'detail':
            [{'loc': ['body', 'title'], 'msg': 'field required', 'type': 'value_error.missing'},
             {'loc': ['body', 'ingredients'], 'msg': 'field required', 'type': 'value_error.missing'},
             {'loc': ['body', 'description'], 'msg': 'field required', 'type': 'value_error.missing'},
             {'loc': ['body', 'cooking_time'], 'msg': 'field required', 'type': 'value_error.missing'}]
    }

    assert response.json() == desired_error


async def test_get_certain_client(client: AsyncClient):
    response = await client.get('/recipes/1/')
