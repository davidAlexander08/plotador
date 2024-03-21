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
from apps.indicadores.indicadores_temporais import IndicadoresTemporais
from apps.indicadores.eco_indicadores import EcoIndicadores
import warnings

class IndicadoresCenarios:

    DIR_SINTESE = "sintese"

    def __init__(
        self, casos: List[Caso], nome_caso_referencia: str, usinas: List[UsinaAvalicao]
    ):
        warnings.simplefilter(action='ignore')
        
        self.casos = casos
        self.usinas = usinas
        self.nome_caso_referencia = nome_caso_referencia
      
        self.indicadores_temporais = IndicadoresTemporais(casos, nome_caso_referencia,usinas)
        self.eco_indicadores = EcoIndicadores(casos, nome_caso_referencia,usinas)


    def mapa_df_cenario(self, sintese, coluna, argumento_filtro):
      eco_mapa  = self.eco_indicadores.retornaMapaDF(sintese)
      mapa_temporal = {}
      if( (coluna is None) & (argumento_filtro is None) ):
          return eco_mapa
      else:
          for c in self.casos: eco_mapa[c] = eco_mapa[c].loc[eco_mapa[c][coluna] == argumento_filtro]
          mapa_temporal = eco_mapa
      return mapa_temporal

    def retorna_df_concatenado(self,sintese, coluna = None, argumento_filtro = None):
        return pd.concat(self.mapa_df_cenario(sintese, coluna, argumento_filtro))
