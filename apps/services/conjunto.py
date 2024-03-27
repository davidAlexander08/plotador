from typing import Dict
from apps.model.caso import Caso
from apps.model.sintese import Sintese
from apps.model.unidade import UnidadeSintese
from apps.graficos.graficos import Graficos
from apps.model.argumento import Argumento
from apps.model.conjuntoCasos import ConjuntoCasos
from apps.indicadores.indicadores_medios import IndicadoresMedios
from apps.indicadores.indicadores_anuais import IndicadoresAnuais
from apps.indicadores.indicadores_temporais import IndicadoresTemporais
import pandas as pd
import os
import json

class Conjunto:


    def __init__(self, data):
        self.conjuntoCasos = data.conjunto
        self.estudo = data.estudo
        self.nome_caso_referencia = ""
        # Gera saídas do estudo
        diretorio_saida = f"resultados/{self.estudo}/conjunto"
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
        
    
        listaConjDF = []
        listaConjDF_Anual = []
        listaConjDF_Temporal_Primeiro_Mes = []
        listaConjDF_Temporal_Segundo_Mes = []
        mapaConjDF_Temporal = {}
        listaNomes = []
        mapCores = {}
        for conjunto in self.conjuntoCasos:
            indicador_conj_medio = IndicadoresMedios(conjunto.casos, self.nome_caso_referencia)
            indicadores_anuais = IndicadoresAnuais(conjunto.casos, self.nome_caso_referencia)
            indicadores_temporais = IndicadoresTemporais(conjunto.casos)
            graficos = Graficos(conjunto.casos)
            
            
            df_unity = indicador_conj_medio.retorna_df_concatenado(unity )
            df_unity = df_unity.rename(columns={"valor": conjunto.nome}).reset_index(drop = True)
            #df_unity["conjunto"] = conjunto.nome

            #df_anual = indicadores_anuais.retorna_df_concatenado_acumulado(unity )
            #df_anual = df_anual.rename(columns={"valor": conjunto.nome}).reset_index(drop = True)

            df_temporal = indicadores_temporais.retorna_df_concatenado(unity )
            df_temporal = df_temporal.rename(columns={"valor": conjunto.nome}).reset_index(drop = True)

            df_temporal_primeiro_mes = df_temporal.loc[df_temporal["estagio"] == 1 ].reset_index(drop = True)
            df_temporal_segundo_mes = df_temporal.loc[df_temporal["estagio"] == 2 ].reset_index(drop = True)
            listaConjDF.append(df_unity)
            #listaConjDF_Anual.append(df_anual)
            listaConjDF_Temporal_Primeiro_Mes.append(df_temporal_primeiro_mes)
            listaConjDF_Temporal_Segundo_Mes.append(df_temporal_segundo_mes)
            mapaConjDF_Temporal[conjunto.nome]  = df_temporal
            
            listaNomes.append(conjunto.nome)
            mapCores[conjunto.nome] = conjunto.cor

        df_concat = pd.concat(listaConjDF, axis=1)
        df_concatenado = df_concat.loc[:,~df_concat.columns.duplicated()].copy()   #df_concat.T.drop_duplicates().T

        #df_concat_anual = pd.concat(listaConjDF_Anual, axis=1)
        #df_concatenado_anual = df_concat_anual.loc[:,~df_concat_anual.columns.duplicated()].copy()   #df_concat.T.drop_duplicates().T

        df_concat_temporal_primeiro_mes = pd.concat(listaConjDF_Temporal_Primeiro_Mes, axis=1)
        df_concatenado_temporal_primeiro_mes = df_concat_temporal_primeiro_mes.loc[:,~df_concat_temporal_primeiro_mes.columns.duplicated()].copy()   #df_concat.T.drop_duplicates().T
        
        df_concat_temporal_segundo_mes = pd.concat(listaConjDF_Temporal_Segundo_Mes, axis=1)
        df_concatenado_temporal_segundo_mes = df_concat_temporal_segundo_mes.loc[:,~df_concat_temporal_segundo_mes.columns.duplicated()].copy()   #df_concat.T.drop_duplicates().T

        indicador_conj_medio.exportar(df_concatenado, diretorio_saida_arg,  "conj_med_"+unity.titulo+"_"+self.estudo)
        #indicadores_anuais.exportar(df_concatenado_anual, diretorio_saida_arg,  "conj_anual_"+unity.titulo+"_"+self.estudo)
        indicadores_temporais.exportar(df_concatenado_temporal_primeiro_mes, diretorio_saida_arg,  "primeiro_mes_"+unity.titulo+"_"+self.estudo)
        indicadores_temporais.exportar(df_concatenado_temporal_segundo_mes, diretorio_saida_arg,  "segundo_mes_"+unity.titulo+"_"+self.estudo)


        fig = graficos.gera_grafico_linhas_diferentes_casos(df_concatenado, "caso", listaNomes, mapCores, unity.legendaEixoY, unity.legendaEixoX, unity.titulo)
        graficos.exportar(fig, diretorio_saida_arg, "conj_medias_"+unity.titulo+"_"+self.estudo)
        
        #df_primeiro_ano = df_concatenado_anual.loc[(df_concatenado_anual["anos"] == df_concatenado_anual["anos"].iloc[0])]
        #fig = graficos.gera_grafico_linhas_diferentes_casos(df_primeiro_ano, "caso", listaNomes, mapCores, unity.legendaEixoY, unity.legendaEixoX, unity.titulo+"_Primeiro_Ano")
        #graficos.exportar(fig, diretorio_saida_arg, "conj_anual_"+unity.titulo+"_primeiro_ano_"+self.estudo)
        
        #df_outros_anos = df_concatenado_anual.loc[(df_concatenado_anual["anos"] == df_concatenado_anual["anos"].iloc[1])]
        #fig = graficos.gera_grafico_linhas_diferentes_casos(df_outros_anos, "caso", listaNomes, mapCores, unity.legendaEixoY, unity.legendaEixoX, unity.titulo+"_Outros_Anos")
        #graficos.exportar(fig, diretorio_saida_arg, "conj_anual_"+unity.titulo+"_outros_anos_"+self.estudo)
        
        fig = graficos.gera_grafico_linhas_diferentes_casos(df_concatenado_temporal_primeiro_mes, "caso", listaNomes, mapCores, unity.legendaEixoY, unity.legendaEixoX, unity.titulo+"_Primeiro_Mes")
        graficos.exportar(fig, diretorio_saida_arg, "conj_temporal_"+unity.titulo+"_primeiro_mes_"+self.estudo)
        
        fig = graficos.gera_grafico_linhas_diferentes_casos(df_concatenado_temporal_segundo_mes, "caso", listaNomes, mapCores, unity.legendaEixoY, unity.legendaEixoX, unity.titulo+"_Segundo_Mes")
        graficos.exportar(fig, diretorio_saida_arg, "conj_temporal_"+unity.titulo+"_segundo_mes_"+self.estudo)

        mapaFig = graficos.subplot_gera_grafico_linha_casos(self.conjuntoCasos, mapaConjDF_Temporal, unity.legendaEixoY , unity.legendaEixoX, unity.titulo)
        for titulo in mapaFig:
            graficos.exportar(mapaFig[titulo], diretorio_saida_arg, titulo+self.estudo, 2000, 900)