from fastapi import APIRouter
from starlette.status import HTTP_200_OK
from fastapi import HTTPException
from app.utils import fetch_pokemon_data
from app.models.request import BattleRequest


router = APIRouter()
path = '/battle'

@router.post(path, status_code=HTTP_200_OK)
async def start_battle(request: BattleRequest):
    try:
        pokemon1 = await fetch_pokemon_data(request.pokemon1)
        pokemon2 = await fetch_pokemon_data(request.pokemon2)

        if not pokemon1 or not pokemon2:
            raise HTTPException(
                status_code=404,
                detail='One or both Pokemon not found'
            )

        score1 = pokemon1.calculate_score()
        score2 = pokemon2.calculate_score()

        winner = (
            pokemon1.id_card['name']
            if score1 > score2 else
            pokemon2.id_card['name']
        )

        return {
            'winner': winner,
            'pokemon1': pokemon1.id_card,
            'pokemon2': pokemon2.id_card
        }

    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


