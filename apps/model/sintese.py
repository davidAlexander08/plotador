from typing import Dict


class SinteseAvalicao:
    """
    Classe base que representa uma sintese do estudo
    que será utilizado para o cálculo de indicadores
    e para geração de gráficos.
    """

    def __init__(self, nome: str):
        self.nome = nome  

    @classmethod
    def from_dict(cls, d: Dict[str, str]):
        return cls(d["nome"])
