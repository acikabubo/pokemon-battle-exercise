from pydantic import BaseModel


class Pokemon(BaseModel):
    id_card: dict
    stats: dict

    def calculate_score(self):
        """
            Make sum of all stats values
        """
        return sum(self.stats.values())
