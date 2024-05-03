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
            lista_Nos = []
            for index, row in d_usi.iterrows():
                no = Node()
                pais =              []
                no.pais =           []
                no.filhos =         None
                no.codigo =         row["codigo_usina"]
                no.nome =           row["nome_usina"]
                no.posto =          row["posto"]
                no.codigo_jusante = row["codigo_usina_jusante"] 
                no.ree =            row["ree"] 
                lista_Nos.append(no)
            print(lista_Nos)
            exit(1)
            usinas_mar = d_usi.loc[d_usi["codigo_usina_jusante"] == 0]
            print(usinas_mar)
        print(d_usi)
        exit(1)

class Node():
    def __init__(self):
        self.pais = []
        self.filhos = []
        self.codigo = None 
        self.nome = None 
        self.posto = None
        self.codigo_jusante = None 
        self.ree = None 