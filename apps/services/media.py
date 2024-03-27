from typing import Dict
from apps.model.unidade import UnidadeSintese
from apps.graficos.graficos import Graficos
from apps.indicadores.indicadores_temporais import IndicadoresTemporais
from apps.indicadores.indicadores_medios import IndicadoresMedios
from apps.model.caso import Caso
from apps.model.sintese import Sintese
from apps.model.argumento import Argumento
import os
import json

class Media:


    def __init__(self, data):
      self.estudo = data.estudo
      self.nome_caso_referencia = data.nome_caso_referencia
      self.casos = data.casos      
      self.indicadores_medios = IndicadoresMedios(casos, self.nome_caso_referencia)
      self.indicadores_temporais = IndicadoresTemporais(casos)
      self.graficos = Graficos(casos)
      # Gera saídas do estudo
      diretorio_saida = f"resultados/{self.estudo}/media"
      os.makedirs(diretorio_saida, exist_ok=True)
      for sts in data.sinteses:
          espacial = sts.sintese.split("_")[1]
          if(espacial == "SIN"):
              arg = Argumento(None, None)
              diretorio_saida_arg = diretorio_saida+"/"+espacial
              os.makedirs(diretorio_saida_arg, exist_ok=True)
              unity = UnidadeSintese(sts, "estagios", arg, tamanho_texto = data.tamanho_texto)
              self.executa(unity,diretorio_saida_arg )
          else:
            for arg in data.args:
                if(espacial == arg.chave):
                    unity = UnidadeSintese(sts, "estagios", arg, tamanho_texto = data.tamanho_texto)
                    diretorio_saida_arg = diretorio_saida+"/"+arg.chave+"/"+arg.nome
                    os.makedirs(diretorio_saida_arg, exist_ok=True)
                    self.executa(unity,diretorio_saida_arg )

                        

    def executa(self, unity, diretorio_saida_arg):
        df_unity = self.indicadores_medios.retorna_df_concatenado(unity)
        self.indicadores_medios.exportar(df_unity, diretorio_saida_arg,  "medias_"+unity.titulo+"_"+self.estudo)

        fig = self.graficos.gera_grafico_barra(df_unity["valor"], df_unity["caso"],  unity.legendaEixoX, unity.legendaEixoY, 2, unity.titulo)
        self.graficos.exportar(fig, diretorio_saida_arg, "medias_"+unity.titulo+"_"+self.estudo)

        df_unity_incr = self.indicadores_medios.retorna_DF_cenario_medio_incremental_percentual(unity)
        self.indicadores_medios.exportar(df_unity_incr, diretorio_saida_arg, "medias_incr_"+unity.titulo+"_"+self.estudo)
        
        fig = self.graficos.gera_grafico_barra(df_unity_incr["valor"], df_unity_incr["caso"],  unity.legendaEixoX, unity.legendaEixoY, 2, unity.titulo)
        self.graficos.exportar(fig, diretorio_saida_arg, "medias_incr_"+unity.titulo+"_"+self.estudo)
