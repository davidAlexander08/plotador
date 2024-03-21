from typing import Dict


class Argumento:
    """
    Classe base que representa um argumento do estudo
    que será utilizado para o cálculo de indicadores
    e para geração de gráficos.
    """

    def __init__(self, nome: str):
        self.nome = nome  

    @classmethod
    def from_dict(cls, d: Dict[str, str]):
        print(d.key())
        return cls(d["nome"])
