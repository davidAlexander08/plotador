from typing import Dict

class Limites:
    def __init__(self, superior: str, inferior: str):
        self.superior = superior
        self.inferior = inferior

    @classmethod
    def from_dict(cls, d: Dict[str, str]):
        return cls(d["superior"], d["inferior"])