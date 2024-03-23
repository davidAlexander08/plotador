from typing import List
from os.path import join
from datetime import datetime
from calendar import monthrange
import numpy as np
import pandas as pd
from inewave.newave import Dger
from apps.utils.log import Log
import os.path
from apps.model.caso import Caso
from apps.indicadores.indicadores_temporais import IndicadoresTemporais
from apps.indicadores.eco_indicadores import EcoIndicadores
import warnings

class IndicadoresMedios:
    """indicadores.df_custos_incrementais.to_csv
    Calcula os indicadores que são utilizados nas visualizações
    dos paretos para a escolha dos pares de CVaR candidatos
    para recalibração.
    """

    DIR_SINTESE = "sintese"

    def __init__(
        self, casos: List[Caso], nome_caso_referencia: str    ):
        warnings.simplefilter(action='ignore')
        
        self.casos = casos
        self.nome_caso_referencia = nome_caso_referencia
        self.indicadores_temporais = IndicadoresTemporais(casos)
        self.eco_indicadores = EcoIndicadores(casos)
    
    def retorna_mapa_media_parquet(self, mapa):
        dict = {}
        for c in self.casos:
            valor = mapa[c]["valor"].mean()
            df = pd.DataFrame()
            df.at[c.nome, "valor"] = valor
            df.index = df.index.rename('caso')
            df = df.reset_index(drop=False)
            dict[c] = df
        return dict


    def retorna_df_concatenado(self,sintese, coluna = None, argumento_filtro = None):
        return pd.concat(self.retorna_mapaDF_cenario_medio(sintese, coluna, argumento_filtro))
            
            
    def retorna_mapaDF_cenario_medio(self,sintese, coluna = None, argumento_filtro = None):
        if( (coluna is None) & (argumento_filtro is None) ):
            return self.retorna_mapa_media_parquet(self.indicadores_temporais.retorna_mapaDF_cenario_medio(sintese))
        else:
            mapa = self.indicadores_temporais.retorna_mapaDF_cenario_medio(sintese)
            for c in self.casos: mapa[c] = mapa[c].loc[mapa[c][coluna] == argumento_filtro]
            return self.retorna_mapa_media_parquet(mapa)           

    
    def retorna_df_std_concatenado(self,sintese, coluna = None, argumento_filtro = None):
        MAP = self.retorna_mapaDF_std_cenarios(sintese, coluna, argumento_filtro)
        print(MAP)
        concat = pd.concat(self.retorna_mapa_std_parquet(MAP))
        print("concat: ", concat)
        return concat
            
    def retorna_mapaDF_std_cenarios(self, sintese, coluna = None, argumento_filtro = None):
        mapa = {}
        mapa = self.eco_indicadores.retornaMapaDF(sintese)
        if( (coluna is not None) & (argumento_filtro is not None) ):
            for c in self.casos: mapa[c] = mapa[c].loc[mapa[c][coluna] == argumento_filtro]
        for c in self.casos:
            mapa[c] =  mapa[c].loc[:, mapa[c].columns!='dataInicio']
            mapa[c] =  mapa[c].loc[:, mapa[c].columns!='dataFim']
            mapa[c] =  mapa[c].loc[:, mapa[c].columns!='estagio']
            mapa[c] =  mapa[c].loc[:, mapa[c].columns!='caso']
            mapa[c] =  mapa[c][mapa[c][['cenario']].apply(lambda x: x[0].isdigit(), axis=1)]
            mapa[c] =  mapa[c].groupby(["cenario"]).mean()
            mapa[c]["caso"] = c.nome
        return mapa


    def retorna_mapa_std_parquet(self, mapa):
        dict = {}
        for c in self.casos:
            print("len(mapa[c][valor].tolist(): ", len(mapa[c]["valor"].tolist()))
            valor =  (1.96*mapa[c]["valor"].std()/(np.sqrt(len(mapa[c]["valor"].tolist()))))
            #valor =  mapa[c]["valor"].std()
            print("valor: ", valor)
            df = pd.DataFrame()
            df.at[c.nome, "valor"] = valor
            df.index = df.index.rename('caso')
            df = df.reset_index(drop=False)
            dict[c] = df
        print(dict)
        return dict


    def retorna_DF_std_incremental_percentual(self, sintese, coluna = None, argumento_filtro = None, dropar = True):
        mapa = self.retorna_mapaDF_cenario_medio(sintese, coluna, argumento_filtro)
        df = self.retorna_DF_incremental(mapa, dropar)
        df["valor"] = df["valor"]*0
        return df
        
        
    def retorna_DF_cenario_medio_incremental_percentual(self, sintese, coluna = None, argumento_filtro = None, dropar = True):
        mapa = self.retorna_mapaDF_cenario_medio(sintese, coluna, argumento_filtro)
        return self.retorna_DF_incremental(mapa, dropar)

    def retorna_DF_incremental(self, mapa, dropar):
        df_mapa = pd.concat(mapa)
        df_mapa["valor" ] = ( (df_mapa["valor"].round(2)/df_mapa.loc[(df_mapa["caso"] == self.nome_caso_referencia)]["valor"].round(2).iloc[0]) - 1)*100
        if(dropar is True):
            df_mapa = df_mapa.drop(df_mapa[df_mapa['caso'] == self.nome_caso_referencia].index)
        return df_mapa
