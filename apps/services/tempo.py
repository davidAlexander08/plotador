from typing import Dict
from apps.model.unidade import UnidadeSintese
from apps.model.conjuntoUnidade import ConjuntoUnidadeSintese
from apps.graficos.graficos import Graficos
from apps.indicadores.indicadores_temporais import IndicadoresTemporais
from apps.model.caso import Caso
from apps.model.sintese import Sintese
from apps.model.argumento import Argumento
from apps.model.unidadeArgumental import UnidadeArgumental
from apps.graficos.figura import Figura
from apps.indicadores.eco_indicadores import EcoIndicadores
import pandas as pd
import os
import json

class Tempo:

    #Faz gráficos de tempo de execução apenas
    def __init__(self, data, largura, altura, html, outpath, titulo, tamanho):
        self.largura = largura
        self.altura = altura
        self.estudo = data.estudo
        self.html = html
        self.titulo = titulo
        self.tamanho = int(tamanho)
        self.eco_indicadores = EcoIndicadores(data.casos)
        self.graficos = Graficos(data)
        # Gera saídas do estudo
        diretorio_saida = f"resultados/{self.estudo}/tempo" if outpath is None else outpath
        print(diretorio_saida)
        os.makedirs(diretorio_saida, exist_ok=True)
        
        df_temp = self.eco_indicadores.retorna_df_concatenado("TEMPO")
        print(df_temp)
        lista_color = []
        temp = []
        for caso in data.casos:
            df_caso = df_temp.loc[(df_temp["caso"] == caso.nome)]
            df_caso["tempo"] = df_caso["tempo"] /(60)
            lista_color.append(caso.cor)
            if(caso.modelo == "NEWAVE"):
                #temp.append(df_temp.loc[(df_temp["etapa"] == "Calculo da Politica") ])
                temp.append(df_caso.loc[(df_caso["etapa"] == "Tempo Total")])
            if(caso.modelo == "DESSEM"):
                #print(df_caso)
                df = df_caso.groupby(['caso']).sum().drop(["etapa","modelo"],axis = 1).reset_index(drop=False)
                temp.append(df)
        df = pd.concat(temp).reset_index(drop = True)
        print(df)

        self.eco_indicadores.exportar(df, diretorio_saida,"Tempo"+self.estudo )
        titulo_tempo = "Tempo de processamento"+" "+self.estudo if self.titulo == " " else self.titulo.replace("_"," ")
        fig = self.graficos.gera_grafico_barras_diferentes(df, colX = "caso", colY = "tempo", categorias = "caso",tamanho = self.tamanho, eixoX = "", eixoY = "minutos",
         aproximacao = 2, titulo = titulo_tempo, lista_cor = lista_color)
        self.graficos.exportar(fig, diretorio_saida, titulo_tempo, self.html, self.largura, self.altura)
                        
