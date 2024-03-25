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
from apps.model.unidade import UnidadeSintese
import warnings

class IndicadoresAnuais(IndicadoresTemporais):
    """indicadores.df_custos_incrementais.to_csv
    Calcula os indicadores que são utilizados nas visualizações
    dos paretos para a escolha dos pares de CVaR candidatos
    para recalibração.
    """

    DIR_SINTESE = "sintese"

    def __init__(
        self, casos: List[Caso], nome_caso_referencia: str
    ):
        warnings.simplefilter(action='ignore')
        
        self.casos = casos
        self.nome_caso_referencia = nome_caso_referencia
        IndicadoresTemporais.__init__(self, casos)


    def retorna_mapa_media_anual_parquet(self, mapa):
        dict = {}
        for c in self.casos:
            df = mapa[c]
            agrupamento = "mean"
            df_anual = df.groupby(df["dataInicio"].dt.year)["valor"].agg([agrupamento]).reset_index(drop=False)
            df_anual.columns = df_anual.columns.str.replace('dataInicio', 'anos')  
            df_anual.columns = df_anual.columns.str.replace(agrupamento, 'valor')  
            df_anual["caso"] = c.nome
            dict[c] = df_anual
        return dict

    def retorna_df_concatenado(self, unidade):
        return pd.concat(self.retorna_mapaDF_cenario_anual_medio(unidade))
        
    def retorna_df_concatenado_acumulado(self, unidade):
        return pd.concat(self.retorna_mapa_media_df_anual_acumulado(self.retorna_mapaDF_cenario_anual_medio(unidade)) )

    def retorna_mapaDF_cenario_anual_medio(self, unidade):
        mapa_temporal = self.retorna_mapaDF_cenario_medio_temporal(unidade)
        mapa_anual = {}
        if( (unidade.fitroColuna is None) & (unidade.filtroArgumento is None) ):
            mapa_anual = self.retorna_mapa_media_anual_parquet(mapa_temporal) 
        else:
            for c in self.casos: mapa_temporal[c] = mapa_temporal[c].loc[mapa_temporal[c][unidade.fitroColuna] == unidade.filtroArgumento]
            mapa_anual = self.retorna_mapa_media_anual_parquet(mapa_temporal) 
        return mapa_anual


    def retorna_mapa_media_df_anual_acumulado(self, mapa):
        dict = {}
        for c in self.casos:
            df = mapa[c]
            anos = set(df["anos"].tolist())
            listaDF = []
            df_primeiro = df.loc[df["anos"] == min(anos)]
            df_outros = df.loc[df["anos"] != min(anos)]
            df_temp = pd.DataFrame()
            df_temp.at[0, "valor"] = df_outros["valor"].mean()
            anoInicial = df_outros["anos"].iloc[0]
            anoFinal = df_outros["anos"].iloc[-1]
            df_temp.at[0, "anos"] = str(anoInicial)+"-"+str(anoFinal)
            df_primeiro["anos"] = df_primeiro["anos"].astype(str)
            listaDF.append(df_primeiro)
            listaDF.append(df_temp)
            df_anual_primeiro_ano_outros_anos = pd.concat(listaDF)
            df_anual_primeiro_ano_outros_anos = df_anual_primeiro_ano_outros_anos.reset_index(drop = True)
            df_anual_primeiro_ano_outros_anos["caso"] = c.nome
            dict[c] = df_anual_primeiro_ano_outros_anos
        return dict

    def retorna_DF_cenario_anual_acumulado_medio_incremental_percentual(self, unidade):
        mapa_anual = self.retorna_mapa_media_df_anual_acumulado(self.retorna_mapaDF_cenario_anual_medio(unidade))
        return self.retorna_DF_incremental(mapa_anual)

    def retorna_DF_cenario_anual_medio_incremental_percentual(self, unidade):
        mapa_anual = self.retorna_mapaDF_cenario_anual_medio(unidade)
        return self.retorna_DF_incremental(mapa_anual)

    def retorna_DF_incremental(self, mapa_anual):
        df_anos = pd.concat(mapa_anual)
        set_anos = df_anos["anos"].unique()
        mapa_incremental_anual = {}
        for ano in set_anos:
            df = pd.DataFrame()
            df = df_anos.loc[df_anos["anos"] == ano]
            df["valor" ] = ( (df["valor"].round(2)/df.loc[(df["caso"] == self.nome_caso_referencia)]["valor"].round(2).iloc[0]) - 1)*100
            df = df.drop(df[df['caso'] == self.nome_caso_referencia].index)
            mapa_incremental_anual[ano] = df
        df_completo = pd.concat(mapa_incremental_anual)
        return df_completo




