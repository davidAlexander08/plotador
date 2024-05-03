from typing import Dict
from apps.model.unidade import UnidadeSintese
from apps.graficos.graficos import Graficos
from apps.indicadores.indicadores_cenarios import IndicadoresCenarios
from apps.model.caso import Caso
from apps.model.sintese import Sintese
from apps.model.argumento import Argumento
import plotly.graph_objects as go
import pandas as pd
from scipy import stats
from apps.interface.metaData import MetaData
from apps.model.conjuntoUnidade import ConjuntoUnidadeSintese
from inewave.newave import Confhd
import os
import json

class Cascatador(MetaData):
    def __init__(self, data):
        MetaData.__init__(self)
        self.estudo = data.estudo
        self.casos = data.casos
        self.indicadores_cenarios = IndicadoresCenarios(self.casos)
        self.graficos = Graficos(self.casos)
        diretorio_saida = f"resultados/{self.estudo}/cascatador"
        os.makedirs(diretorio_saida, exist_ok=True)
        for c in self.casos:
            arquivo_confhd = c.caminho+"/confhd.dat"
            d_usi = Confhd.read(arquivo_confhd).usinas
            print(d_usi)
            mapa_codigo_nos = {}   
            for index, row in d_usi.iterrows():
                no = Node()
                no.pais =           []
                no.filhos =         []
                no.codigo =         row["codigo_usina"]
                no.nome =           row["nome_usina"]
                no.posto =          row["posto"]
                no.ree =            row["ree"] 
                no.nivel =          None
                mapa_codigo_nos[no.codigo] = no

            #usinas_mar = d_usi.loc[d_usi["codigo_usina_jusante"] == 0]
            lista_no_aux = list(mapa_codigo_nos.keys())
            print(lista_no_aux)
            for cod_usi in lista_no_aux:
                lista_nos_pais = []
                lista_nos_filhos = []
                pais = d_usi.loc[d_usi["codigo_usina_jusante"] == cod_usi]
                for index, row in pais.iterrows():
                    no_pai = mapa_codigo_nos[row["codigo_usina"]]
                    lista_nos_pais.append(no_pai)

                codigo_filho = d_usi.loc[d_usi["codigo_usina"] == cod_usi]["codigo_usina_jusante"].iloc[0]
                no_filho = mapa_codigo_nos[codigo_filho] if codigo_filho != 0 else None
                lista_nos_filhos.append(no_filho)
                lista_no_aux.remove(cod_usi)
                no = mapa_codigo_nos[cod_usi]
                no.pais = lista_nos_pais
                no.filhos = lista_nos_filhos

            for cod in mapa_codigo_nos:
                no = mapa_codigo_nos[cod]
                print("usi: ", cod)
                for pai in no.pais:
                    print("pai: ", pai, " cod: ", pai.codigo)
                for filho in no.filhos:
                    if( filho is not None):
                        print("filho: ", filho, " cod: ", filho.codigo)
                    else:
                        print("MAR")

            exit(1)
            print(lista_Nos)
            exit(1)
            usinas_mar = d_usi.loc[d_usi["codigo_usina_jusante"] == 0]
            print(usinas_mar)
        print(d_usi)
        exit(1)

class Node():
    def __init__(self):
        self.pais = []
        self.filhos = any
        self.codigo = None 
        self.nome = None 
        self.posto = None
        self.codigo_jusante = None 
        self.ree = None 
        self.nivel = None