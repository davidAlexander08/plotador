from apps.model.caso import Caso
from apps.model.sintese import Sintese
from apps.model.argumento import Argumento
from apps.model.conjuntoCasos import ConjuntoCasos
from apps.model.metaData import MetaData
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


class Dados_json_caso(MetaData):

    def __init__(self, arquivo_json):
        MetaData.__init__(self)

        with open(arquivo_json, "r") as f:
            dados = json.load(f)
        self.estudo = dados["estudo"]
        if("nome_caso_referencia" in dados):
            self.nome_caso_referencia = dados["nome_caso_referencia"]
        else:
            self.nome_caso_referencia = ""
        
        if("casos" in dados):
            self.casos = [Caso.from_dict(d) for d in dados["casos"]]
        elif("conjuntos" in dados):
            self.conjuntoCasos = [ConjuntoCasos.from_dict(d) for d in dados["conjuntos"]]
        else:
            print("ERRO: CASOS OU CONJUNTOS DECLARADOS COM ERRO NO JSON")
        
        if("sinteses" in dados):
            sts = [Sintese.from_dict(d) for d in dados["sinteses"]]
        else:
            sts = ""
        if("argumentos" in dados):
            argum = [Argumento.from_dict(d) for d in dados["argumentos"]]
        else:
            argum = ""

        if(("configuracao") in dados):
            config = [Configuracao.from_dict(d) for d in dados["configuracao"]][0]
            config_sintese = config.sintese.replace(" ", "")
            config_arg = config.argumento.replace(" ", "")
        else:
            config_sintese = ""
            config_arg = ""

        if(config_sintese == ""):
            self.sinteses = sts
        else:
            self.sinteses = self.mapa_sinteses[config_sintese]

        if(config_arg == ""):
            self.args = argum
        else:
            self.args = self.mapa_argumentos[config_arg]

        if(config_sintese == "" and sts == ""):
            self.sinteses = self.mapa_sinteses["TODOS"]

        if(config_arg == "" and argum == ""):
            self.args = self.mapa_argumentos["TODOS"]