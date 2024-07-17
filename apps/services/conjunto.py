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
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import os
import json

class Conjunto:


    def __init__(self, data, xinf, xsup, yinf, ysup,estagio, cenario, sintese, argumentos, chave, largura, altura, eixox, cronologico, titulo, subplot, labelx, tamanho):
        self.conjuntoCasos = data.conjuntoCasos
        self.xinf  = xinf
        self.xsup = xsup
        self.yinf = yinf
        self.ysup = ysup
        self.eixox = eixox
        self.labelx = labelx
        self.tamanho_texto = data.tamanho_texto if tamanho is None else int(tamanho)
        self.estagio = estagio
        self.cenario = cenario
        self.sintese = sintese
        self.largura = largura
        self.altura = altura
        self.titulo = titulo
        self.argumentos  = argumentos
        self.chave = chave
        self.cronologico = cronologico
        self.estudo = data.estudo
        self.nome_caso_referencia = ""
        # Gera saídas do estudo
        diretorio_saida = f"resultados/{self.estudo}/conjunto" 
        self.graficosConjunto = GraficosConjunto(data.conjuntoCasos)
        os.makedirs(diretorio_saida, exist_ok=True)

        self.subp_col = int(subplot.split(",")[0]) if subplot is not None else 4
        self.subp_lin = int(subplot.split(",")[1]) if subplot is not None else 3
        print(self.subp_col, " ", self.subp_lin)

        if(self.argumentos is not None and self.chave is None):
            print("FALTA DECLARAR A CHAVE DO ARGUMENTO")
            exit(1)
        if(self.chave is not None and self.argumentos is None):
            print("FALTA DECLARAR O ARGUMENTO DO ARGUMENTO")
            exit(1)
        if(self.chave is not None and self.argumentos is not None):
            lista_argumentos = self.argumentos.split(",")
            data.args = [Argumento(lista_argumentos, self.chave, "out")] 
            if(len(lista_argumentos) == 1 and self.titulo == " "): 
                self.titulo = lista_argumentos[0]

        sts_temp = Sintese("TEMPO")
        arg_temp = Argumento(None, None, ["ree", "25x35"])
        conj = ConjuntoUnidadeSintese(sts_temp,arg_temp , "casos", data.limites, self.tamanho_texto)
        mapaTempo = {}
        fig = go.Figure()
        concat_df = []
        listaGO = []
        for conjunto in self.conjuntoCasos:
            eco_indicadores = EcoIndicadores(conjunto.casos)
            df_temp = eco_indicadores.retorna_df_concatenado(conj.sintese.sintese)
            temp = []
            for caso in conjunto.casos:
                df_caso = df_temp.loc[(df_temp["caso"] == caso.nome)]
                df_caso["tempo"] = df_caso["tempo"] /(60)
                if(caso.modelo == "NEWAVE" or caso.modelo == "DECOMP"):
                    temp.append(df_caso.loc[(df_caso["etapa"] == "Tempo Total")])
                if(caso.modelo == "DESSEM"):
                    df = df_caso.groupby(['caso']).sum().drop(["etapa","modelo"],axis = 1).reset_index(drop=False)
                    temp.append(df)
            df_tempo_total = pd.concat(temp).reset_index(drop = True)
            df_tempo_total["conjunto"] = conjunto.nome
            mapaTempo[conjunto] = df_tempo_total
            concat_df.append(df_tempo_total)
            listaGO.append(go.Scatter(
                                x = df_tempo_total["caso"],
                                y = df_tempo_total["tempo"],
                                name = conjunto.nome,
                                line = dict(color = conjunto.cor),
                                showlegend=True,
                            )
            )
        for elemento_go in listaGO:
            fig.add_trace(elemento_go)
        fig.update_layout(title= "Comparacao Tempo de Execucao")
        fig.update_yaxes(title="min") 
        fig.update_xaxes(title="casos") 
        fig.update_layout(font=dict(size= self.tamanho_texto))  
        self.graficosConjunto.exportar(fig,diretorio_saida, "conjunto tempo "+self.estudo, self.largura, self.altura)

        df_tempo = pd.concat(concat_df)
        eco_indicadores.exportar(df_tempo,diretorio_saida,  "conjunto_tempo "+self.estudo)
        sinteses = data.sinteses if (self.sintese == "") else [Sintese(self.sintese)]


        for sts in sinteses:
            espacial = sts.sintese.split("_")[1]
            if(espacial == "SIN"):
                arg = Argumento(None, None, "SIN")
                conj = ConjuntoUnidadeSintese(sts,arg , "casos", data.limites, self.tamanho_texto)
                if(self.labelx is not None):
                    conj.legendaEixoX = self.labelx
                diretorio_saida_arg = diretorio_saida+"/"+espacial
                os.makedirs(diretorio_saida_arg, exist_ok=True)
                #unity = UnidadeSintese(sts, args, "caso", data.limites, data.tamanho_texto)
                self.executa(conj,diretorio_saida_arg )
            else:
                for arg in data.args:
                    if(espacial == arg.chave):
                        conj = ConjuntoUnidadeSintese(sts,arg , "casos", data.limites, self.tamanho_texto) 
                        if(self.labelx is not None):
                            conj.legendaEixoX = self.labelx
                        diretorio_saida_arg = diretorio_saida+"/"+arg.chave+"/"+arg.nome
                        os.makedirs(diretorio_saida_arg, exist_ok=True)
                        #unity = UnidadeSintese(sts, args, "caso", data.limites, data.tamanho_texto)
                        self.executa(conj,diretorio_saida_arg )





    def executa(self, conjUnity, diretorio_saida_arg):
        
        mapaTemporal_2_mes = {}
        mapaTemporal_1_est = {}
        mapaMedio = {}
        mapaCronologico = {}
        flag_muitos_casos = 0
        for unity in conjUnity.listaUnidades:
            mapaTemporal = {}
            listaTemporal_2_mes = []
            listaTemporal_1_est = []
            listaMedia = []
            listaCronologica = []
            for conjunto in self.conjuntoCasos:
                if(len(conjunto.casos) > 12):
                    flag_muitos_casos = 1
                indicadores_temporais = IndicadoresTemporais(conjunto.casos)  
                indicadores_medios = IndicadoresMedios(conjunto.casos, self.nome_caso_referencia)   
                df_temporal = indicadores_temporais.retorna_df_concatenado(unity, self.cenario)
                if(self.xsup < df_temporal["estagio"].max()):
                    df_temporal = df_temporal.loc[(df_temporal["estagio"] < self.xsup)]
                if(self.xinf > df_temporal["estagio"].min()):
                    df_temporal = df_temporal.loc[(df_temporal["estagio"] > self.xinf)]
                
                if(self.yinf is not None and self.ysup is None):
                    self.ysup = df_temporal["valor"].max()

                if(self.ysup is not None and self.yinf is None):
                    self.yinf = df_temporal["valor"].min() 

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
            titulo_padrao = conjUnity.titulo+" "+unity.titulo+" "+self.estudo
            tituloFigura = titulo_padrao if self.titulo == " " else self.titulo.replace("_", " ")
            if(flag_muitos_casos == 0):
                mapaFig = self.graficosConjunto.subplot_gera_grafico_linha_casos(mapaTemporal, conjUnity, unity, tituloFigura, self.subp_col, self.subp_lin, self.yinf, self.ysup, legEixoX = "estagios" )
                for titulo in mapaFig:
                    self.graficosConjunto.exportar(mapaFig[titulo], diretorio_saida_arg, titulo+self.estudo, self.largura, self.altura)

            mapaCronologico[unity] = pd.concat(listaCronologica)
            indicadores_temporais.exportar(pd.concat(listaCronologica), diretorio_saida_arg,  "cronologico_"+unity.titulo+"_"+self.estudo,)

            #mapaTemporal_1_est[unity] = pd.concat(listaTemporal_1_est)
            #indicadores_temporais.exportar(pd.concat(listaTemporal_1_est), diretorio_saida_arg,  "primeiro_est_"+conjUnity.titulo+"_"+unity.titulo+"_"+self.estudo)

            #mapaMedio[unity] = pd.concat(listaMedia)
            #indicadores_medios.exportar(pd.concat(listaMedia), diretorio_saida_arg,  "media_"+unity.titulo+"_"+self.estudo)
            
        if(self.cronologico == "True"):
            mapaGO = self.graficosConjunto.gera_grafico_linha(mapaCronologico, colx = self.eixox, cronologico = self.cronologico)
            figura = Figura(conjUnity, mapaGO, tituloFigura, self.yinf, self.ysup)
            self.graficosConjunto.exportar(figura.fig, diretorio_saida_arg, figura.titulo, self.largura, self.altura)
        #mapaGO = self.graficosConjunto.gera_grafico_linhas_diferentes_casos(mapaTemporal_1_est)
        #figura = Figura(conjUnity, mapaGO, "Primeiro Est "+conjUnity.titulo+self.estudo)
        #self.graficosConjunto.exportar(figura.fig, diretorio_saida_arg, figura.titulo)

        #mapaGO = self.graficosConjunto.gera_grafico_linhas_diferentes_casos(mapaMedio)
        #figura = Figura(conjUnity, mapaGO, "Media "+conjUnity.titulo+self.estudo)
        #self.graficosConjunto.exportar(figura.fig, diretorio_saida_arg, figura.titulo)

