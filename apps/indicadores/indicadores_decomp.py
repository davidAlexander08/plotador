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
from apps.model.usina import UsinaAvalicao
import warnings

class IndicadoresCalibracaoCVAR_Decomp:
    """indicadores.df_custos_incrementais.to_csv
    Calcula os indicadores que são utilizados nas visualizações
    dos paretos para a escolha dos pares de CVaR candidatos
    para recalibração.
    """

    DIR_SINTESE = "sintese"

    def __init__(
        self, casos: List[Caso], nome_caso_referencia: str, usinas: List[UsinaAvalicao]
    ):
      warnings.simplefilter(action='ignore')
      self.__df_valores_medios_decomp = None
      self.casos = casos
      self.usinas = usinas

    def __le_arquivo_sintese_caso_periodo_decomp(
        self, caso: Caso, nome_sintese: str, segundoArgumento
        ) -> pd.DataFrame:
        
        caminho_caso = caso.caminho
        arq_sintese = join(
            caminho_caso+"/decomp/", self.DIR_SINTESE, f"{nome_sintese}.parquet.gzip"
        )
        if(os.path.isfile(arq_sintese)):
            df = pd.read_parquet(arq_sintese)
            if(segundoArgumento is None):
                dados = df.loc[df["cenario"] == "mean"].reset_index(drop=True)
            else:
                dados = (
                    df.loc[
                        (df["cenario"] == "mean") & (df["submercado"] == segundoArgumento)].reset_index(drop=True)
                )
            return dados
        else:
            dados = pd.DataFrame({"valor":[0]})
            return dados

    def __gera_df_valores_medios_periodo_decomp(
        self, caso: Caso, nome_sintese:str, segundoArgumento
    ) -> pd.DataFrame:
        nome_caso = caso.nome
        df_med = self.__le_arquivo_sintese_caso_periodo_decomp(caso, nome_sintese, segundoArgumento)
        return df_med

    def __gera_df_acumulado_valores_medios_periodo_decomp(self,nome_sintese, segundoArgumento, coluna) -> pd.DataFrame:
        Log.log().info("Gerando DataFrame de valores médios por periodo")
        mapaCasos  = {}
        df = pd.DataFrame()
        for c in self.casos:
            df[c.nome] = self.__gera_df_valores_medios_periodo_decomp(c,nome_sintese, segundoArgumento)[coluna]
        df.index.name = "estagio"
        return df

    def calcula_df_valores_medios_periodo_decomp(self, nome_sintese, segundoArgumento, coluna) -> pd.DataFrame:
        dfvalores_medios_periodo = self.__gera_df_acumulado_valores_medios_periodo_decomp(nome_sintese, segundoArgumento, coluna)
        return dfvalores_medios_periodo



    def __le_arquivo_sintese_caso_decomp_SIN(
        self, caso: Caso, nome_sintese: str
    ) -> np.ndarray:
        caminho_caso = caso.caminho
        arq_sintese = join(
            caminho_caso+"/decomp/", self.DIR_SINTESE,f"{nome_sintese}.parquet.gzip"
        )
        df = pd.read_parquet(arq_sintese)
        df_teste = df.loc[df["cenario"] == "mean"]
        df_teste = df_teste.round(1)
        return df_teste.reset_index(drop = True)

    def __le_arquivo_sintese_caso_decomp_SBM(
        self, caso: Caso, nome_sintese: str, submercado: str
    ) -> np.ndarray:
        caminho_caso = caso.caminho
        arq_sintese = join(
            caminho_caso+"/decomp/", self.DIR_SINTESE,f"{nome_sintese}.parquet.gzip"
        )
        df = pd.read_parquet(arq_sintese)
        df_teste = df.loc[(df["cenario"] == "mean") & (df["submercado"] == submercado)]
        df_teste = df_teste.round(1)
        return df_teste.reset_index(drop = True)

    def __gera_df_valores_medios_caso_decomp(self, caso: Caso) -> pd.DataFrame:
        nome_caso = caso.nome
        cmo_se_med = self.__le_arquivo_sintese_caso_decomp_SBM(
            caso, 
            "CMO_SBM_EST", 
            "SE"
            )
        
        cmo_ne_med = self.__le_arquivo_sintese_caso_decomp_SBM(
            caso, 
            "CMO_SBM_EST", 
            "NE"
            )
        earm_med_perc = self.__le_arquivo_sintese_caso_decomp_SIN(
            caso, 
            "EARPF_SIN_EST"
            )
        evert_tot_med =  self.__le_arquivo_sintese_caso_decomp_SIN(
            caso, 
            "EVER_SIN_EST"
            )
        gter_med = self.__le_arquivo_sintese_caso_decomp_SIN(
            caso, 
            "GTER_SIN_EST"
            )
        ghid_med = self.__le_arquivo_sintese_caso_decomp_SIN(
            caso, 
            "GHID_SIN_EST"
            )

        ever_turb = self.__le_arquivo_sintese_caso_decomp_SIN(
            caso, 
            "EVERT_SIN_EST"
            )

        ever_not_turb = self.__le_arquivo_sintese_caso_decomp_SIN(
            caso, 
            "EVERNT_SIN_EST"
            )

        df = pd.DataFrame()
        df["estagio"] = cmo_se_med["estagio"]
        df["caso"] = nome_caso
        df["cmo_se_med"] = cmo_se_med["valor"]
        df["cmo_ne_med"] = cmo_ne_med["valor"]
        df["earm_med_perc"] = earm_med_perc["valor"]
        df["vert_tot_med_mwmes"] = evert_tot_med["valor"]
        df["gterm_med_mwmes"] = gter_med["valor"]
        df["ghid_med_mwmes"] = ghid_med["valor"]
        df["evert"] = ever_turb["valor"]
        df["evernt"] = ever_not_turb["valor"]

        return df

    def gera_df_valores_medios_decomp(self) -> pd.DataFrame:
        Log.log().info("Gerando DataFrame de valores médios dos casos decomp")
        """
        Gera o DataFrame que contém as informações para serem visualizadas
        nos gráficos de fronteiras de pareto.

        Colunas:
        """
        dfs_casos = [
            self.__gera_df_valores_medios_caso_decomp(c) for c in self.casos
                            ]
        df_completo = pd.concat(dfs_casos)
        return df_completo
    
    @property
    def df_valores_medios_decomp(self) -> pd.DataFrame:
        if self.__df_valores_medios_decomp is None:
            self.__df_valores_medios_decomp = self.gera_df_valores_medios_decomp()
        return self.__df_valores_medios_decomp
    
