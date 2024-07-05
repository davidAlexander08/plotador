import pandas as pd
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

import os
import json

class Temporal:


    def __init__(self, data, xinf, xsup,estagio, cenario, sintese, largura, altura, eixox, cronologico, labely, booltitulo, titulo, showlegend, labelx, argumentos, chave):
        self.xinf  = xinf
        self.xsup = xsup
        self.eixox = eixox
        self.estagio = estagio
        self.cenario = cenario
        self.sintese = sintese
        self.argumentos  = argumentos
        self.chave = chave
        self.largura = largura
        self.altura = altura
        self.cronologico = cronologico
        self.labely = labely
        self.labelx = labelx
        self.booltitulo = booltitulo
        self.titulo = titulo
        self.showlegend = showlegend
        self.estudo = data.estudo
        self.indicadores_temporais = IndicadoresTemporais(data.casos)
        self.graficos = Graficos(data)
        # Gera saídas do estudo
        diretorio_saida = f"resultados/{self.estudo}/temporal"
        os.makedirs(diretorio_saida, exist_ok=True)

        if(self.argumentos is not None and self.chave is None):
            print("FALTA DECLARAR A CHAVE DO ARGUMENTO")
            exit(1)
        if(self.chave is not None and self.argumentos is None):
            print("FALTA DECLARAR O ARGUMENTO DO ARGUMENTO")
            exit(1)
        if(self.chave is not None and self.argumentos is not None):
            lista_argumentos = self.argumentos.split(",")
            print(lista_argumentos)
            data.args = [Argumento(lista_argumentos, self.chave, "out")] 
            if(len(lista_argumentos) == 1 and self.titulo == " "): self.titulo = lista_argumentos[0]


        sinteses = data.sinteses if (self.sintese == "") else [Sintese(self.sintese)]
        for sts in sinteses:
            espacial = sts.sintese.split("_")[1] 
            if(espacial == "SIN"):
                arg = Argumento(None, None, "SIN")
                conj = ConjuntoUnidadeSintese(sts,arg , "estagios", data.limites, data.tamanho_texto)
                diretorio_saida_arg = diretorio_saida+"/"+arg.nome
                os.makedirs(diretorio_saida_arg, exist_ok=True)
                self.executa(conj,diretorio_saida_arg )
            else:
                for arg in data.args:
                    if(espacial == arg.chave):
                        conj = ConjuntoUnidadeSintese(sts, arg, "estagios", data.limites, data.tamanho_texto)
                        if(self.labely is not None):
                            conj.legendaEixoY = self.labely
                        if(self.labelx is not None):
                            conj.legendaEixoX = self.labelx
                        diretorio_saida_arg = diretorio_saida+"/"+arg.nome
                        os.makedirs(diretorio_saida_arg, exist_ok=True)
                        self.executa(conj,diretorio_saida_arg )
                        

 
    def executa(self, conjUnity, diretorio_saida_arg): 
        mapa_temporal = {}
        for unity in conjUnity.listaUnidades:
            df_temporal = self.indicadores_temporais.retorna_df_concatenado(unity, self.cenario)
            if(self.xsup < df_temporal["estagio"].max()):
                df_temporal = df_temporal.loc[(df_temporal["estagio"] < self.xsup)]
            if(self.xinf > df_temporal["estagio"].min()):
                df_temporal = df_temporal.loc[(df_temporal["estagio"] > self.xinf)]
            mapa_temporal[unity] = df_temporal
            self.indicadores_temporais.exportar(mapa_temporal[unity], diretorio_saida_arg,  "Temporal "+conjUnity.titulo+self.estudo)
        



        mapaGO = self.graficos.gera_grafico_linha(mapa_temporal, colx = self.eixox, cronologico = self.cronologico)

        titulo_padrao = "Temporal "+conjUnity.titulo+self.estudo
        tituloFigura = titulo_padrao if self.booltitulo == "True" else " "
        tituloFigura = titulo_padrao if self.titulo == " " else self.titulo.replace("_", " ")

        figura = Figura(conjUnity, mapaGO, tituloFigura)
        if(self.showlegend == "False"):
            figura.fig.update_layout(showlegend= False)
        self.graficos.exportar(figura.fig, diretorio_saida_arg, titulo_padrao, self.largura, self.altura)
        
        
        if(self.estagio != ""):
            mapaEst = {self.estagio:" Estagio "+str(self.estagio)} 
            
            for est in mapaEst:
                mapa_estagio = {}
                print(est)
                for unity in conjUnity.listaUnidades:
                    mapa_estagio[unity] = mapa_temporal[unity].loc[mapa_temporal[unity]["estagio"] == int(est)]
                    self.indicadores_temporais.exportar(mapa_estagio[unity], diretorio_saida_arg,  mapaEst[est]+"_"+unity.titulo+"_"+conjUnity.sintese.sintese+" "+self.estudo)
                        
                mapaGO = self.graficos.gera_grafico_barra(conjUnity, mapa_estagio, mapaEst[est]+conjUnity.titulo+" "+self.estudo)
                figura = Figura(conjUnity, mapaGO, mapaEst[est]+conjUnity.sintese.sintese+" "+self.estudo)
                self.graficos.exportar(figura.fig, diretorio_saida_arg, figura.titulo, self.largura, self.altura)


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
    
