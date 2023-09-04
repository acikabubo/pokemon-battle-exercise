import pytest
from httpx import Response
from unittest.mock import patch
from starlette.status import HTTP_200_OK
from app.utils import fetch_pokemon_data, fetch_move_data


@pytest.mark.asyncio
@patch("app.utils.fetch_data")
async def test_fetch_pokemon_data(fetch_data):
    data = {
        "name": "bulbasaur",
        "id": 1,
        "height": 7,
        "weight": 69,
        "moves": [
            {
                "move": {
                    "name": "razor-wind"
                }
            },
            {
                "move": {
                    "name": "swords-dance"
                }
            },
            {
                "move": {
                    "name": "cut"
                }
            },
            {
                "move": {
                    "name": "bind"
                }
            },
            {
                "move": {
                    "name": "vine-whip"
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
            },
            {
                "base_stat": 49,
                "stat": {
                    "name": "defence"
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
        "name": "bulbasaur",
        "height": "0.7 kg",
        "weight": "6.9 m",
        "moves": [
            "razor-wind",
            "swords-dance",
            "cut",
            "bind",
            "vine-whip"
        ],
        "stats": {
            "hp": 45,
            "attack": 49,
            "defence": 49
        }}


@pytest.mark.asyncio
@patch("app.utils.fetch_data")
async def test_fetch_move_data(fetch_data):
    data = {
        "name": "razor-wind",
        "power": 15
    }

    fetch_data.return_value = Response(
        HTTP_200_OK,
        json=data
    )

    move = await fetch_move_data("razor-wind")

    assert move.model_dump() == {
        "name": "razor-wind",
        "power": 15
    }
