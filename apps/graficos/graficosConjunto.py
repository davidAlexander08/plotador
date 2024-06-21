from typing import List
import pandas as pd

from apps.model.caso import Caso
from apps.utils.log import Log
import os
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
from plotly.subplots import make_subplots
from apps.model.unidade import UnidadeSintese
from apps.model.conjuntoCasos import ConjuntoCasos
pio.templates.default = "ggplot2"

class GraficosConjunto:

    def __init__(self, conjuntoCasos):
        self.conjuntoCasos = conjuntoCasos


    def exportar(self, figura, diretorio_saida, nome_arquivo, W = 2400, H = 1400):
        Log.log().info("Gerando grafico "+nome_arquivo)
        figura.write_image(
            os.path.join(diretorio_saida, nome_arquivo+".png"),
            width=W,
            height=H)
        

    def gera_grafico_linhas_artesanal(
        self,
        mapa,
        colY = "valor",
        colX = "caso" ):
        mapaGO = {}
        for conj in self.conjuntoCasos:  
            df = mapa[conj]
            listaGO = []
            listaGO.append(go.Scatter(
                                x = df[colX],
                                y = df[colY],
                                name = conj.nome,
                                line = dict(color = conj.cor),
                                showlegend=True,
                            )
            )
            mapaGO[unity] = listaGO
        return mapaGO


    def gera_grafico_linhas_diferentes_casos(
        self,
        mapa,
        colY = "valor",
        colX = "caso" ):
        mapaGO = {}
        for unity in mapa:  
            df = mapa[unity]
            listaGO = []
            for conj in self.conjuntoCasos:
                df_conj = df.loc[(df["conjunto"] == conj.nome)]
                listaGO.append(go.Scatter(
                                    x = df_conj[colX],
                                    y = df_conj[colY],
                                    name = conj.nome,
                                    line = dict(color = conj.cor),
                                    showlegend=unity.arg.show,
                                )
                )
            mapaGO[unity] = listaGO
        return mapaGO

    def gera_grafico_linha(
        self,
        mapa,
        cronologico, 
        coly = "valor",
        #colx = "estagio"
        colx = "estagio" ) :
        mapaGO = {}
        for unity in mapa:
            print(unity)
            print("SHOW: ", unity.arg.show)
            df = mapa[unity]
            listaGO = []
            for conj in self.conjuntoCasos:
                df_conj = df.loc[(df["conjunto"] == conj.nome)]
                listaGO.append(go.Scatter( 
                        x = df_conj[colx],
                        y = df_conj[coly],
                        name = conj.nome,
                        line = dict(color = conj.cor),
                        showlegend=unity.arg.show))
            mapaGO[unity] = listaGO
        return mapaGO


    def subplot_gera_grafico_linha_casos(
        self,
        mapaConjuntoCasos,
        conjUnity, 
        unidade,
        titulo: str,
        legEixoX = "",
        colY = "valor",
        colX = "index"
    ) -> go.Figure:

        legendaEixoX = conjUnity.legendaEixoX if legEixoX == "" else legEixoX
        
        mapaFiguras = {}
        subplot_col = 4
        subplot_lin = 3
        fig_subplot = make_subplots(rows=subplot_lin, cols=subplot_col,subplot_titles=(" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "))
        for conj in self.conjuntoCasos:
            df_conj = mapaConjuntoCasos[conj.nome]
            contador_col = 1
            contador_lin = 1
            contador_titulo = 0
            for caso in conj.casos:
                show = True if contador_titulo == 0 else False
                dfY = df_conj.loc[df_conj["caso"] == caso.nome]["valor"].reset_index(drop=True)
                dfY = dfY.reset_index(drop = False)
                fig_subplot.add_trace(
                    go.Scatter(
                        x = dfY[colX],
                        y = dfY[colY],
                        name = conj.nome,
                        line = dict(color = conj.cor),
                        showlegend=show,
                    ), row = contador_lin, col = contador_col    )
                fig_subplot.update_xaxes(title= legendaEixoX, row = contador_lin, col = contador_col )
                if(contador_lin == 1 and contador_col == 1):
                    fig_subplot.update_yaxes(title=conjUnity.legendaEixoY, row = contador_lin, col = contador_col )
                contador_col += 1
                if(contador_col == subplot_col+1):
                    contador_col = 1
                    contador_lin += 1
                fig_subplot.layout.annotations[contador_titulo].update(text=caso.nome)
                contador_titulo += 1

        fig_subplot.update_layout(title = titulo, 
                                  font=dict(size= conjUnity.tamanho_texto)
                                  )
        mapaFiguras["subplot"+titulo] = fig_subplot
        return mapaFiguras
