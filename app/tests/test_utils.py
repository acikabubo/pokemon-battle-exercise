import pytest
from httpx import Response
from unittest.mock import patch
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from app.utils import fetch_pokemon_data


@pytest.mark.asyncio
@patch("app.utils.fetch_data")
async def test_fetch_pokemon_data_unknown(fetch_data):
    fetch_data.return_value = Response(HTTP_404_NOT_FOUND)

    pokemon = await fetch_pokemon_data("unknown_pokemon")

    assert pokemon is None


@pytest.mark.asyncio
@patch("app.utils.fetch_data")
async def test_fetch_pokemon_data(fetch_data):
    data = {
        "name": "bulbasaur",
        "id": 1,
        "height": 7,
        "weight": 69,
        "types": [
            {
                "type": {
                    "name": "grass"
                }
            },
            {
                "type": {
                    "name": "poison"
                }
            }
        ],
        "stats": [
            {
                "base_stat": 45,
                "stat": {
                    "name": "hp"
                }
            },
            {
                "base_stat": 49,
                "stat": {
                    "name": "attack"
                }
            }
        ]
    }

    fetch_data.return_value = Response(
        HTTP_200_OK,
        json=data
    )

    pokemon = await fetch_pokemon_data("bulbasaur")

    assert pokemon.model_dump() == {
        "id_card": {
            "name": "bulbasaur",
            "id": 1,
            "height": 7,
            "weight": 69,
            "types": [
                "grass",
                "poison"
            ]
        },
        "stats": {
            "hp": 45,
            "attack": 49
        }
    }
