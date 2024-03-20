from typing import List
from os.path import join
from datetime import datetime
from calendar import monthrange
import numpy as np
import pandas as pd
from inewave.newave import Dger
from apps.utils.log import Log
import os.path
from apps.calibracao_cvar.caso import CasoCalibracaoCVAR
from apps.calibracao_cvar.usina import UsinaAvalicao
import warnings

class EcoIndicadores:
    """indicadores.df_custos_incrementais.to_csv
    Calcula os indicadores que são utilizados nas visualizações
    dos paretos para a escolha dos pares de CVaR candidatos
    para recalibração.
    """

    DIR_SINTESE = "sintese"

    def __init__(
        self, casos: List[CasoCalibracaoCVAR], nome_caso_referencia: str, usinas: List[UsinaAvalicao]
    ):
        warnings.simplefilter(action='ignore')
        
        self.casos = casos
        self.usinas = usinas
        self.nome_caso_referencia = nome_caso_referencia

    def retorna_df_concatenado(self,sintese):
        return pd.concat(self.retornaMapaDF(sintese))
    
    def __retorna_df(self, caso, sintese) -> pd.DataFrame:
        caminho_caso = caso.caminho
        arq_sintese = join(
            caminho_caso, self.DIR_SINTESE, sintese+".parquet.gzip"
        )
        check_file = os.path.isfile(arq_sintese)
        if(check_file) :
            df = pd.read_parquet(arq_sintese)
            return df
        else:
            #print("CASO: ", caso.nome, " NAO POSSUI A SINTESE: ", sintese)
            df_vazio = pd.DataFrame()
            return df_vazio
            
    def retornaMapaDF(self, sintese):
        dict = {}
        for c in self.casos:
            df = self.__retorna_df(c, sintese)
            df["caso"] = c.nome
            dict[c] = df
        return dict





