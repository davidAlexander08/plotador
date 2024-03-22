from typing import List
from os.path import join
import pandas as pd
from apps.utils.log import Log
import os.path
from apps.model.caso import Caso
from apps.indicadores.abstractIndicadores import AbstractIndicadores
import warnings

class EcoIndicadores:
    """indicadores.df_custos_incrementais.to_csv
    Calcula os indicadores que são utilizados nas visualizações
    dos paretos para a escolha dos pares de CVaR candidatos
    para recalibração.
    """

    

    def __init__(  self, casos: List[Caso] ):
        warnings.simplefilter(action='ignore')
        self.casos = casos
        AbstractIndicadores.__init__(self)
        
    def retorna_df_concatenado(self,sintese):
        return pd.concat(self.retornaMapaDF(sintese))
    
    def __retorna_df(self, caso, sintese) -> pd.DataFrame:
        arq_sintese = join( caso.caminho, self.DIR_SINTESE, sintese+".parquet.gzip"  )
        check_file = os.path.isfile(arq_sintese)
        if(check_file) :
            df = pd.read_parquet(arq_sintese)
            return df
        else:
            df_vazio = pd.DataFrame()
            return df_vazio
            
    def retornaMapaDF(self, sintese):
        dict = {}
        for c in self.casos:
            df = self.__retorna_df(c, sintese)
            df["caso"] = c.nome
            dict[c] = df
        return dict





