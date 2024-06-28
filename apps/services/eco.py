from typing import Dict
from apps.model.unidade import UnidadeSintese
from apps.graficos.graficos import Graficos
from apps.indicadores.indicadores_temporais import IndicadoresTemporais
from apps.model.caso import Caso
from apps.model.sintese import Sintese
from apps.model.argumento import Argumento
from apps.indicadores.eco_indicadores import EcoIndicadores
import os
import json

class Eco:
    def __init__(self, data):
        self.estudo = data.estudo
        self.casos = data.casos
        
        eco_indicadores = EcoIndicadores(casos)
        graficos = Graficos(casos)
        # Gera saídas do estudo
        diretorio_saida = f"resultados/{estudo}/eco"
        os.makedirs(diretorio_saida, exist_ok=True)

        for sts in data.sinteses:
            Log.log().info("Gerando eco "+ sts.sintese +" para o estudo: "+ estudo)
            eco = eco_indicadores.retorna_df_concatenado(sts.sintese)
            eco.to_csv(
                os.path.join(diretorio_saida, "eco_"+sts.sintese+"_"+estudo+".csv"),
                index=False,
            )

        df_custos = eco_indicadores.retorna_df_concatenado("CUSTOS")
        #df_custos = df_custos.loc[(df_custos["mean"] != 0)] #Remove colunas com 0
        df_custos = df_custos.loc[(df_custos["mean"] > 10)] #Remove colunas menores que 10, pois nao sao significantes
        df_custos = df_custos.sort_values(by="mean", ascending=False)
        df_custos = df_custos.round(0)
        fig = graficos.gera_grafico_barras_diferentes(df_custos, "parcela", "mean", "caso",  "parcelas", "R$", 0, "Custos Totais Casos")
        fig.write_image(
            os.path.join(diretorio_saida, "Newave_"+"Custos Totais Casos"+"_"+estudo+".png"),
            width=800,
            height=600,
        )
        for c in casos:
            df_plot = df_custos.loc[(df_custos["caso"] == c.nome)]
            fig = graficos.gera_grafico_barras_diferentes(df_plot, "parcela", "mean", "caso",  "parcelas", "R$", 0, "Custos Totais "+c.nome)
            fig.write_image(
                os.path.join(diretorio_saida, "Newave_"+"Custos Totais "+"_"+c.nome+"_"+estudo+".png"),
                width=800,
                height=600,
            )

        df_convergencia = eco_indicadores.retorna_df_concatenado("CONVERGENCIA")
        #lista = ["zinf","zsup"]
        #mapFormatLine = {"zinf": "dot", "zsup":"dash"}
        lista = ["zinf"]
        mapFormatLine = {"zinf": "dot"}
        fig = graficos.gera_grafico_linhas_diferentes(df_convergencia,lista, mapFormatLine, "R$ (10 6)", "iteracoes", "Convergencia")
        fig.write_image(
            os.path.join(diretorio_saida, "Newave_"+"Convergencias"+"_"+estudo+".png"),
            width=800,
            height=600,
        )
        
    def executa(self, unity, diretorio_saida_arg):
        pass
