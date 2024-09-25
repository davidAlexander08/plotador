from typing import Dict


class Sintese:
    """
    Classe base que representa uma sintese do estudo
    que será utilizado para o cálculo de indicadores
    e para geração de gráficos.
    """
    def retornaFiltro(self, sts): 
        espacial = sts.split("_")[1]
        return self.__mapa_filtro[espacial]
         
    def __init__(self, sts: str):
        self.__mapa_filtro = {
            "SBM": "submercado",
            "REE": "ree",
            "UHE": "usina",
            "BCA": "bacia",
            "SIN": None
        }
        self.sintese = sts  
        self.filtro = self.retornaFiltro(sts) if len(sts.split("_")) > 1 else ""


    @classmethod
    def from_dict(cls, d: Dict[str, str]):
        return cls(d["sintese"])
