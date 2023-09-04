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
    assert resp_data == {
        'detail': 'Error occurred while fetching data for pokemon "pokemon1"'}


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

    def fetch_pokemon_data_mock(*args, **kwargs):
        data = {}
        if 'pokemon1' in args:
            data = {
                'name': 'bulbasaur',
                'height': '0.7 kg',
                'weight': '6.9 m',
                'moves': [
                    'razor-wind',
                    'swords-dance',
                    'cut',
                    'bind',
                    'vine-whip'
                ],
                'stats': {
                    'hp': 45,
                    'attack': 49,
                    'defense': 49,
                }
            }

        if 'pokemon2' in args:
            data = {
                'name': 'wartortle',
                'height': '1.0 kg',
                'weight': '22.5 m',
                'moves': [
                    'mega-punch',
                    'ice-punch',
                    'mega-kick',
                    'headbutt',
                    'tackle'
                ],
                'stats': {
                    'hp': 59,
                    'attack': 63,
                    'defense': 80
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
        'winner': 'wartortle wins!',
        'cards': {
            'pokemon1': {
                'name': 'bulbasaur',
                'height': '0.7 kg',
                'weight': '6.9 m'
            },
            'pokemon2': {
                'name': 'wartortle',
                'height': '1.0 kg',
                'weight': '22.5 m'
            }
        }
    }

