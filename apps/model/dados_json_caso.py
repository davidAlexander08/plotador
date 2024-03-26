from apps.model.caso import Caso
from apps.model.sintese import Sintese
from apps.model.argumento import Argumento
from apps.model.conjuntoCasos import ConjuntoCasos
import os
import json
from typing import Dict

class Configuracao:
    def __init__(self, sintese: str, argumento: str):
        self.sintese = sintese
        self.argumento = argumento

    @classmethod
    def from_dict(cls, d: Dict[str, str]):
        return cls(d["sintese"], d["argumento"])


class Dados_json_caso:

    def __init__(self, arquivo_json):

        self.default_sts_cenarios_ending = ["FOR", "SF"]

        self.default_sts_SIN = [Sintese("COP_SIN_EST"), Sintese("CTER_SIN_EST"),Sintese("EARPF_SIN_EST"), Sintese("EVER_SIN_EST"), Sintese("GHID_SIN_EST"), Sintese("GTER_SIN_EST")]
        self.default_sts_SBM = [Sintese("CMO_SBM_EST"), Sintese("EARPF_SBM_EST"), Sintese("EVER_SBM_EST"), Sintese("GHID_SBM_EST"), Sintese("GTER_SBM_EST")]
        self.default_sts_REE = [Sintese("EARPF_REE_EST"), Sintese("EVER_REE_EST"), Sintese("GHID_REE_EST")]
        self.default_sts_UHE = [Sintese("GHID_UHE_EST"), Sintese("QAFL_UHE_EST"), Sintese("QDEF_UHE_EST"), Sintese("QVER_UHE_EST"), Sintese("QTUR_UHE_EST"), Sintese("VARMF_UHE_EST")]
        self.default_sts_CEN = [Sintese("ENAA_SIN_SF"), Sintese("ENAA_SBM_SF"), Sintese("ENAA_REE_SF"), Sintese("QINC_SIN_SF"), Sintese("QINC_SBM_SF"), Sintese("QINC_REE_SF"), Sintese("QINC_UHE_SF")]

        self.mapa_sinteses = {
            "TODOS": self.default_sts_SIN + self.default_sts_SBM + self.default_sts_REE + self.default_sts_UHE,
            "OPER": self.default_sts_SIN + self.default_sts_SBM,
            "SIN": self.default_sts_SIN,
            "SBM": self.default_sts_SBM,
            "REE": self.default_sts_REE,
            "UHE": self.default_sts_UHE,
            "CEN": self.default_sts_CEN
        }

        chave_sbm = "submercado"
        self.lista_submercados = [Argumento("SUDESTE", chave_sbm), Argumento("NORDESTE",chave_sbm), Argumento("NORTE", chave_sbm), Argumento("SUL", chave_sbm)]
        chave_ree = "ree"
        self.lista_rees = [Argumento('BMONTE', chave_ree),
                            Argumento('IGUACU', chave_ree),
                            Argumento('ITAIPU', chave_ree),
                            Argumento('MADEIRA', chave_ree),
                            Argumento('MAN-AP', chave_ree),
                            Argumento('NORDESTE', chave_ree),
                            Argumento('NORTE', chave_ree),
                            Argumento('PARANA', chave_ree),
                            Argumento('PRNPANEMA', chave_ree),
                            Argumento('SUDESTE', chave_ree),
                            Argumento('SUL', chave_ree),
                            Argumento('TPIRES', chave_ree)]
        chave_usina = "usina"
        self.lista_usinas_principais = [Argumento("NOVA PONTE", chave_usina),
                                        Argumento("EMBORCACAO", chave_usina),
                                        Argumento("SAO SIMAO", chave_usina),
                                        Argumento("FURNAS", chave_usina),
                                        Argumento("MARIMBONDO", chave_usina),
                                        Argumento("A. VERMELHA", chave_usina),
                                        Argumento("I. SOLTEIRA", chave_usina),
                                        Argumento("JUPIA", chave_usina),
                                        Argumento("P. PRIMAVERA",chave_usina),
                                        Argumento("A.A. LAYDNER", chave_usina),
                                        Argumento("G.B. MUNHOZ", chave_usina),
                                        Argumento("MACHADINHO", chave_usina),
                                        Argumento("TRES MARIAS", chave_usina),
                                        Argumento("SOBRADINHO", chave_usina),
                                        Argumento("ITAPARICA", chave_usina),
                                        Argumento("SERRA MESA", chave_usina),
                                        Argumento("TUCURUI",    chave_usina  ),
                                        ]
        
        self.mapa_argumentos = {
            "TODOS": self.lista_submercados+self.lista_rees+self.lista_usinas_principais,
            "SBM": self.lista_submercados,
            "REE": self.lista_rees,
            "UHE": self.lista_usinas_principais
        }

        with open(arquivo_json, "r") as f:
            dados = json.load(f)
        self.estudo = dados["estudo"]
        self.nome_caso_referencia = dados["nome_caso_referencia"]
        self.casos = [Caso.from_dict(d) for d in dados["casos"]]
        
        sts = [Sintese.from_dict(d) for d in dados["sinteses"]]
        argum = [Argumento.from_dict(d) for d in dados["argumentos"]]

        config = [Configuracao.from_dict(d) for d in dados["configuracao"]][0]
        config_sintese = self.config.sintese.replace(" ", "")
        config_arg = self.config.argumento.replace(" ", "")
        if(config_sintese == ""):
            self.sinteses = sts
        else:
            self.sinteses = self.mapa_sinteses[config_sintese]

        if(config_arg == ""):
            self.args = argum
        else:
            self.sinteses = self.mapa_argumentos[config_arg]

