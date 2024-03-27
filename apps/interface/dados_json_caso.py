from apps.model.caso import Caso
from apps.model.sintese import Sintese
from apps.model.argumento import Argumento
from apps.model.conjuntoCasos import ConjuntoCasos
from apps.interface.metaData import MetaData
from apps.model.configuracao import Configuracao
from apps.model.limites import Limites
import os
import json
from typing import Dict




class Dados_json_caso(MetaData):

    def __init__(self, arquivo_json):
        MetaData.__init__(self)

        with open(arquivo_json, "r") as f:
            dados = json.load(f)
        self.estudo = dados["estudo"]
        self.nome_caso_referencia = dados["nome_caso_referencia"] if "nome_caso_referencia" in dados else ""
        
        if("casos" in dados):
            self.casos = [Caso.from_dict(d) for d in dados["casos"]]
        elif("conjuntos" in dados):
            self.conjuntoCasos = [ConjuntoCasos.from_dict(d) for d in dados["conjuntos"]]
        else:
            print("ERRO: CASOS OU CONJUNTOS DECLARADOS COM ERRO NO JSON")
        
        sts = [Sintese.from_dict(d) for d in dados["sinteses"]] if "sinteses" in dados else ""
        argum = [Argumento.from_dict(d) for d in dados["argumentos"]] if "argumentos" in dados else ""

        if(("limites") in dados):
            lim = [Limites.from_dict(d) for d in dados["limites"]][0]
            self.lim_sup = True if lim.superior.replace(" ", "") == "True" else False
            self.lim_inf = True if lim.inferior.replace(" ", "") == "True" else False
            
        else:
            self.lim_sup = False
            self.lim_inf = False
            
        print("lim_sup: ", lim_sup)
        print("lim_inf: ", lim_inf)

        if(("configuracao") in dados):
            config = [Configuracao.from_dict(d) for d in dados["configuracao"]][0]
            config_sintese = config.sintese.replace(" ", "")
            config_arg = config.argumento.replace(" ", "")
        else:
            config_sintese = ""
            config_arg = ""

        self.sinteses = sts if config_sintese == "" else self.mapa_sinteses[config_sintese]
        self.args = argum if config_arg == "" else self.mapa_argumentos[config_arg]


        if(config_sintese == "" and sts == ""):
            self.sinteses = self.mapa_sinteses["TODOS"]

        if(config_arg == "" and argum == ""):
            self.args = self.mapa_argumentos["TODOS"]