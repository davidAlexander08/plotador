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
from apps.model.unidade import UnidadeSintese
import warnings

class IndicadoresMedios(EcoIndicadores):
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
        EcoIndicadores.__init__(self, casos)
    
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


    def retorna_df_concatenado(self, unidade):
        return pd.concat(self.retorna_mapaDF_cenario_medio(unidade))
            
            
    def retorna_mapaDF_cenario_medio(self, unidade):
        if( (unidade.fitroColuna is None) & (unidade.filtroArgumento is None) ):
            return self.retorna_mapa_media_parquet(self.indicadores_temporais.retorna_mapaDF_cenario_medio_temporal(unidade))
        else:
            mapa = self.indicadores_temporais.retorna_mapaDF_cenario_medio_temporal(unidade)
            for c in self.casos: mapa[c] = mapa[c].loc[mapa[c][unidade.fitroColuna] == unidade.filtroArgumento]
            return self.retorna_mapa_media_parquet(mapa)           

    
    def retorna_df_std_concatenado(self, unidade):
        MAP = self.retorna_mapaDF_std_cenarios(unidade)
        print(MAP)
        concat = pd.concat(self.retorna_mapa_std_parquet(MAP))
        print("concat: ", concat)
        return concat
            
    def retorna_mapaDF_std_cenarios(self, unidade):
        mapa = {}
        mapa = self.retornaMapaDF(unidade)
        if( (unidade.fitroColuna is not None) & (unidade.filtroArgumento is not None) ):
            for c in self.casos: mapa[c] = mapa[c].loc[mapa[c][unidade.fitroColuna] == unidade.filtroArgumento]
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


    def retorna_DF_std_incremental_percentual(self, unidade, dropar = True):
        mapa = self.retorna_mapaDF_cenario_medio(unidade)
        df = self.retorna_DF_incremental(mapa, dropar)
        df["valor"] = df["valor"]*0
        return df
        
        
    def retorna_DF_cenario_medio_incremental_percentual(self, unidade, dropar = True):
        mapa = self.retorna_mapaDF_cenario_medio(unidade)
        return self.retorna_DF_incremental(mapa, dropar)

    def retorna_DF_incremental(self, mapa, dropar):
        df_mapa = pd.concat(mapa)
        df_mapa["valor" ] = ( (df_mapa["valor"].round(2)/df_mapa.loc[(df_mapa["caso"] == self.nome_caso_referencia)]["valor"].round(2).iloc[0]) - 1)*100
        if(dropar is True):
            df_mapa = df_mapa.drop(df_mapa[df_mapa['caso'] == self.nome_caso_referencia].index)
        return df_mapa
