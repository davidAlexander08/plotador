from typing import Dict

class Configuracao:
    def __init__(self, sintese: str, argumento: str):
        self.sintese = sintese
        self.argumento = argumento

    @classmethod
    def from_dict(cls, d: Dict[str, str]):
        return cls(d["sintese"], d["argumento"])
    

class Meta:


    def __init__(self, dados):

        

        self.default_sts_cenarios_ending = ["FOR", "SF"]

        self.default_sts_SIN = ["COP_SIN_EST", "CTER_SIN_EST","EARPF_SIN_EST", "EVER_SIN_EST", "GHID_SIN_EST", "GTER_SIN_EST"]
        self.default_sts_SBM = ["CMO_SBM_EST", "EARPF_SBM_EST", "EVER_SBM_EST", "GHID_SBM_EST", "GTER_SBM_EST"]
        self.default_sts_REE = ["EARPF_REE_EST", "EVER_REE_EST", "GHID_REE_EST"]
        self.default_sts_UHE = ["GHID_UHE_EST", "QAFL_UHE_EST", "QDEF_UHE_EST", "QVER_UHE_EST", "QTUR_UHE_EST", "VARMF_UHE_EST"]
        self.default_sts_CEN = ["ENAA_SIN_SF", "ENAA_SBM_SF", "ENAA_REE_SF", "QINC_SIN_SF", "QINC_SBM_SF", "QINC_REE_SF", "QINC_UHE_SF"]

        self.mapa_sinteses = {
            "TODOS": self.default_sts_SIN + self.default_sts_SBM + self.default_sts_REE + self.default_sts_UHE,
            "OPER": self.default_sts_SIN + self.default_sts_SBM,
            "SIN": self.default_sts_SIN,
            "SBM": self.default_sts_SBM,
            "REE": self.default_sts_REE,
            "UHE": self.default_sts_UHE,
            "CEN": self.defaut_sts_CEN
        }

        self.lista_submercados = ["SUDESTE", "NORDESTE", "NORTE", "SUL"]
        self.lista_rees = ['BMONTE', 'IGUACU', 'ITAIPU', 'MADEIRA', 'MAN-AP', 'NORDESTE', 'NORTE', 'PARANA', 'PRNPANEMA', 'SUDESTE', 'SUL', 'TPIRES']
        self.lista_usinas_principais = ["NOVA PONTE", "EMBORCACAO", "SAO SIMAO", "FURNAS", "MARIMBONDO", "A. VERMELHA", "I. SOLTEIRA", "JUPIA", "P. PRIMAVERA",
                                        "A.A. LAYDNER", "G.B. MUNHOZ", "MACHADINHO", "TRES MARIAS", "SOBRADINHO", "ITAPARICA", "SERRA MESA", "TUCURUI"]
        
        self.mapa_argumentos = {
            "TODOS": self.lista_submercados+self.lista_rees+self.lista_usinas_principais,
            "SBM": self.lista_submercados,
            "REE": self.lista_rees,
            "UHE": self.lista_usinas_principais
        }