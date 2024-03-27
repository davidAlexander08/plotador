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


    def exportar(self, figura, diretorio_saida, nome_arquivo, W = 800, H = 600):
        Log.log().info("Gerando grafico "+nome_arquivo)
        figura.write_image(
            os.path.join(diretorio_saida, nome_arquivo+".png"),
            width=W,
            height=H)
        
    def gera_grafico_linhas_diferentes_casos(
        self,
        df,
        unidade,
        titulo: str,
        colY = "valor",
        colX = "caso",
    ) -> go.Figure:
        fig = go.Figure()
        lista_casos = df["caso"].unique()
        lista_conjuntos = df["conjunto"].unique()

        if(unidade.limInf is True):
            limInf = 0 if df["valor"].min() > 0 else df["valor"].min()*1.1
        else:
            limInf = None

        limSup = df["valor"].max()*1.1 if unidade.limSup is True else None 

        for conj in self.conjuntoCasos:
            df_conj = df.loc[(df["conjunto"] == conj.nome)]
            fig.add_trace(
            go.Scatter(
                x = df_conj[colX],
                y = df_conj[colY],
                name = conj.nome,
                line = dict(color = conj.cor),
                showlegend=True,
            )
        )

        fig.update_layout(title=titulo)
        fig.update_xaxes(title=unidade.legendaEixoX)
        fig.update_yaxes(title=unidade.legendaEixoY)
        fig.update_layout(legend=dict(title_font_family="Times New Roman",
                              font=dict(size= 11)),
                              yaxis=dict(range=[limInf,limSup])
                        )
        return fig



    def subplot_gera_grafico_linha_casos(
        self,
        mapaConjuntoCasos,
        unidade,
        titulo: str,
        colY = "valor",
        colX = "index"
    ) -> go.Figure:
        
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
                fig_subplot.update_xaxes(title=unidade.legendaEixoX, row = contador_lin, col = contador_col )
                fig_subplot.update_yaxes(title=unidade.legendaEixoY, row = contador_lin, col = contador_col )
                contador_col += 1
                if(contador_col == subplot_col+1):
                    contador_col = 1
                    contador_lin += 1
                fig_subplot.layout.annotations[contador_titulo].update(text=caso.nome)
                contador_titulo += 1

        fig_subplot.update_layout(title = titulo, legend=dict(title_font_family="Times New Roman",
                              font=dict(size= 11)))
        mapaFiguras["subplot"+titulo] = fig_subplot
        return mapaFiguras