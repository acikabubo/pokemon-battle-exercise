from fastapi import FastAPI
from app.api import battle


app = FastAPI(
    debug=False,
    title="Pokemon Battle",
    description="Pokemon Battle Description",
    version="1.0.0"
)

app.include_router(battle.router)
