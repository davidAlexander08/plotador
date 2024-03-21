from typing import Dict


class Sintese:
    """
    Classe base que representa uma sintese do estudo
    que será utilizado para o cálculo de indicadores
    e para geração de gráficos.
    """

    def __init__(self, sintese: str):
        self.sintese = sintese  
        self.filtro = self.retornaFiltro(sintese)

        self.mapa_filtro = {
            "SBM": "submercado",
            "REE": "ree",
            "UHE": "usina",
            "SIN": None
        }
    def retornaFiltro(self, sintese):
        espacial = sintese.split("_")[1]
        return self.mapa_filtro[espacial]

    @classmethod
    def from_dict(cls, d: Dict[str, str]):
        return cls(d["sintese"])
