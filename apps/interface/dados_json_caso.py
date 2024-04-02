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
        self.tamanho_texto = int(dados["tamanho_texto"]) if "tamanho_texto" in dados else 11

        if("casos" in dados):
            self.casos = [Caso.from_dict(d) for d in dados["casos"]]
        elif("conjuntos" in dados):
            self.conjuntoCasos = [ConjuntoCasos.from_dict(d) for d in dados["conjuntos"]]
        else:
            print("ERRO: CASOS OU CONJUNTOS DECLARADOS COM ERRO NO JSON")
        


        if(("limites") in dados):
            lim = dados["limites"] if "limites" in dados else ""
            self.limites = True if lim.replace(" ", "") == "True" else False
            
        else:
            self.limites = False

        grupo_parquet = dados["grupo_parquet"] if "grupo_parquet" in dados else ""


        sts = [Sintese.from_dict(d) for d in dados["parquets"]] if "parquets" in dados else ""
        self.sinteses = self.mapa_sinteses[grupo_parquet.replace(" ", "")] if sts == "" else sts


        argum = [Argumento.from_dict(d) for d in dados["argumentos"]] if "argumentos" in dados else ""
        caminho_externo = dados["arquivo_externo"] if "arquivo_externo" in dados else None
        if(caminho_externo is not None):
            with open(caminho_externo, "r") as d:
                dados_externo = json.load(d)
                argum = [Argumento.from_dict(d) for d in dados_externo["argumentos"]] if "argumentos" in dados_externo else ""
        
        self.args = self.mapa_argumentos[grupo_parquet.replace(" ", "")] if argum == "" else argum


        if(grupo_parquet == "" and sts == ""):
            self.sinteses = self.mapa_sinteses["TODOS"]
        
        if(grupo_parquet == "" and argum == ""):
            self.args = self.mapa_argumentos["TODOS"]
