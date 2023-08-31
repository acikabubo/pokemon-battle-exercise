from httpx import AsyncClient
from starlette.status import HTTP_200_OK
from app.models.pokemon import Pokemon


async def fetch_data(client: AsyncClient, url: str) -> dict:
    return await client.get(url)  # pragma: no cover


async def fetch_pokemon_data(name) -> Pokemon:
    async with AsyncClient() as client:

        response = await fetch_data(
            client, f"https://pokeapi.co/api/v2/pokemon/{name}")

    if response.status_code != HTTP_200_OK:
        return

    data = response.json()

    pokemon_data = {
        'id_card': {
            'name': data['name'],
            'id': data['id'],
            'height': data['height'],
            'weight': data['weight'],
            'types': [t['type']['name'] for t in data['types']]
        },
        'stats': {
            stat['stat']['name']: stat['base_stat']
            for stat in data['stats']
        }
    }

    return Pokemon(**pokemon_data)
