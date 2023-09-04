import random
from httpx import AsyncClient
from fastapi import HTTPException
from starlette.status import HTTP_200_OK
from cachetools import TTLCache
from app.models.pokemon import Pokemon, Move
from app.constants import POKEMON_URL, MOVE_URL
from app.logger import logger


# Create a cache with a TTL (time-to-live) of 3600 seconds (60 minutes)
cache = TTLCache(maxsize=100, ttl=3600)


def convert_measurement(meas: int) -> float:
    """
    There are 10 decimeters in 1 meter or 10 hectograms in 1 kilogram.

    For both measurements is 10 to 1 so i will use one function for conversion

    More info at: https://pokeapi.co/docs/v2#pokemon-section

    Args:
        meas (integer): measurement is in
        hectograms for weight or decimeter for weight

    Returns:
        float: measurement which is hectograms or decimeter devided by 10
    """
    return meas / 10


# Used function wrapper around AsyncClient because it's easier for mocking
async def fetch_data(client: AsyncClient, url: str) -> dict:  # pragma: no cover
    # Check if data is already cached
    if url in cache:
        logger.info(f'Get cached data for {url}')
        return cache[url]

    # If not cached, fetch the data and cache it
    data = await client.get(url)
    cache[url] = data

    return data


async def fetch_move_data(name) -> Move:
    async with AsyncClient() as client:
        response = await fetch_data(
            client, f"{MOVE_URL}{name}/")

    if response.status_code != HTTP_200_OK:
        detail = f'Error occurred while fetching data for move "{name}"'
        logger.error(detail)
        raise HTTPException(
            status_code=response.status_code,
            detail=detail
        )

    data = response.json()

    return Move(
        name=data['name'],
        power=data['power'] or 0
    )


async def fetch_pokemon_data(name) -> Pokemon:
    async with AsyncClient() as client:
        response = await fetch_data(
            client, f"{POKEMON_URL}{name}")

    if response.status_code != HTTP_200_OK:
        detail = f'Error occurred while fetching data for pokemon "{name}"'
        logger.error(detail)
        raise HTTPException(
            status_code=response.status_code,
            detail=detail
        )

    data = response.json()

    # Format move data
    moves = [m['move']['name'] for m in data['moves']]

    # Format stats data
    stats={
        stat['stat']['name']: stat['base_stat']
        for stat in data['stats']
    }

    return Pokemon(
        name=data['name'],
        height=f'{convert_measurement(data["height"])} m',
        weight=f'{convert_measurement(data["weight"])} kg',
        moves=moves,
        stats=stats
    )


async def simulate_battle(pokemon1, pokemon2):
    while pokemon1.stats['hp'] > 0 and pokemon2.stats['hp'] > 0:
        # Pokemon 1 attacks Pokemon 2

        # Get random move from list of moves
        move1 = random.choice(pokemon1.moves)

        # Fetch additional data for move
        move1_data = await fetch_move_data(move1)

        # Simulate attack and calcuate damage
        damage1 = move1_data.power + (
            pokemon1.stats["attack"] - pokemon2.stats["defense"])

        # Update hp
        pokemon2.stats["hp"] -= max(0, damage1)

        # Check if Pokemon 2 failed
        if pokemon2.stats["hp"] <= 0:
            return f"{pokemon1.name} wins!"

        # Pokemon 2 attacks Pokemon 1

        # Get random move from list of moves
        move2 = random.choice(pokemon2.moves)

        # Fetch additional data for move
        move2_data = await fetch_move_data(move2)

        # Simulate attack and calculate damage
        damage2 = move2_data.power + (
            pokemon2.stats["attack"] - pokemon1.stats["defense"])

        # Update hp
        pokemon1.stats["hp"] -= max(0, damage2)

    return f"{pokemon2.name} wins!"
