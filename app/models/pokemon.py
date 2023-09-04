from typing import List
from pydantic import BaseModel


class Move(BaseModel):
    name: str
    power: int


class Pokemon(BaseModel):
    name: str
    height: str
    weight: str
    moves: List[str]
    stats: dict

    @property
    def card(self):
        return {
            "name": self.name,
            "height": self.height,
            "weight": self.weight
        }


