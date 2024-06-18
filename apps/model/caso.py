from typing import Dict


class Caso:
    """
    Classe base que representa um caso de estudo
    que será utilizado para o cálculo de indicadores da
    calibração do CVaR e para geração de gráficos.
    """

    def __init__(self, nome: str, caminho: str, cor: str, marcador: str):
        self.nome = nome
        self.caminho = caminho
        self.cor = cor
        self.marcador = marcador 

    @classmethod
    def from_dict(cls, d: Dict[str, str]):
        marcador = d["marcador"] if "marcador" in d else "diamond"
        return cls(d["nome"], d["caminho"], d["cor"], marcador)
