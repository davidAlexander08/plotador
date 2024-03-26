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
from apps.indicadores.eco_indicadores import EcoIndicadores
import warnings

class IndicadoresCenarios(EcoIndicadores):

    DIR_SINTESE = "sintese"

    def __init__(self, casos: List[Caso] ):
        warnings.simplefilter(action='ignore')
        self.casos = casos
        EcoIndicadores.__init__(self, casos)


    def mapa_df_cenario(self, unidade):
      eco_mapa  = self.retornaMapaDF(unidade.sintese)
      mapa_temporal = {}
      if( (unidade.fitroColuna is None) & (unidade.filtroArgumento is None) ):
          return eco_mapa
      else:
          for c in self.casos: eco_mapa[c] = eco_mapa[c].loc[eco_mapa[c][unidade.fitroColuna] == unidade.filtroArgumento]
          mapa_temporal = eco_mapa
      return mapa_temporal

    def retorna_df_concatenado(self,unidade):
        return pd.concat(self.mapa_df_cenario(unidade))
