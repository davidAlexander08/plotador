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
from inewave.newave import Ree
from inewave.nwlistcf import Nwlistcfrel
from inewave.nwlistcf import Estados
import plotly.express as px
import pandas as pd
import os
import json
import plotly.graph_objects as go
import plotly.io as pio

class NWLISTCF:


    def __init__(self, data, xinf, xsup, largura, altura, eco, yinf, ysup):
        self.xinf = xinf
        self.xsup = xsup
        self.largura = largura
        self.altura = altura
        self.eco = eco
        self.yinf = yinf
        self.ysup = ysup

        self.estudo = data.estudo
        self.casos = data.casos
        self.indicadores_temporais = IndicadoresTemporais(data.casos)
        self.graficos = Graficos(data)
        diretorio_saida = f"resultados/{self.estudo}/nwlistcf"
        os.makedirs(diretorio_saida, exist_ok=True)

        set_modelos =set({})
        for caso in self.casos:
            set_modelos.add(caso.modelo)
        if(len(set_modelos) != 1):
            print("ERRO: Tentativa de plotar NWLISTCF Com mais de um modelo no JSON")
            exit(1)
        if(len(self.casos) != 1):
            print("ERRO: Tentativa de plotar NWLISTCF Com mais de um caso no JSON")
            exit(1)
        modelo = list(set_modelos)[0]

        for arg in data.args:
            if(arg.chave == "UHE"):
                sts = Sintese("VAGUA_UHE_EST") #SINTESE DUMMY
                conj = ConjuntoUnidadeSintese(sts, arg, "estagios", data.limites, data.tamanho_texto)
                for unity in conj.listaUnidades:
                    if(modelo == "NEWAVE"):
                        lista_df_casos_nwlistcf = []
                        for caso in self.casos:
                            print("ENTROU AQUI")
                            df = self.processa_NWLISTCF(unity, caso)
                            lista_df_casos_nwlistcf.append(df)
                        df_nwlistcf_rees = pd.concat(lista_df_casos_nwlistcf)
                        df_nwlistcf_rees.to_csv(diretorio_saida+"/df_nwlistcf_rees"+self.estudo+".csv")

                        series = df_nwlistcf_rees["serie"].unique()
                        iteracoes = df_nwlistcf_rees["iter"].unique()
                        periodos = df_nwlistcf_rees["PERIODO"].unique()
                        lista_rees = df_nwlistcf_rees["REE"].unique()

                        lista_df_casos_estados = []
                        for caso in self.casos:
                            df_est = self.processa_ESTADOS(unity, caso)
                            lista_df_casos_estados.append(df_est)
                        df_estados_rees = pd.concat(lista_df_casos_estados)
                        df_estados_rees.to_csv(diretorio_saida+"/df_estados_rees"+self.estudo+".csv")



                        for u_ree in lista_rees:
                            df_nwlistcf_ree = df_nwlistcf_rees.loc[(df_nwlistcf_rees["REE"] == u_ree) & (df_nwlistcf_rees["iter"] != 1)]
                            df_estados_ree = df_estados_rees.loc[(df_estados_rees["REE"] == u_ree) & (df_estados_rees["ITEc"] != 1)]
                            #EVOLUCAO TEMPORAL DO PIV POR SERIE UMA LINHA PARA CADA ITERACAO
                            lista_series = list(range(1,201))
                            Variavel  = "PIEARM"
                            for ser in lista_series:
                                print("IMPRIMINDO GRAFICO DA SERIE: ", ser)
                                df_serie = df_nwlistcf_ree.loc[(df_nwlistcf_ree["serie"] == ser) & (df_nwlistcf_ree["iter"] != 1) ].copy()
                                fig = go.Figure()
                                lista_per = df_serie["PERIODO"].unique()
                                lista_iter = df_serie["iter"].unique()
                                degradee = 1.0/(len(lista_iter) + 1)
                                tonalidade = 0.95
                                for it in lista_iter:
                                    df_iter = df_serie.loc[(df_serie["iter"] == it)].copy()
                                    ly = df_iter[Variavel].tolist()
                                    fig.add_trace(go.Scatter( y = ly, x = lista_per, name = str(it), marker_color = "rgba(0,0,155,"+str(tonalidade)+")"))
                                    tonalidade -= degradee
                                fig.update_layout(title="PIs Por Iteracao Temporal "+str(REE) + " Serie "+str(ser))
                                fig.update_xaxes(title_text="Periodos")
                                fig.update_yaxes(title_text="R$/MWh")
                                #fig.update_yaxes(range=[-4000,0])
                                fig.update_yaxes(range=[self.yinf,self.ysup])
                                fig.update_xaxes(range=[self.xinf,self.xsup])
                                fig.update_layout(font=dict(size= data.tamanho_texto), showlegend=True)
                                fig.write_image(
                                    os.path.join(diretorio_saida+"/36_iteracao_linhas_"+str(REE)+"_serie_"+str(ser)+"_temporal.png"),
                                    width=self.largura,
                                    height=self.altura)
                            #FIM EVOLUCAO TEMPORAL DO PIV POR SERIE



                            #BOXPLOT PARA CADA PERIODO
                            print("IMPRIMINDO GRAFICO BOXPLOT")

                            Variavel  = "PIEARM"
                            fig = go.Figure()
                            periodos_artificial = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]
                            for per in periodos_artificial:
                                df_per = df_nwlistcf_ree.loc[(df_nwlistcf_ree["PERIODO"] == per) & (df_nwlistcf_ree["iter"] != 1)].copy()
                                ly = df_per[Variavel].tolist()
                                fig.add_trace(go.Box( y = ly, boxpoints = False, name = str(per), marker_color = 'blue'))
                            fig.update_layout(title="PIs Temporal"+str(REE))
                            fig.update_xaxes(title_text="Periodos")
                            fig.update_yaxes(title_text="R$/MWh")
                            #fig.update_yaxes(range=[-4000,0])
                            fig.update_yaxes(range=[self.yinf,self.ysup])
                            fig.update_xaxes(range=[self.xinf,self.xsup])
                            fig.update_layout(font=dict(size= data.tamanho_texto), showlegend=False)

                            fig.write_image(
                                os.path.join(diretorio_saida+"/"+str(REE)+"_temporal.png"),
                                width=self.largura,
                                height=self.altura)
                            #FIM BOXPLOT POR PERIODO



                            #BOXPLOT PARA CADA SERIE
                            lista_series = list(range(1,201))
                            Variavel  = "PIEARM"
                            for ser in lista_series:
                                print("IMPRIMINDO GRAFICO DA SERIE: ", ser)
                                df_serie = df_nwlistcf_ree.loc[(df_nwlistcf_ree["serie"] == ser) & (df_nwlistcf_ree["iter"] != 1)].copy()
                                fig = go.Figure()
                                for per in periodos:
                                    df_per = df_serie.loc[(df_serie["PERIODO"] == per) & (df_serie["iter"] != 1)].copy()
                                    ly = df_per[Variavel].tolist()
                                    fig.add_trace(go.Box( y = ly, boxpoints = False, name = str(per), marker_color = 'blue'))
                                    fig.update_layout(title="PIs Temporal "+str(REE) + " Serie "+str(ser))
                                    fig.update_xaxes(title_text="Periodos")
                                    fig.update_yaxes(title_text="R$/MWh")
                                    fig.update_yaxes(range=[self.yinf,self.ysup])
                                    fig.update_xaxes(range=[self.xinf,self.xsup])
                                    fig.update_layout(font=dict(size= data.tamanho_texto), showlegend=False)
                                    fig.write_image(
                                        os.path.join(diretorio_saida+str(REE)+"_serie_"+str(ser)+"_temporal.png"),
                                        width=self.largura,
                                        height=self.altura)
                            #FIM BOXPLOT POR PERIODOS E SERIE





                            #BOXPLOT POR PERIODO
                            print("IMPRIMINDO GRAFICO TEMPORAL")
                            Variavel  = "EARM"
                            fig = go.Figure()
                            for per in periodos:
                                df_per = df_estados_ree.loc[(df_estados_ree["PERIODO"] == per) & (df_estados_ree["ITEc"] != 1)].copy()
                                ly = df_per[Variavel].tolist()
                                fig.add_trace(go.Box( y = ly, boxpoints = False, name = str(per), marker_color = 'blue'))
                            fig.update_layout(title="EARM Temporal"+str(REE))
                            fig.update_xaxes(title_text="Periodos")
                            fig.update_yaxes(title_text="MW")
                            fig.update_yaxes(range=[self.yinf,self.ysup])
                            fig.update_xaxes(range=[self.xinf,self.xsup])
                            fig.update_layout(font=dict(size= data.tamanho_texto), showlegend=False)

                            fig.write_image(
                                os.path.join(diretorio_saida+"/estados_"+str(REE)+"_temporal.png"),
                                width=self.largura,
                                height=self.altura)


                            #print("IMPRIMINDO CSV")
                            #df_ree.to_csv("ESTADOS_REE_"+str(REE)+".csv")
                            Variavel  = "EARM"
                            for ser in series:
                                print("IMPRIMINDO GRAFICO DA SERIE: ", ser)
                                df_serie = df_estados_ree.loc[(df_estados_ree["SIMc"] == ser) & (df_estados_ree["ITEc"] != 1) ].copy()
                                fig = go.Figure()
                                lista_per = df_serie["PERIODO"].unique()
                                lista_iter = df_serie["ITEc"].unique()
                                degradee = 1.0/(len(lista_iter) + 1)
                                tonalidade = 0.95
                                for it in lista_iter:
                                    df_iter = df_serie.loc[(df_serie["ITEc"] == it)].copy()
                                    ly = df_iter[Variavel].tolist()
                                    fig.add_trace(go.Scatter( y = ly, x = lista_per, name = str(it), marker_color = "rgba(0,0,155,"+str(tonalidade)+")"))
                                    tonalidade -= degradee
                                fig.update_layout(title="EARM Por Iteracao Temporal "+str(REE) + " Serie "+str(ser))
                                fig.update_xaxes(title_text="Periodos")
                                fig.update_yaxes(title_text="MW")
                                fig.update_yaxes(range=[self.yinf,self.ysup])
                                fig.update_xaxes(range=[self.xinf,self.xsup])
                                fig.update_layout(font=dict(size= data.tamanho_texto), showlegend=True)
                                fig.write_image(
                                    os.path.join(diretorio_saida+"/36_earm_iteracao_linhas_"+str(REE)+"_serie_"+str(ser)+"_temporal.png"),
                                    width=self.largura,
                                    height=self.altura)


                            #BOXPLOT POR PERIODO
                            print("GRAFICO PIVs por EARMs  SCATTER")
                            Variavel_ESTADO  = "EARM"
                            Variavel_PIV = "PIEARM"
                            cores = ["255,0,0", "0,255,0","0,0,255", "0,0,0"]
                            for per in periodos:
                                fig = go.Figure()
                                degradee = 1.0/11
                                tonalidade = 0.95
                                cor = cores[0]
                                contador_cores = -1
                                for it in iteracoes:
                                    if(it%10 == 0.0):
                                        contador_cores += 1
                                        print(it, " contador: ", contador_cores)
                                        cor = cores[contador_cores]
                                        tonalidade = 0.95
                                    if(it != 1):
                                        aparece = True
                                        for ser in series:
                                            valor_piv = df_nwlistcf_ree.loc[(df_nwlistcf_ree["PERIODO"] == per) & (df_nwlistcf_ree["iter"] == it) & (df_nwlistcf_ree["serie"] == ser)][Variavel_PIV].iloc[0]
                                            valor_earm = df_estados_ree.loc[(df_estados_ree["PERIODO"] == per) & (df_estados_ree["ITEc"] == it) & (df_estados_ree["SIMc"] == ser)][Variavel_ESTADO].iloc[0]

                                            fig.add_trace(go.Scatter( y = [valor_piv], x = [valor_earm], name = str(it), showlegend = aparece, marker_color = "rgba("+cor+","+str(tonalidade)+")"))
                                            aparece = False
                                        tonalidade -= degradee
                                fig.update_layout(title="PIVs x EARM REE "+str(REE)+" PERIODO "+str(per))
                                fig.update_xaxes(title_text="EARM")
                                fig.update_yaxes(title_text="PIVs")
                                fig.update_yaxes(range=[self.yinf,self.ysup])
                                fig.update_xaxes(range=[self.xinf,self.xsup])
                                fig.update_layout(font=dict(size= data.tamanho_texto))
                                fig.write_image(
                                    os.path.join(diretorio_saida+"/scatter_REE_"+str(REE)+"_PERIODO_"+str(per)+"_temporal.png"),
                                    width=self.largura,
                                    height=self.altura)
















                        #fig = go.Figure()
                        #casos = df_cortes_ativos_todos_casos["caso"].unique()
                        #for caso in self.casos:
                        #    df = df_cortes_ativos_todos_casos.loc[(df_cortes_ativos_todos_casos["caso"] == caso.nome)]
                        #    ly = df["coef"].tolist()
                        #    fig.add_trace(go.Box( y = ly, boxpoints = False, name = caso.nome))
                        #
                        #    if(self.eco == "True"):
                        #        df_fcfs = df_fcf_todos_casos.loc[(df_fcf_todos_casos["caso"] == caso.nome)]
                        #        ly = df_fcfs["coef"].tolist()
                        #        fig.add_trace(go.Box( y = ly, boxpoints = False, name = "fcfnw "+caso.nome))
                        #
                        #fig.update_layout(title="PIs Ativos "+unity.arg.nome+" "+self.estudo)
                        #fig.update_xaxes(title_text="Casos")
                        #fig.update_yaxes(title_text="1000R$/hm3")
                        #fig.update_yaxes(range=[self.yinf,self.ysup])
                        #fig.update_xaxes(range=[self.xinf,self.xsup])
                        #fig.update_layout(font=dict(size= data.tamanho_texto))
                        #fig.write_image(
                        #    os.path.join(diretorio_saida+"/pis_ativos"+unity.arg.nome+self.estudo+".png"),
                        #    width=self.largura,
                        #    height=self.altura)
            




            
    def processa_ESTADOS(self, unity, caso):
        dado = Estados.read(caso.caminho+"/nwlistcf/estados.rel")
        df = dado.estados
        return df





    def processa_NWLISTCF(self, unity, caso):
        dado = Nwlistcfrel.read(caso.caminho+"/nwlistcf/nwlistcf.rel")
        df = dado.cortes

        REEs = Ree.read(caso.caminho+"/ree.dat")
        df_rees = REEs.rees
        print(df_rees)
        numero_rees = df_rees["codigo"].unique()

        lista_data_frame_rees = []
        for n_ree in numero_rees:
            df_teste = df.copy()
            df_teste = df_teste.loc[(df_teste["REE"] == n_ree)]
            lista_df = []
            periodos = df_teste["PERIODO"].unique()
            contador = 0
            for per in periodos:
                df_temporal = df_teste.loc[(df_teste["PERIODO"] == per)].copy()
                df_temporal["iter"] = (((df_temporal["IREG"]-22400 + 200*contador)/22800)+1).astype("int")
                #print(df_temporal)
                iteracoes = df_temporal["iter"].unique()
                contador += 1
                #print(iteracoes)
                for it in iteracoes:
                    df_temp = df_temporal.loc[(df_temporal["iter"] == it)].reset_index(drop = True)
                    #print(df_temp)
                    registro_0 = df_temp["IREG"].iloc[-1] -1
                    #print("MENOR REGISTRO: ", registro_0)
                    df_temp["serie"] = df_temp["IREG"] - registro_0
                    #print(df_temp)
                    lista_df.append(df_temp)
            df_concat = pd.concat(lista_df).reset_index(drop = True)
            lista_data_frame_rees.append(df_concat)
        df_concat_rees =    pd.concat(lista_data_frame_rees).reset_index(drop = True)
        print(df_concat_rees)
        return df_concat_rees














