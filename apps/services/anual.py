from typing import Dict
from apps.model.unidade import UnidadeSintese
from apps.graficos.graficos import Graficos
from apps.indicadores.indicadores_anuais import IndicadoresAnuais
from apps.model.caso import Caso
from apps.model.sintese import Sintese
from apps.model.argumento import Argumento
from apps.interface.dados_json_caso import Dados_json_caso
import os
import json

class Anual:


    def __init__(self, data):
        self.estudo = data.estudo
        self.nome_caso_referencia = data.nome_caso_referencia
        self.casos = data.casos
        self.indicadores_anuais = IndicadoresAnuais(casos, self.nome_caso_referencia)
        self.graficos = Graficos(casos)
        diretorio_saida = f"resultados/{self.estudo}/anual"
        os.makedirs(diretorio_saida, exist_ok=True)
      
        for sts in data.sinteses:
            espacial = sts.sintese.split("_")[1]
            if(espacial == "SIN"):
                arg = Argumento(None, None)
                diretorio_saida_arg = diretorio_saida+"/"+espacial
                os.makedirs(diretorio_saida_arg, exist_ok=True)
                unity = UnidadeSintese(sts, "estagios", arg)
                self.executa(unity,diretorio_saida_arg )
            else:
                for arg in data.args:
                    if(espacial == arg.chave):
                        diretorio_saida_arg = diretorio_saida+"/"+arg.chave+"/"+arg.nome
                        os.makedirs(diretorio_saida_arg, exist_ok=True)
                        unity = UnidadeSintese(sts, "estagios", arg)
                        self.executa(unity,diretorio_saida_arg )
      



    def executa(self, unity, diretorio_saida_arg):
        df = self.indicadores_anuais.retorna_df_concatenado(unity )
        self.indicadores_anuais.exportar(df, diretorio_saida_arg,  "anual_"+unity.titulo+"_"+self.estudo)

        ## GRAFICOS ANOS DISCRETIZADOS
        fig = self.graficos.gera_grafico_barras_diferentes(df, "anos", "valor", "caso",  unity.legendaEixoX, unity.legendaEixoY, 2, unity.titulo+"_anos_discretizados")
        self.graficos.exportar(fig, diretorio_saida_arg, "anual_"+unity.titulo+"_anos_discretizados_"+self.estudo)

        df_unity = self.indicadores_anuais.retorna_DF_cenario_anual_medio_incremental_percentual(unity )
        self.indicadores_anuais.exportar(df_unity, diretorio_saida_arg,  "anual_incr_"+unity.titulo+"_"+self.estudo)
    
        #ANOS DISCRETIZADOS INCREMENTAL
        fig = self.graficos.gera_grafico_barras_diferentes(df_unity, "anos", "valor", "caso",  unity.legendaEixoX, unity.legendaEixoY, 2, unity.titulo+"_incremental")
        self.graficos.exportar(fig, diretorio_saida_arg, "anual_"+unity.titulo+"_anos_discretizados_incremental_"+self.estudo)

        ## PRIMEIRO ANO INCREMENTAL
        fig = self.graficos.gera_grafico_barras_diferentes(
            df_unity.loc[(df_unity["anos"] == df_unity["anos"].iloc[0])], 
            "anos", 
            "valor", 
            "caso",  
            unity.legendaEixoX, 
            unity.legendaEixoY, 
            2, 
            unity.titulo+"_incremental"
        )
        self.graficos.exportar(fig, diretorio_saida_arg, "anual_"+unity.titulo+"_primeiro_ano_incremental_"+self.estudo)

        df_unity = self.indicadores_anuais.retorna_df_concatenado_acumulado(unity )
        self.indicadores_anuais.exportar(df_unity, diretorio_saida_arg,  "anual_acum_"+unity.titulo+"_"+self.estudo)
        
        ## GRAFICOS PRIMEIRO ANO
        df = df_unity.loc[(df_unity["anos"] == df_unity["anos"].iloc[0])]
        fig = self.graficos.gera_grafico_barra(df["valor"], df["caso"],  unity.legendaEixoX, unity.legendaEixoY, 2, unity.titulo+"_primeiro_ano")
        self.graficos.exportar(fig, diretorio_saida_arg, "anual_"+unity.titulo+"_primeiro_ano_"+self.estudo)

        ## OUTROS ANOS
        df = df_unity.loc[(df_unity["anos"] != df_unity["anos"].iloc[0])]
        fig = self.graficos.gera_grafico_barra(df["valor"], df["caso"],  unity.legendaEixoX, unity.legendaEixoY, 2, unity.titulo+"_outros_anos")
        self.graficos.exportar(fig, diretorio_saida_arg, "anual_"+unity.titulo+"_outros_anos_"+self.estudo)

        ## GRAFICOS ANO E OUTROS ANOS DISCRETIZADOS
        fig = self.graficos.gera_grafico_barras_diferentes(df_unity, "anos", "valor", "caso",  unity.legendaEixoX, unity.legendaEixoY, 2, unity.titulo+"_primeiro_ano_outros_anos")
        self.graficos.exportar(fig, diretorio_saida_arg, "anual_"+unity.titulo+"_primeiro_ano_e_outros_anos_"+self.estudo)
                
        df_unity = self.indicadores_anuais.retorna_DF_cenario_anual_acumulado_medio_incremental_percentual(unity )
        self.indicadores_anuais.exportar(df_unity, diretorio_saida_arg,  "anual_acum_incr_"+unity.titulo+"_"+self.estudo)

        #ANOS DISCRETIZADOS INCREMENTAL
        fig = self.graficos.gera_grafico_barras_diferentes(df_unity, "anos", "valor", "caso",  unity.legendaEixoX, unity.legendaEixoY, 2, unity.titulo+"_incremental")
        self.graficos.exportar(fig, diretorio_saida_arg, "anual_"+unity.titulo+"_anos_discretizados_incremental_"+self.estudo)

        ## PRIMEIRO ANO INCREMENTAL
        df = df_unity.loc[(df_unity["anos"] != df_unity["anos"].iloc[0])]
        fig = self.graficos.gera_grafico_barras_diferentes(df, "anos", "valor", "caso",  unity.legendaEixoX, unity.legendaEixoY, 2, unity.titulo+"_incremental")
        self.graficos.exportar(fig, diretorio_saida_arg, "anual_"+unity.titulo+"_outros_anos_incremental_"+self.estudo)
