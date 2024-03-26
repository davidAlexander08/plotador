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

        print(self.mapa_argumentos)

        with open(arquivo_json, "r") as f:
            dados = json.load(f)
        self.estudo = dados["estudo"]
        self.nome_caso_referencia = dados["nome_caso_referencia"]
        self.casos = [Caso.from_dict(d) for d in dados["casos"]]
        
        sts = [Sintese.from_dict(d) for d in dados["sinteses"]]
        argum = [Argumento.from_dict(d) for d in dados["argumentos"]]

        self.config = [Configuracao.from_dict(d) for d in dados["configuracao"]][0]

        config_sintese = self.config.sintese.replace(" ", "")
        config_arg = self.config.argumento.replace(" ", "")

        if(config_sintese == ""):
            self.sinteses = sts
        else:
            lista = []
            lista_strings = self.mapa_sinteses[config_sintese]
            for elem in lista_strings:
                lista.append(Sintese(elem))
            self.sinteses = lista

        if(config_arg == ""):
            self.args = argum
        else:
            lista = []
            lista_strings = self.mapa_argumentos[config_arg]
            for elem in lista_strings:
                lista.append(Argumento(elem[0], elem[1]))
            self.sinteses = lista

