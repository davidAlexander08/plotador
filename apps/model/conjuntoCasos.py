from typing import Dict
from apps.model.caso import Caso

class ConjuntoCasos:
    """
    Classe base que representa um caso de estudo
    que será utilizado para o cálculo de indicadores da
    calibração do CVaR e para geração de gráficos.
    """

    def __init__(self, nome: str, cor: str, dados):
        self.nome = nome
        self.cor = cor
        #print(dados)
        self.casos = [Caso.from_dict(d) for d in dados]

    @classmethod
    def from_dict(cls, d: Dict[str, str]):
        return cls(d["nome_conj"], d["cor_conj"], d["casos"])
