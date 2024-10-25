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
from apps.graficos.figura import Figura

pio.templates.default = "ggplot2"

class Graficos:
    """
    Realiza a geração dos gráficos utilizados na análise
    de escolha dos pares de CVaR para recalibração.
    """

    def __init__(self, data):
        self.casos = data.casos
        self.estudo = data.estudo
        self.pre_defined_colors = [
            "#BA0F30",
            "#ff4500",
            "orange",
            "yellow",
            "#64f2a4",
            "#18b76c",
            "green",
            "purple",
            "blue",
            "gray",
            "#20362b",
            "#232828",
            "#220f28",
            "#220f0c",
            "brown",
            "#0d0f0c",
            "#203607",
            "black",
        ]

    def exportar(self, figura, diretorio_saida, nome_arquivo, html, W = 1500, H = 1200):
        Log.log().info("Gerando grafico "+nome_arquivo)
        figura.write_image(
            os.path.join(diretorio_saida, nome_arquivo+".png"),
            width=W,
            height=H)

        if(html =="True"):
            figura.update_layout(width = int(W), height = int(H))
            figura.write_html(os.path.join(diretorio_saida, nome_arquivo+".html"))
    
    

    def gera_pareto_fast(
        self,
        eixo_x: pd.DataFrame,
        eixo_y: pd.DataFrame, 
        erro_x :pd.DataFrame,
        erro_y:pd.DataFrame,
        label_x: str,
        label_y: str,
        limSupY: int,
        limInfY:int,
        limSupX: int,
        limInfX:int,
        titulo: str,
        
    ) -> go.Figure:
        Log.log().info("Gerando pareto - "+titulo)
        fig = go.Figure()
        for c in self.casos:
            fig.add_trace(
                go.Scatter(
                    x = eixo_x.loc[ eixo_x["caso"] == c.nome]["valor"].tolist(),
                    y = eixo_y.loc[ eixo_y["caso"] == c.nome]["valor"].tolist(),
                    error_x = dict(type='data', array= erro_x.loc[ erro_x["caso"] == c.nome]["valor"].tolist()),
                    error_y = dict(type='data', array= erro_y.loc[ erro_y["caso"] == c.nome]["valor"].tolist()),
                    mode="markers+text",
                    text=c.nome,
                    marker_color=c.cor,
                    marker_symbol=c.marcador,
                    showlegend=False,
                )
            )
        fig.update_traces(textposition="top right")
        fig.update_traces(marker_size=20)
        fig.update_layout(title=titulo)
        fig.update_xaxes(title=label_x)
        fig.update_yaxes(title=label_y)

        if(limSupY is not None):
            fig.update_layout(yaxis_range=[limInfY,limSupY])
        if(limSupX is not None):
            fig.update_layout(xaxis_range=[limInfX,limSupX])
        return fig



    def gera_bar_custos(
        self,
        df: pd.DataFrame,
        titulo: str,
    ) -> go.Figure:
        Log.log().info("Gerando grafico barras de custos de violação")
        fig = go.Figure()

        indiceCores = 0
        for column in df:
            fig.add_trace(
                go.Bar(
                    x=df.index.tolist(),
                    y=df[column].tolist(),
                    marker_color=self.pre_defined_colors[indiceCores],
                    showlegend=True,
                    name=column,
                    visible=True,
                )
            )
            indiceCores += 1
        fig.add_trace(
            go.Scatter(
                x=df.index.tolist(),
                y=df.sum(axis=1).round(1).values,
                text=df.sum(axis=1).round(1).values,
                mode="text",
                textposition="top center",
                textfont=dict(
                    size=12,
                ),
                showlegend=False,
            )
        )

        fig.update_xaxes(title_text="casos")
        fig.update_yaxes(title_text="R$")
        fig.update_layout(
            title=titulo,
            barmode="stack",
        )

        return fig



    def gera_grafico_linhas_diferentes(
        self,
        df,
        lista_df,
        mapFormatLine,
        legendaEixoY:str,
        legendaEixoX:str,
        titulo: str,
        tamanho = 25
    ) -> go.Figure:
        fig = go.Figure()
        for c in self.casos:
            for elemento in lista_df:
                dfY = df.loc[(df["caso"] == c.nome)][elemento].reset_index(drop=True)
                fig.add_trace(
                    go.Scatter(
                        x = dfY.index,
                        y = dfY,
                        name = c.nome+"_"+elemento,
                        line = dict(color = c.cor, dash= mapFormatLine[elemento]),
                        showlegend=True,
                    )
                )
        fig.update_layout(title=titulo)
        fig.update_xaxes(title=legendaEixoX)
        fig.update_yaxes(title=legendaEixoY)
        fig.update_layout(legend=dict(title_font_family="Times New Roman",
                              font=dict(size= tamanho)
        ))
        return fig

    def gera_grafico_linha( 
        self,
        mapa,
        cronologico, 
        eixo_y2,
        coly = "valor",
        #colx = "estagio"
        colx = "estagio" ) :
        mapaGO = {}
        if(cronologico == "True"):
            for unity in mapa:
                df = mapa[unity]
                listaGO = []
                df = df.reset_index(drop = True)
                listaGO.append(go.Scatter( 
                        x = df[colx],
                        y = df[coly],
                        name = self.estudo,
                        showlegend=unity.arg.show))
                mapaGO[unity] = listaGO
        else:
            for unity in mapa:  
                df = mapa[unity]
                listaGO = []
                lista_casos = df["caso"].unique()
                for c in self.casos:
                    dfY = df.loc[df["caso"] == c.nome].reset_index(drop=True)
                    dfY = dfY.reset_index(drop = False)
                    modo = "lines" if c.marcador == None else "lines+markers"
                    listaGO.append(go.Scatter( 
                            x = dfY[colx],
                            y = dfY[coly],
                            mode=modo,
                            marker=dict( symbol=c.marcador ),
                            name = c.nome,
                            legendgroup=c.nome,
                            line = dict(color = c.cor, dash=c.dash),
                            showlegend=unity.arg.show))
                if(eixo_y2 == "True"):
                    for unity in mapa:  
                        df = mapa[unity]
                        lista_casos = df["caso"].unique()
                        df_caso_0 = df.loc[df["caso"] == lista_casos[0]].reset_index(drop=True)
                        df_caso_1 = df.loc[df["caso"] == lista_casos[1]].reset_index(drop=True)
                        df_valor = df_caso_0[coly] - df_caso_1[coly].reset_index(drop=True)
                        print(df_valor)
                        listaGO.append(go.Bar( 
                                x = df_caso_0[colx],
                                y = df_valor,
                                yaxis = "y2",
                                #text = df_valor.round(1).tolist(),
                                #textposition ="outside",
                                marker_color="gray",
                                name = lista_casos[0]+"-"+lista_casos[1],
                                showlegend=True))
                mapaGO[unity] = listaGO
        return mapaGO


    def gera_grafico_boxplot( 
        self,
        mapa,
        coly = "valor",
        colx = "estagio" ) :
        mapaGO = {}
        for unity in mapa:  
            df = mapa[unity]
            listaGO = []
            for c in self.casos:
                dfY = df.loc[df["caso"] == c.nome].reset_index(drop=True)
                dfY = dfY.reset_index(drop = False)
                print(dfY)
                listaGO.append(go.Box( 
                        x = list(map(str,dfY[colx].tolist())) ,
                        y =  dfY[coly].tolist(),
                        name = c.nome,
                        line = dict(color = c.cor),
                        boxpoints = False,
                        showlegend=unity.arg.show))
            mapaGO[unity] = listaGO
        return mapaGO



    def gera_grafico_barra(
        self,
        conjUnity,
        mapa,
        titulo:str,
        aproximacao = 1,
        coly = "valor",
        colx = "caso",
        ) -> go.Figure:

        mapaGO = {}
        for unity in mapa:  
            df = mapa[unity]
            listaGO = []
            listaGO.append(go.Bar(
            x=df[colx],
            y=df[coly],
            marker_color="#00a6ff",
            showlegend=False
            ))

            listaGO.append(go.Scatter(
            x=df[colx],
            y=df[coly],
            text=df[coly].round(aproximacao),
            mode="text",
            textposition="top center",
            textfont=dict(
                size=12,
            ),
            showlegend=False,
            ))

                #listaGO.append(go.Scatter( 
                #        x = dfY[colx],
                #        y = dfY[coly],
                #        name = c.nome,
                #        line = dict(color = c.cor),
                #        showlegend=unity.arg.show))

            mapaGO[unity] = listaGO
        return mapaGO



        #fig = go.Figure()
        #fig.add_trace(
        #    go.Bar(
        #        x=dfX,
        #        y=dfY,
        #        marker_color="#00a6ff",
        #        showlegend=False
        #    )
        #)
        #fig.add_trace(
        #    go.Scatter(
        #        x=dfX,
        #        y=dfY,
        #        text=dfY.round(aproximacao),
        #        mode="text",
        #        textposition="top center",
        #        textfont=dict(
        #            size=12,
        #        ),
        #        showlegend=False,
        #    )
        #)
        #
        #fig.update_xaxes(title_text=eixoX)
        #fig.update_yaxes(title_text=eixoY)
        #fig.update_layout(title=titulo)
        #return fig



    def gera_grafico_barras_diferentes(
        self,
        df: pd.DataFrame,
        colX,
        colY,
        categorias,
        eixoX:str,
        eixoY:str,
        aproximacao:int,
        titulo:str,
        lista_cor = [],
        tamanho = 25,
    ) -> go.Figure:
        colors = self.pre_defined_colors if (len(lista_cor) == 0 ) else lista_cor
        Log.log().info("Gerando grafico "+titulo)
        fig = go.Figure()
        indiceCor = 0
        for cat in df[categorias].unique():
            fig.add_trace(
                go.Bar(
                    x = df.loc[df[categorias] == cat][colX],
                    y = df.loc[df[categorias] == cat][colY],
                    text = df.loc[df[categorias] == cat][colY].round(aproximacao),
                    textposition = "outside",
                    name = cat,
                    textfont=dict(
                        size=tamanho,
                    ),
                    marker_color=colors[indiceCor],
                    showlegend=True
                )
            )
            indiceCor += 1
            


        fig.update_xaxes(title_text=eixoX)
        fig.update_yaxes(title_text=eixoY)
        fig.update_layout(font=dict(size= tamanho))
        fig.update_layout(title=titulo)
        return fig










    def gera_bar_decomp(
        self,
        df: pd.DataFrame,
        indice: int,
        titulo: str,
    ):
        estagio = df["estagio"].unique()[indice]
        df_graphic = df.loc[df["estagio"] == estagio]
        mapaFig = {}
        tamanhoTexto = 20
        color = "#00a6ff"

        Log.log().info("Gerando grafico barras decomp de CMO SE")
        fig = px.bar(
            df_graphic,
            x="caso",
            y="cmo_se_med",
            title=titulo + " CMO SE",
            text_auto=True,
        )
        fig.update_traces(
            textfont_size=tamanhoTexto,
            textangle=0,
            textposition="outside",
            cliponaxis=False,
            marker_color=color,
        )
        fig.update_yaxes(title="R$/MWh")
        mapaFig["cmo_se_med"] = fig

        Log.log().info("Gerando grafico barras decomp de CMO NE")
        fig = px.bar(
            df_graphic,
            x="caso",
            y="cmo_ne_med",
            title=titulo + " CMONE",
            text_auto=True,
        )
        fig.update_traces(
            textfont_size=tamanhoTexto,
            textangle=0,
            textposition="outside",
            cliponaxis=False,
            marker_color=color,
        )
        fig.update_yaxes(title="R$/MWh")
        mapaFig["cmo_ne_med"] = fig

        Log.log().info("Gerando grafico barras decomp de EARPF")
        fig = px.bar(
            df_graphic,
            x="caso",
            y="earm_med_perc",
            title=titulo + " Energia Armaz. Final Perc.",
            text_auto=True,
        )
        fig.update_traces(
            textfont_size=tamanhoTexto,
            textangle=0,
            textposition="outside",
            cliponaxis=False,
            marker_color=color,
        )
        fig.update_yaxes(title="%")
        mapaFig["earm_med_perc"] = fig

        Log.log().info("Gerando grafico barras decomp de EVERT")
        fig = px.bar(
            df_graphic,
            x="caso",
            y="vert_tot_med_mwmes",
            title=titulo + " Energia Vertida",
            text_auto=True,
        )
        fig.update_traces(
            textfont_size=tamanhoTexto,
            textangle=0,
            textposition="outside",
            cliponaxis=False,
            marker_color=color,
        )
        fig.update_yaxes(title="MWmes")
        mapaFig["evert_tot_med_mwmes"] = fig

        Log.log().info("Gerando grafico barras decomp de G. Term.")
        fig = px.bar(
            df_graphic,
            x="caso",
            y="gterm_med_mwmes",
            title=titulo + " Geracao Termica",
            text_auto=True,
        )
        fig.update_traces(
            textfont_size=tamanhoTexto,
            textangle=0,
            textposition="outside",
            cliponaxis=False,
            marker_color=color,
        )
        fig.update_yaxes(title="MWmes")
        mapaFig["gterm_med_mwmes"] = fig

        Log.log().info("Gerando grafico barras decomp de G. Hidr.")
        fig = px.bar(
            df_graphic,
            x="caso",
            y="ghid_med_mwmes",
            title=titulo + " Geracao Hidreletrica",
            text_auto=True,
        )
        fig.update_traces(
            textfont_size=tamanhoTexto,
            textangle=0,
            textposition="outside",
            cliponaxis=False,
            marker_color=color,
        )
        
        fig.update_yaxes(title="MWmes")
        mapaFig["ghid_med_mwmes"] = fig


        Log.log().info("Gerando grafico barras decomp de EVER TURB")
        fig = px.bar(
            df_graphic,
            x="caso",
            y="evert",
            title=titulo + " Vertimento Turbinável",
            text_auto=True,
        )
        fig.update_traces(
            textfont_size=tamanhoTexto,
            textangle=0,
            textposition="outside",
            cliponaxis=False,
            marker_color=color,
        )
        
        fig.update_yaxes(title="MWmes")
        mapaFig["evert"] = fig


        Log.log().info("Gerando grafico barras decomp de EVER NTURB")
        fig = px.bar(
            df_graphic,
            x="caso",
            y="evernt",
            title=titulo + " Vertimento Não Turbinável",
            text_auto=True,
        )
        fig.update_traces(
            textfont_size=tamanhoTexto,
            textangle=0,
            textposition="outside",
            cliponaxis=False,
            marker_color=color,
        )
        
        fig.update_yaxes(title="MWmes")
        mapaFig["evernt"] = fig
        return mapaFig





    def gera_grafico_barra_primeira_semana_CREF_Decomp(
        self,
        df_dataInicial: pd.DataFrame,
        df_valores : pd.DataFrame,
        df_CREF: pd.DataFrame,
        grandeza: str,
        unidade: str,
        titulo: str
        ) ->go.Figure:

        df_verde = df_CREF.loc[df_CREF["BANDEIRA"] == "VERDE"]
        df_amarelo = df_CREF.loc[df_CREF["BANDEIRA"] == "AMARELO"]
        df_vermelho = df_CREF.loc[df_CREF["BANDEIRA"] == "VERMELHO"]
            
        df_verde_filtro = df_verde.loc[(df_verde["data"] >= df_dataInicial.iloc[:, 0].tolist()[0]) & (df_verde["data"] <= df_dataInicial.iloc[:, 0].tolist()[-1])]
        df_amarelo_filtro = df_amarelo.loc[(df_amarelo["data"] >= df_dataInicial.iloc[:, 0].tolist()[0]) & (df_amarelo["data"] <= df_dataInicial.iloc[:, 0].tolist()[-1])]
        df_vermelho_filtro = df_vermelho.loc[(df_vermelho["data"] >= df_dataInicial.iloc[:, 0].tolist()[0]) & (df_vermelho["data"] <= df_dataInicial.iloc[:, 0].tolist()[-1])]

        df_val = df_valores.iloc[0,:]
        df_verde = df_verde_filtro.iloc[0,:]
        df_amarelo = df_amarelo_filtro.iloc[0,:]
        df_vermelho =df_vermelho_filtro.iloc[0,:]
        tamanhoCasos = len(df_valores.columns.values.tolist())
            
        fig = self.gera_grafico_barra(
            df_val.values , 
            df_valores.columns.values.tolist(), 
            "casos", 
            unidade,
            1,
            titulo
        )

        fig.add_trace(
            go.Scatter(
                x=df_valores.columns.values.tolist(),
                y=[df_verde.at[grandeza]]*tamanhoCasos,
                name = "CREF_"+df_verde.at["BANDEIRA"],
                line = dict(color = "green"),
                showlegend=True,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df_valores.columns.values.tolist(),
                y=[df_amarelo.at[grandeza]]*tamanhoCasos,
                name = "CREF_"+df_amarelo.at["BANDEIRA"],
                line = dict(color = "yellow"),
                showlegend=True,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df_valores.columns.values.tolist(),
                    y=[df_vermelho.at[grandeza]]*tamanhoCasos,
                name = "CREF_"+df_vermelho.at["BANDEIRA"],
                line = dict(color = "red"),
                showlegend=True,
            )
        )
            
        return fig




    def gera_graficos_linha_mean_p10_p90_CREF(self,
        df: pd.DataFrame,
        df_CREF: pd.DataFrame,
        grandeza: str,
        unidade: str,
        titulo: str,
        comando: str,
    ) -> go.Figure:
        Log.log().info("Gerando grafico "+titulo)
        fig = go.Figure()
        #print(df)
        for c in self.casos:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["mean"+c.nome],
                    name = "mean_"+c.nome,
                    line = dict(color = c.cor, width = 2),
                    showlegend=True,
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["p10"+c.nome],
                    name = "p10_"+c.nome,
                    line = dict(color = c.cor, dash = "dash", width = 1),
                    showlegend=True,
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["p90"+c.nome],
                    name = "p90_"+c.nome,
                    line = dict(color = c.cor, dash = "dot", width = 1),
                    showlegend=True,
                )
            )

        df_dataInicial = df["dataInicio"+self.casos[0].nome]
        df_verde = df_CREF.loc[df_CREF["BANDEIRA"] == "VERDE"]
        df_amarelo = df_CREF.loc[df_CREF["BANDEIRA"] == "AMARELO"]
        df_vermelho = df_CREF.loc[df_CREF["BANDEIRA"] == "VERMELHO"]

        if (comando is None):
            
            df_verde_filtro = df_verde.loc[(df_verde["data"] >= df_dataInicial.iloc[0]) & (df_verde["data"] <= df_dataInicial.iloc[-1])]
            df_amarelo_filtro = df_amarelo.loc[(df_amarelo["data"] >= df_dataInicial.iloc[0]) & (df_amarelo["data"] <= df_dataInicial.iloc[-1])]
            df_vermelho_filtro = df_vermelho.loc[(df_vermelho["data"] >= df_dataInicial.iloc[0]) & (df_vermelho["data"] <= df_dataInicial.iloc[-1])]
        if(comando == "2020" or comando == "2021" or comando == "2022" or comando == "2023" or comando == "2024" or comando  == "ADEQUA"):
            if(comando == "ADEQUA"):
                ano_vigente = str(df_dataInicial.iloc[:, 0].tolist()[0].year)
                comando = ano_vigente
            df_verde_filtro_ano = df_verde.loc[(df_verde["data"] >= pd.Timestamp(comando+"-01-01")) & (df_verde["data"] <= pd.Timestamp(comando+"-12-31"))]
            df_amarelo_filtro_ano = df_amarelo.loc[(df_amarelo["data"] >= pd.Timestamp(comando+"-01-01")) & (df_amarelo["data"] <= pd.Timestamp(comando+"-12-31"))]
            df_vermelho_filtro_ano = df_vermelho.loc[(df_vermelho["data"] >= pd.Timestamp(comando+"-01-01")) & (df_vermelho["data"] <= pd.Timestamp(comando+"-12-31"))]
            df_verde_filtro = df_verde_filtro_ano
            df_amarelo_filtro = df_amarelo_filtro_ano
            df_vermelho_filtro = df_vermelho_filtro_ano
            for i in range(0,4):
                df_verde_filtro = pd.concat([df_verde_filtro, df_verde_filtro_ano], ignore_index=True)
                df_amarelo_filtro = pd.concat([df_amarelo_filtro, df_amarelo_filtro_ano], ignore_index=True)
                df_vermelho_filtro = pd.concat([df_vermelho_filtro, df_vermelho_filtro_ano], ignore_index=True)

        
        df_verde_filtro = df_verde_filtro.reset_index(drop=True)
        df_amarelo_filtro = df_amarelo_filtro.reset_index(drop=True)
        df_vermelho_filtro = df_vermelho_filtro.reset_index(drop=True)
        
        fig.add_trace(
            go.Scatter(
                x=df_verde_filtro.index,
                y=df_verde_filtro[grandeza],
                name = "CREF_"+df_verde_filtro["BANDEIRA"].tolist()[0],
                line = dict(color = "green"),
                showlegend=True,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df_amarelo_filtro.index,
                y=df_amarelo_filtro[grandeza],
                name = "CREF_"+df_amarelo_filtro["BANDEIRA"].tolist()[0],
                line = dict(color = "yellow"),
                showlegend=True,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df_vermelho_filtro.index,
                y=df_vermelho_filtro[grandeza],
                name = "CREF_"+df_vermelho_filtro["BANDEIRA"].tolist()[0],
                line = dict(color = "red"),
                showlegend=True,
            )
        )
        
        fig.update_layout(title=titulo)
        fig.update_xaxes(title="estagios")
        fig.update_yaxes(title=unidade)
        return fig



    def gera_graficos_linha_Newave_CREF(self,
        df: pd.DataFrame,
        df_CREF: pd.DataFrame,
        grandeza: str,
        unidade: str,
        titulo: str,
        comando: str,
    ) -> go.Figure:
        Log.log().info("Gerando grafico "+titulo)
        fig = go.Figure()
        df_dataInicial = df["dataInicio"].reset_index(drop=True)
        df_valores = df["valor"]
        for c in self.casos:
            valores = df.loc[df["caso"] == c.nome]["valor"]
            fig.add_trace(
                go.Scatter(
                    x=valores.reset_index(drop=True).index,
                    y=valores,
                    name = c.nome,
                    line = dict(color = c.cor),
                    showlegend=True,
                )
            )

        
        df_verde = df_CREF.loc[df_CREF["BANDEIRA"] == "VERDE"]
        df_amarelo = df_CREF.loc[df_CREF["BANDEIRA"] == "AMARELO"]
        df_vermelho = df_CREF.loc[df_CREF["BANDEIRA"] == "VERMELHO"]
        if (comando is None):
            
            df_verde_filtro = df_verde.loc[(df_verde["data"] >= df_dataInicial.tolist()[0]) & (df_verde["data"] <= df_dataInicial.tolist()[-1])]
            df_amarelo_filtro = df_amarelo.loc[(df_amarelo["data"] >= df_dataInicial.tolist()[0]) & (df_amarelo["data"] <= df_dataInicial.tolist()[-1])]
            df_vermelho_filtro = df_vermelho.loc[(df_vermelho["data"] >= df_dataInicial.tolist()[0]) & (df_vermelho["data"] <= df_dataInicial.tolist()[-1])]
        if(comando == "2020" or comando == "2021" or comando == "2022" or comando == "2023" or comando == "2024" or comando  == "ADEQUA"):
            if(comando == "ADEQUA"):
                ano_vigente = str(df_dataInicial.tolist()[0].year)
                comando = ano_vigente
            df_verde_filtro_ano = df_verde.loc[(df_verde["data"] >= pd.Timestamp(comando+"-01-01")) & (df_verde["data"] <= pd.Timestamp(comando+"-12-31"))]
            df_amarelo_filtro_ano = df_amarelo.loc[(df_amarelo["data"] >= pd.Timestamp(comando+"-01-01")) & (df_amarelo["data"] <= pd.Timestamp(comando+"-12-31"))]
            df_vermelho_filtro_ano = df_vermelho.loc[(df_vermelho["data"] >= pd.Timestamp(comando+"-01-01")) & (df_vermelho["data"] <= pd.Timestamp(comando+"-12-31"))]
            df_verde_filtro = df_verde_filtro_ano
            df_amarelo_filtro = df_amarelo_filtro_ano
            df_vermelho_filtro = df_vermelho_filtro_ano
            for i in range(0,4):
                df_verde_filtro = pd.concat([df_verde_filtro, df_verde_filtro_ano], ignore_index=True)
                df_amarelo_filtro = pd.concat([df_amarelo_filtro, df_amarelo_filtro_ano], ignore_index=True)
                df_vermelho_filtro = pd.concat([df_vermelho_filtro, df_vermelho_filtro_ano], ignore_index=True)

        
        df_verde_filtro = df_verde_filtro.reset_index(drop=True)
        df_amarelo_filtro = df_amarelo_filtro.reset_index(drop=True)
        df_vermelho_filtro = df_vermelho_filtro.reset_index(drop=True)
        
        fig.add_trace(
            go.Scatter(
                x=df_verde_filtro.index,
                y=df_verde_filtro[grandeza],
                name = "CREF_"+df_verde_filtro["BANDEIRA"].tolist()[0],
                line = dict(color = "green"),
                showlegend=True,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df_amarelo_filtro.index,
                y=df_amarelo_filtro[grandeza],
                name = "CREF_"+df_amarelo_filtro["BANDEIRA"].tolist()[0],
                line = dict(color = "yellow"),
                showlegend=True,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df_vermelho_filtro.index,
                y=df_vermelho_filtro[grandeza],
                name = "CREF_"+df_vermelho_filtro["BANDEIRA"].tolist()[0],
                line = dict(color = "red"),
                showlegend=True,
            )
        )
        
        fig.update_layout(title=titulo)
        fig.update_xaxes(title="estagios")
        fig.update_yaxes(title=unidade)
        return fig




    def gera_graficos_linha_Decomp_CREF(self,
        df_dataInicial: pd.DataFrame,
        df_valores : pd.DataFrame,
        df_CREF: pd.DataFrame,
        grandeza: str,
        unidade: str,
        titulo: str
    ) -> go.Figure:
        Log.log().info("Gerando grafico "+titulo)
        fig = go.Figure()
        for c in self.casos:
            fig.add_trace(
                go.Scatter(
                    x=df_valores.index,
                    y=df_valores[c.nome],
                    name = c.nome,
                    line = dict(color = c.cor),
                    showlegend=True,
                )
            )

        
        df_verde = df_CREF.loc[df_CREF["BANDEIRA"] == "VERDE"]
        df_amarelo = df_CREF.loc[df_CREF["BANDEIRA"] == "AMARELO"]
        df_vermelho = df_CREF.loc[df_CREF["BANDEIRA"] == "VERMELHO"]


        df_verde_filtro = df_verde.loc[(df_verde["data"] >= df_dataInicial.iloc[:, 0].tolist()[0]) & (df_verde["data"] <= df_dataInicial.iloc[:, 0].tolist()[-1])]
        df_amarelo_filtro = df_amarelo.loc[(df_amarelo["data"] >= df_dataInicial.iloc[:, 0].tolist()[0]) & (df_amarelo["data"] <= df_dataInicial.iloc[:, 0].tolist()[-1])]
        df_vermelho_filtro = df_vermelho.loc[(df_vermelho["data"] >= df_dataInicial.iloc[:, 0].tolist()[0]) & (df_vermelho["data"] <= df_dataInicial.iloc[:, 0].tolist()[-1])]

        df_verde_filtro = df_verde_filtro.reset_index(drop=True)
        df_amarelo_filtro = df_amarelo_filtro.reset_index(drop=True)
        df_vermelho_filtro = df_vermelho_filtro.reset_index(drop=True)
        tamanhoLista = len(df_dataInicial[df_dataInicial.columns[0]].to_list())
        for i in range(1,tamanhoLista-1):
            df_verde_filtro = pd.concat([df_verde_filtro.iloc[:1],df_verde_filtro.loc[:]]).reset_index(drop=True)
            df_amarelo_filtro = pd.concat([df_amarelo_filtro.iloc[:1],df_amarelo_filtro.loc[:]]).reset_index(drop=True)
            df_vermelho_filtro = pd.concat([df_vermelho_filtro.iloc[:1],df_vermelho_filtro.loc[:]]).reset_index(drop=True)


        fig.add_trace(
            go.Scatter(
                x=df_verde_filtro.index,
                y=df_verde_filtro[grandeza],
                name = "CREF_"+df_verde_filtro["BANDEIRA"].tolist()[0],
                line = dict(color = "green"),
                showlegend=True,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df_amarelo_filtro.index,
                y=df_amarelo_filtro[grandeza],
                name = "CREF_"+df_amarelo_filtro["BANDEIRA"].tolist()[0],
                line = dict(color = "yellow"),
                showlegend=True,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df_vermelho_filtro.index,
                y=df_vermelho_filtro[grandeza],
                name = "CREF_"+df_vermelho_filtro["BANDEIRA"].tolist()[0],
                line = dict(color = "red"),
                showlegend=True,
            )
        )
        
        fig.update_layout(title=titulo)
        fig.update_xaxes(title="estagios")
        fig.update_yaxes(title=unidade)
        return fig
