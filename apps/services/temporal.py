from typing import Dict
from apps.model.unidade import UnidadeSintese
from apps.model.conjuntoUnidade import ConjuntoUnidadeSintese
from apps.graficos.graficos import Graficos
from apps.indicadores.indicadores_temporais import IndicadoresTemporais
from apps.model.caso import Caso
from apps.model.sintese import Sintese
from apps.model.argumento import Argumento
from apps.model.unidadeArgumental import UnidadeArgumental

import os
import json

class Temporal:


    def __init__(self, data):
        self.estudo = data.estudo
        self.indicadores_temporais = IndicadoresTemporais(data.casos)
        self.graficos = Graficos(data.casos)
        # Gera saídas do estudo
        diretorio_saida = f"resultados/{self.estudo}/temporal"
        os.makedirs(diretorio_saida, exist_ok=True)
        
        for sts in data.sinteses:
            espacial = sts.sintese.split("_")[1]
            if(espacial == "SIN"):
                arg = Argumento(None, None, "SIN")
                diretorio_saida_arg = diretorio_saida+"/"+espacial
                os.makedirs(diretorio_saida_arg, exist_ok=True)
                conj = ConjuntoUnidadeSintese(sts, Argumento(None, None, "SIN"), "estagios", data.lim_sup, data.lim_inf, data.tamanho_texto)
                self.executa(conj,diretorio_saida_arg )
            else:
                for arg in data.args:
                    if(espacial == arg.chave):
                        diretorio_saida_arg = diretorio_saida+"/"+arg.chave
                        os.makedirs(diretorio_saida_arg, exist_ok=True)
                        conj = ConjuntoUnidadeSintese(sts, arg, "estagios", data.lim_sup, data.lim_inf, data.tamanho_texto)
                        self.executa(conj,diretorio_saida_arg )
                        


    def executa(self, conjUnity, diretorio_saida_arg):
        mapa_temporal = {}
        for unity in conjUnity.listaUnidades:
            mapa_temporal[unity] = self.indicadores_temporais.retorna_df_concatenado(unity)
            self.indicadores_temporais.exportar(mapa_temporal[unity], diretorio_saida_arg,  unity.titulo+"_temporal_"+self.estudo)
        
        fig = self.graficos.gera_grafico_linha(conjUnity, mapa_temporal, conjUnity.arg.nome+" Temporal "+self.estudo)
        self.graficos.exportar(fig, diretorio_saida_arg, "temporal_"+self.estudo)
        
        #df_unity_2_mes = self.indicadores_temporais.retorna_df_concatenado_medio_2_mes(unity)
        #self.indicadores_temporais.exportar(df_unity_2_mes, diretorio_saida_arg,  unity.titulo+"_temporal_2_mes_"+self.estudo)
        
        #fig = self.graficos.gera_grafico_barra(df_unity_2_mes["valor"], df_unity_2_mes["caso"],  unity.legendaEixoX, unity.legendaEixoY, 2, unity.titulo+"2_mes")
        #self.graficos.exportar(fig, diretorio_saida_arg, unity.titulo+"_temporal_2_mes_"+self.estudo)






            #unity = UnidadeSintese("EARPF_SIN_EST", None, "%", "Energia_Armazenada_Percentual_Final_SIN_CREF "+estudo)
            #df_unity = indicadores_temporais.retorna_df_concatenado(unity)
            #graficos.gera_graficos_linha_Newave_CREF(df_unity, indicadores_temporais.df_cref, "EARPF", unity.legendaEixoY, unity.titulo, None).write_image(
            #    os.path.join(diretorio_saida, "SIN_EARPF_CREF"+estudo+".png"),
            #    width=800,
            #    height=600
            #    )
            #graficos.gera_graficos_linha_Newave_CREF(df_unity, indicadores_temporais.df_cref, "EARPF", unity.legendaEixoY, unity.titulo+"_2024", "2024").write_image(
            #    os.path.join(diretorio_saida, "SIN_EARPF_CREF_2024"+estudo+".png"),
            #    width=800,
            #    height=600
            #    )
            #graficos.gera_graficos_linha_Newave_CREF(df_unity, indicadores_temporais.df_cref, "EARPF", unity.legendaEixoY, unity.titulo+"_Ano_Vigente", "ADEQUA").write_image(
            #    os.path.join(diretorio_saida, "SIN_EARPF_CREF_AnoCaso"+estudo+".png"),
            #    width=800,
            #    height=600
            #    )
            #df_EARPF_mean_p10_p90 = indicadores_temporais.gera_df_mean_p10_p90("EARPF_SIN_EST")
            #graficos.gera_graficos_linha_mean_p10_p90_CREF(df_EARPF_mean_p10_p90,indicadores_temporais.df_cref, "EARPF", "%", "Energia Armazenada Cenarios CREF"+estudo, None ).write_image(
            #    os.path.join(diretorio_saida, "Energia_Armazenada_Media_P10_P90_"+estudo+".png"),
            #    width=800,
            #    height=600
            #    )
    
