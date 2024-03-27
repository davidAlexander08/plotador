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
        colX,
        lista_df,
        mapaCores,
        legendaEixoY:str,
        legendaEixoX:str,
        titulo: str,
    ) -> go.Figure:
        fig = go.Figure()

        print(lista_df)

        for elemento in lista_df:
            dfY = df[elemento].reset_index(drop=True)
            fig.add_trace(
                go.Scatter(
                    x = df[colX],
                    y = dfY,
                    name = elemento,
                    line = dict(color = mapaCores[elemento]),
                    showlegend=True,
                )
            )
        fig.update_layout(title=titulo)
        fig.update_xaxes(title=legendaEixoX)
        fig.update_yaxes(title=legendaEixoY)
        fig.update_layout(legend=dict(title_font_family="Times New Roman",
                              font=dict(size= 11))
                        )
        return fig



    def subplot_gera_grafico_linha_casos(
        self,
        conjuntoCasos,
        mapaConjuntoCasos,
        legendaEixoY:str,
        legendaEixoX:str,
        titulo: str,
    ) -> go.Figure:
        mapaFiguras = {}
        len_map = len(self.conjuntoCasos[0].casos)
        subplot_col = 4
        subplot_lin = 3
        fig_subplot = make_subplots(rows=subplot_lin, cols=subplot_col,subplot_titles=(" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "))
        contador_col = 1
        contador_lin = 1
        contador_titulo = 0
        for caso in mapaConjuntoCasos[list(mapaConjuntoCasos.keys())[0]]["caso"].unique():
            show = True if contador_titulo == 0 else False
            #print(caso)
            listaCasos = []
            for conjunto in conjuntoCasos:
                df_caso = mapaConjuntoCasos[conjunto.nome].loc[mapaConjuntoCasos[conjunto.nome]["caso"] == caso].copy()
                df_caso = df_caso.rename(columns={conjunto.nome: "valor"}).reset_index(drop = True)
                df_caso["caso"] = conjunto.nome
                listaCasos.append(df_caso)
            df_concat_casos = pd.concat(listaCasos)

            #fig = self.gera_grafico_linha_casos(conjuntoCasos, df_concat_casos, legendaEixoY , legendaEixoX, titulo+"_"+caso)
            #mapaFiguras[titulo+"_"+caso] = fig
            for conj in self.conjuntoCasos:
                dfY = df_concat_casos.loc[df_concat_casos["caso"] == conj.nome]["valor"].reset_index(drop=True)
                fig_subplot.add_trace(
                    go.Scatter(
                        x = dfY.index,
                        y = dfY,
                        name = conj.nome,
                        line = dict(color = conj.cor),
                        showlegend=show,
                    ), row = contador_lin, col = contador_col    )
                fig_subplot.update_xaxes(title=legendaEixoX, row = contador_lin, col = contador_col )
                fig_subplot.update_yaxes(title=legendaEixoY, row = contador_lin, col = contador_col )
            fig_subplot.layout.annotations[contador_titulo].update(text=caso)
            contador_titulo += 1
            contador_col += 1
            if(contador_col == subplot_col+1):
                contador_col = 1
                contador_lin += 1

        fig_subplot.update_layout(title = titulo, legend=dict(title_font_family="Times New Roman",
                              font=dict(size= 11)))
        mapaFiguras["subplot"+titulo] = fig_subplot
        return mapaFiguras