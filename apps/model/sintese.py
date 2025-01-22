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
            "SBM": "codigo_submercado",
            "REE": "codigo_ree",
            "UHE": "codigo_usina",
            "SIN": None
        }
        
        if(sts.split("-")[0] == "VIOLMIN"):
            self.violMin = True
            sts = sts.split("-")[1]
        else:
            self.violMin = False
        self.sintese = sts  
        self.grandeza = sts.split("_")[0]
        self.espacial = sts.split("_")[1] if len(sts.split("_")) > 1 else None
        self.filtro = self.retornaFiltro(sts) if len(sts.split("_")) > 1 else ""


    @classmethod
    def from_dict(cls, d: Dict[str, str]):
        return cls(d["sintese"])
