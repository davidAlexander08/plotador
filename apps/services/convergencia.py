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

class Convergencia:

    #Faz gráficos de tempo de execução apenas
    def __init__(self, data, largura, altura, html, outpath, titulo, tamanho):
        self.largura = largura
        self.altura = altura
        self.estudo = data.estudo
        self.html = html
        self.titulo = titulo
        self.tamanho = int(tamanho) if tamanho is not None else 25
        self.eco_indicadores = EcoIndicadores(data.casos)
        self.graficos = Graficos(data)
        # Gera saídas do estudo
        diretorio_saida = f"resultados/{self.estudo}/convergencia" if outpath is None else outpath
        print(diretorio_saida)
        os.makedirs(diretorio_saida, exist_ok=True)
        
        df_convergencia = self.eco_indicadores.retorna_df_concatenado("CONVERGENCIA")
        self.eco_indicadores.exportar(df_convergencia, diretorio_saida,"Convergencia"+self.estudo )
        titulo_grafico = "Convergencia "+self.estudo if self.titulo == " " else self.titulo.replace("_"," ")
        lista = ["zinf"]
        mapFormatLine = {"zinf": "dot"}
        fig = self.graficos.gera_grafico_linhas_diferentes(df_convergencia,lista, mapFormatLine, "R$ (10 6)", "iteracoes", titulo_grafico, tamanho = self.tamanho)
        self.graficos.exportar(fig, diretorio_saida, titulo_grafico, self.html, self.largura, self.altura)
                        
