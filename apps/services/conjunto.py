from typing import Dict
from apps.model.caso import Caso
from apps.model.sintese import Sintese
from apps.model.unidade import UnidadeSintese
from apps.graficos.graficos import Graficos
from apps.graficos.graficosConjunto import GraficosConjunto
from apps.model.argumento import Argumento
from apps.model.conjuntoCasos import ConjuntoCasos
from apps.indicadores.indicadores_medios import IndicadoresMedios
from apps.indicadores.indicadores_anuais import IndicadoresAnuais
from apps.indicadores.indicadores_temporais import IndicadoresTemporais
from apps.model.conjuntoUnidade import ConjuntoUnidadeSintese
from apps.indicadores.eco_indicadores import EcoIndicadores
from apps.graficos.figura import Figura
from apps.services.tempo import Tempo
import pandas as pd
import os
import json

class Conjunto:


    def __init__(self, data, xinf, xsup, estagio, cenario, sintese, largura, altura, eixox, cronologico):
        self.conjuntoCasos = data.conjuntoCasos
        self.xinf  = xinf
        self.xsup = xsup
        self.eixox = eixox
        self.estagio = estagio
        self.cenario = cenario
        self.sintese = sintese
        self.largura = largura
        self.altura = altura
        self.cronologico = cronologico
        self.estudo = data.estudo
        self.nome_caso_referencia = ""
        # Gera saídas do estudo
        diretorio_saida = f"resultados/{self.estudo}/conjunto"
        self.graficosConjunto = GraficosConjunto(data.conjuntoCasos)
        os.makedirs(diretorio_saida, exist_ok=True)

        mapaTempo = {}
        for conjunto in self.conjuntoCasos:
            eco_indicadores = EcoIndicadores(conjunto.casos)
            df_temp = eco_indicadores.retorna_df_concatenado("TEMPO")
            temp = []
            for caso in conjunto.casos:
                df_caso = df_temp.loc[(df_temp["caso"] == caso.nome)]
                df_caso["tempo"] = df_caso["tempo"] /(60)
                if(caso.modelo == "NEWAVE"):
                    temp.append(df_caso.loc[(df_caso["etapa"] == "Tempo Total")])
                if(caso.modelo == "DESSEM"):
                    df = df_caso.groupby(['caso']).sum().drop(["etapa","modelo"],axis = 1).reset_index(drop=False)
                    temp.append(df)
            df_tempo_total = pd.concat(temp).reset_index(drop = True)

            #df_tempo_total = Tempo.retorna_df_tempo_total_casos(conjunto.casos, df_temp)
            df_tempo_total["conjunto"] = conjunto.nome
            mapaTempo[conjunto] = df_tempo_total
        eco_indicadores.exportar(pd.concat(mapaTempo), diretorio_saida,  "tempo "+self.estudo)
        mapaGO = self.graficosConjunto.gera_grafico_linhas_artesanal(mapaTempo, colY = "tempo", colX = "caso")
        figura = Figura(conjUnity, mapaGO, "Comparacao Tempo "+self.estudo)
        self.graficosConjunto.exportar(figura.fig, diretorio_saida, figura.titulo)

        for sts in data.sinteses:
            espacial = sts.sintese.split("_")[1]
            if(espacial == "SIN"):
                arg = Argumento(None, None, "SIN")
                conj = ConjuntoUnidadeSintese(sts,arg , "casos", data.limites, data.tamanho_texto)
                diretorio_saida_arg = diretorio_saida+"/"+espacial
                os.makedirs(diretorio_saida_arg, exist_ok=True)
                #unity = UnidadeSintese(sts, args, "caso", data.limites, data.tamanho_texto)
                self.executa(conj,diretorio_saida_arg )
            else:
                for arg in data.args:
                    if(espacial == arg.chave):
                        conj = ConjuntoUnidadeSintese(sts,arg , "casos", data.limites, data.tamanho_texto) 
                        diretorio_saida_arg = diretorio_saida+"/"+arg.chave+"/"+arg.nome
                        os.makedirs(diretorio_saida_arg, exist_ok=True)
                        #unity = UnidadeSintese(sts, args, "caso", data.limites, data.tamanho_texto)
                        self.executa(conj,diretorio_saida_arg )





    def executa(self, conjUnity, diretorio_saida_arg):
        mapaTemporal_2_mes = {}
        mapaTemporal_1_est = {}
        mapaMedio = {}
        mapaCronologico = {}
        for unity in conjUnity.listaUnidades:
            mapaTemporal = {}
            listaTemporal_2_mes = []
            listaTemporal_1_est = []
            listaMedia = []
            listaCronologica = []
            for conjunto in self.conjuntoCasos:
                indicadores_temporais = IndicadoresTemporais(conjunto.casos)  
                indicadores_medios = IndicadoresMedios(conjunto.casos, self.nome_caso_referencia)   
                df_temporal = indicadores_temporais.retorna_df_concatenado(unity, self.cenario)
                if(self.xsup < df_temporal["estagio"].max()):
                    df_temporal = df_temporal.loc[(df_temporal["estagio"] < self.xsup)]
                if(self.xinf > df_temporal["estagio"].min()):
                    df_temporal = df_temporal.loc[(df_temporal["estagio"] > self.xinf)]

                df_temporal["conjunto"] = conjunto.nome
                mapaTemporal[conjunto.nome] = df_temporal
                listaCronologica.append(df_temporal)

                #df_temporal_primeiro_est = df_temporal.loc[df_temporal["estagio"] == 1 ].reset_index(drop = True)
                #df_temporal_primeiro_est["conjunto"] = conjunto.nome
                #listaTemporal_1_est.append(df_temporal_primeiro_est)

                #df_medio = indicadores_medios.retorna_df_concatenado(unity)
                #df_medio["conjunto"] = conjunto.nome
                #listaMedia.append(df_medio)

            indicadores_temporais.exportar(pd.concat(mapaTemporal), diretorio_saida_arg,  "temporal_"+conjUnity.titulo+"_"+unity.titulo+"_"+self.estudo)


            mapaFig = self.graficosConjunto.subplot_gera_grafico_linha_casos(mapaTemporal, conjUnity, unity, conjUnity.titulo+" "+unity.titulo+" "+self.estudo, legEixoX = "estagios")
            for titulo in mapaFig:
                self.graficosConjunto.exportar(mapaFig[titulo], diretorio_saida_arg, titulo+self.estudo, self.largura, self.altura)

            mapaCronologico[unity] = pd.concat(listaCronologica)
            indicadores_temporais.exportar(pd.concat(listaCronologica), diretorio_saida_arg,  "cronologico_"+unity.titulo+"_"+self.estudo)

            #mapaTemporal_1_est[unity] = pd.concat(listaTemporal_1_est)
            #indicadores_temporais.exportar(pd.concat(listaTemporal_1_est), diretorio_saida_arg,  "primeiro_est_"+conjUnity.titulo+"_"+unity.titulo+"_"+self.estudo)

            #mapaMedio[unity] = pd.concat(listaMedia)
            #indicadores_medios.exportar(pd.concat(listaMedia), diretorio_saida_arg,  "media_"+unity.titulo+"_"+self.estudo)
            
        if(self.cronologico == "True"):
            mapaGO = self.graficosConjunto.gera_grafico_linha(mapaCronologico, colx = self.eixox, cronologico = self.cronologico)
            figura = Figura(conjUnity, mapaGO, "Temporal "+conjUnity.titulo+self.estudo)
            self.graficosConjunto.exportar(figura.fig, diretorio_saida_arg, figura.titulo, self.largura, self.altura)
        #mapaGO = self.graficosConjunto.gera_grafico_linhas_diferentes_casos(mapaTemporal_1_est)
        #figura = Figura(conjUnity, mapaGO, "Primeiro Est "+conjUnity.titulo+self.estudo)
        #self.graficosConjunto.exportar(figura.fig, diretorio_saida_arg, figura.titulo)

        #mapaGO = self.graficosConjunto.gera_grafico_linhas_diferentes_casos(mapaMedio)
        #figura = Figura(conjUnity, mapaGO, "Media "+conjUnity.titulo+self.estudo)
        #self.graficosConjunto.exportar(figura.fig, diretorio_saida_arg, figura.titulo)

