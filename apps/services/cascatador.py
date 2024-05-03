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
            usinas_mar = d_usi.loc[d_usi["codigo_usina_jusante"] == 0]
            print(usinas_mar)
            exit(1)
            first = nome_usinas[0]
            mapa_cascatas = {}
            while True:
                d_usi["codigo_usina_jusante"] == 
                
            
            print(nome_usinas)

        print(d_usi)
        exit(1)

        df_vazoes = pd.DataFrame()
        if(u_fw.filtroArgumento is None):
            if(df_vazoes.empty):
                lista_df = []
                for c in self.casos:
                    arquivo_vazoes = c.caminho+"/vazoes.dat"
                    print(arquivo_vazoes)
                    df = self.le_vazoes(arquivo_vazoes)
                    df["caso"] = c.nome
                    lista_df.append(df)
                df_vazoes = pd.concat(lista_df)
                print(df_vazoes)

