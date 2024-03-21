from typing import Dict


class SubmercadoAvalicao:
    """
    Classe base que representa um submercado do estudo
    que será utilizado para o cálculo de indicadores
    e para geração de gráficos.
    """

    def __init__(self, nome: str):
        self.nome = nome  

    @classmethod
    def from_dict(cls, d: Dict[str, str]):
        return cls(d["nome"])
