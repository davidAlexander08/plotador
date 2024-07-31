from typing import Dict


class Caso:
    """
    Classe base que representa um caso de estudo
    que será utilizado para o cálculo de indicadores da
    calibração do CVaR e para geração de gráficos.
    """

    def __init__(self, nome: str, caminho: str, cor: str, marcador: str, modelo:str, dash:str, tipo:str):
        self.nome = nome
        self.caminho = caminho
        self.cor = cor
        self.marcador = marcador
        self.modelo = modelo
        self.dash = dash
        self.tipo = tipo

    @classmethod
    def from_dict(cls, d: Dict[str, str]):
        marcador = d["marcador"] if "marcador" in d else "diamond"
        modelo = d["modelo"] if "modelo" in d else "NEWAVE"
        return cls(d["nome"], d["caminho"], d["cor"], marcador, modelo, None, "mean")
