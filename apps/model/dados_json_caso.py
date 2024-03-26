from apps.model.caso import Caso
from apps.model.sintese import Sintese
from apps.model.argumento import Argumento
from apps.model.conjuntoCasos import ConjuntoCasos
from apps.services.meta_data import Configuracao
import os
import json
from typing import Dict
class Dados_json_caso:

    def __init__(self, arquivo_json):

        with open(arquivo_json, "r") as f:
            dados = json.load(f)
        self.estudo = dados["estudo"]
        self.nome_caso_referencia = dados["nome_caso_referencia"]
        self.casos = [Caso.from_dict(d) for d in dados["casos"]]
        self.sinteses = [Sintese.from_dict(d) for d in dados["sinteses"]]
        self.args = [Argumento.from_dict(d) for d in dados["argumentos"]]
        b = dados["configuracao"]
        print(b)
        print(b["argumento"])
        #self.config = Configuracao(dados["configuracao"]["sintese"])
        #[Configuracao.from_dict(d) for d in dados["configuracao"]]
        print(self.config.sintese)

