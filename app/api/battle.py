from fastapi import APIRouter
from starlette.status import HTTP_200_OK
from fastapi import HTTPException
from app.utils import fetch_pokemon_data, simulate_battle
from app.models.request import BattleRequest


router = APIRouter()
path = '/battle'

@router.post(path, status_code=HTTP_200_OK)
async def start_battle(request: BattleRequest):
    try:
        pokemon1 = await fetch_pokemon_data(request.pokemon1)
        pokemon2 = await fetch_pokemon_data(request.pokemon2)

        winner = await simulate_battle(pokemon1, pokemon2)

        return {
            'winner': winner,
            'cards': {
                'pokemon1': pokemon1.card,
                'pokemon2': pokemon2.card
            }
        }

    except HTTPException:
        # Because FastAPI has build-in exception handlers for HTTPException
        # reraise the exception so FastAPI can handle it
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


