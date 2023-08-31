import pytest
from unittest.mock import patch
from app.api.battle import path
from starlette.status import (HTTP_200_OK, HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR)
from app.models.pokemon import Pokemon


@pytest.mark.asyncio
@patch("app.utils.fetch_pokemon_data")
async def test_start_battle_with_unknown_pokemon(
        fetch_pokemon_data, client):
    fetch_pokemon_data.return_value = None

    response = client.post(
        path,
        json={
            'pokemon1': 'pokemon1',
            'pokemon2': 'pokemon2'
        }
    )

    resp_data = response.json()

    assert response.status_code == HTTP_404_NOT_FOUND
    assert resp_data == {'detail': 'One or both Pokemon not found'}


@pytest.mark.asyncio
@patch("app.api.battle.fetch_pokemon_data")
async def test_start_battle_exception(fetch_pokemon_data, client):
    fetch_pokemon_data.side_effect = Exception("Something happend")

    response = client.post(
        path,
        json={
            'pokemon1': 'pokemon1',
            'pokemon2': 'pokemon2'
        }
    )

    resp_data = response.json()

    assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR
    assert resp_data == {'detail': 'Something happend'}


@pytest.mark.asyncio
@patch("app.api.battle.fetch_pokemon_data")
async def test_start_battle(fetch_pokemon_data, client):

    pokemon1_card = {
        'name': 'bulbasaur',
        'id': 1,
        'height': 7,
        'weight': 69,
        'types': [
            'grass',
            'poison'
        ]
    }

    pokemon2_card = {
        'name': 'wartortle',
        'id': 8,
        'height': 10,
        'weight': 225,
        'types': [
            'water'
        ]
    }

    def fetch_pokemon_data_mock(*args, **kwargs):
        data = {}
        if 'pokemon1' in args:
            data = {
                'id_card': pokemon1_card,
                'stats': {
                    'hp': 45,
                    'attack': 49,
                    'defense': 49,
                    'special-attack': 65,
                    'special-defense': 65,
                    'speed': 45
                }
            }

        if 'pokemon2' in args:
            data = {
                'id_card': pokemon2_card,
                'stats': {
                    'hp': 59,
                    'attack': 63,
                    'defense': 80,
                    'special-attack': 65,
                    'special-defense': 80,
                    'speed': 58
                }
            }

        return Pokemon(**data)


    fetch_pokemon_data.side_effect = fetch_pokemon_data_mock

    response = client.post(
        path,
        json={
            'pokemon1': 'pokemon1',
            'pokemon2': 'pokemon2'
        }
    )

    resp_data = response.json()

    assert response.status_code == HTTP_200_OK
    assert resp_data == {
        'winner': 'wartortle',
        'pokemon1': pokemon1_card,
        'pokemon2': pokemon2_card
    }

