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

import os
import json

class Tempo:

    #Faz gráficos de tempo de execução apenas
    def __init__(self, data):
        self.estudo = data.estudo
        self.eco_indicadores = EcoIndicadores(data.casos)
        self.graficos = Graficos(data.casos)
        # Gera saídas do estudo
        diretorio_saida = f"resultados/{self.estudo}/tempo"
        os.makedirs(diretorio_saida, exist_ok=True)
        
        df_temp = self.eco_indicadores.retorna_df_concatenado("TEMPO")
        df_temp["tempo"] = df_temp["tempo"] /(60*60)
        lista_color = []
        for caso in data.casos:
            lista_color.append(caso.cor)
        print(df_temp)
        df = df_temp.loc[(df_temp["etapa"] == "Calculo da Politica") & (df_temp["etapa"] == "Tempo Total")]
        fig = self.graficos.gera_grafico_barras_diferentes(df_temp, colX = "etapa", colY = "tempo", categorias = "caso", eixoX = "", eixoY = "minutos",
         aproximacao = 2, titulo = "Tempo de processamento", lista_cor = lista_color)
        self.graficos.exportar(fig, diretorio_saida, "Tempo"+self.estudo)
                        

