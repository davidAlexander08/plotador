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
from inewave.newave import Dger
from inewave.nwlistcf import Nwlistcfrel
from inewave.nwlistcf import Estados
import plotly.express as px
import pandas as pd
import os
import json
import plotly.graph_objects as go
import plotly.io as pio

class NWLISTCF:


    def __init__(self, data, xinf, xsup, largura, altura, eco, yinf, ysup, ree, box, linhas, series, iters, periodos):
        self.xinf = xinf
        self.xsup = xsup
        self.largura = largura
        self.altura = altura
        self.eco = eco
        self.yinf = yinf
        self.ysup = ysup
        self.ree = ree
        self.box = box
        self.linhas = linhas
        self.tamanho_texto = data.tamanho_texto
        self.series = series.split(",") if series is not None else None
        self.iters = iters.split(",") if iters is not None else None
        self.periodos = periodos.split(",") if periodos is not None else None

        self.estudo = data.estudo
        self.casos = data.casos
        self.indicadores_temporais = IndicadoresTemporais(data.casos)
        self.graficos = Graficos(data)
        self.diretorio_saida = f"resultados/{self.estudo}/nwlistcf"
        os.makedirs(self.diretorio_saida, exist_ok=True)

        set_modelos =set({})
        for caso in self.casos:
            set_modelos.add(caso.modelo)
        if(len(set_modelos) != 1):
            print("ERRO: Tentativa de plotar NWLISTCF Com mais de um modelo no JSON")
            exit(1)
        if(len(self.casos) != 1):
            print("ERRO: Tentativa de plotar NWLISTCF Com mais de um caso no JSON")
            exit(1)
        if(list(set_modelos)[0] != "NEWAVE"):
            print("ERRO: NWLISTCF e valido apenas para o modelo NEWAVE")
            exit(1)
        modelo = list(set_modelos)[0]

        for arg in data.args:
            sts = Sintese("VAGUA_UHE_EST") #SINTESE DUMMY
            conj = ConjuntoUnidadeSintese(sts, arg, "estagios", data.limites, data.tamanho_texto)
            if(arg.chave == "UHE"):
                for unity in conj.listaUnidades:
                    lista_df_casos_nwlistcf = []
                    for caso in self.casos:
                        df = self.processa_NWLISTCF(unity, caso, self.ree)
                        lista_df_casos_nwlistcf.append(df)
                    df_nwlistcf_rees = pd.concat(lista_df_casos_nwlistcf)
                    df_nwlistcf_rees.to_csv(self.diretorio_saida+"/df_nwlistcf_rees"+self.estudo+".csv")

                    lista_rees = df_nwlistcf_rees["REE"].unique()

                    lista_df_casos_estados = []
                    for caso in self.casos:
                        df_est = self.processa_ESTADOS(unity, caso)
                        lista_df_casos_estados.append(df_est)
                    df_estados_rees = pd.concat(lista_df_casos_estados)
                    df_estados_rees.to_csv(self.diretorio_saida+"/df_estados_rees"+self.estudo+".csv")

                    if(self.ree != None):
                        lista_rees = [int(self.ree)]

                    for u_ree in lista_rees:
                        df_nwlistcf_ree = df_nwlistcf_rees.loc[(df_nwlistcf_rees["REE"] == u_ree) & (df_nwlistcf_rees["ITEc"] != 1)]
                        df_nwlistcf_ree = self.filtra_data_frame(df_nwlistcf_ree)

                        df_estados_ree = df_estados_rees.loc[(df_estados_rees["REE"] == u_ree) & (df_estados_rees["ITEc"] != 1)]
                        df_estados_ree = self.filtra_data_frame(df_estados_ree)

                        Variavel_ESTADO  = "EARM"
                        Variavel_PIV = "PIEARM"
                        if(self.box == "True"):
                            self.gera_grafico_boxplot_por_serie_para_cada_periodo_todas_iteracoes(Variavel_PIV, df_nwlistcf_ree, u_ree)
                            self.gera_grafico_boxplot_por_periodo_todas_series_e_iteracoes(Variavel_PIV, df_nwlistcf_ree, u_ree)
                            self.gera_grafico_boxplot_por_periodo_todas_series_e_iteracoes(Variavel_ESTADO, df_estados_ree, u_ree)

                        if(self.linhas == "True"):
                            self.gera_grafico_evolucao_temporal_por_serie_para_cada_iteracao(Variavel_PIV, df_nwlistcf_ree, u_ree)
                            self.gera_grafico_evolucao_temporal_por_serie_para_cada_iteracao(Variavel_ESTADO, df_estados_ree, u_ree)

                        self.gera_grafico_nuvem_PIVs_por_Armazanamento_Scatter(Variavel_ESTADO, Variavel_PIV, df_nwlistcf_ree, df_estados_ree, u_ree)

            if(arg.chave == "REE"):
                for unity in conj.listaUnidades:
                    lista_df_casos_nwlistcf = []
                    for caso in self.casos:
                        df = self.processa_NWLISTCF(unity, caso, self.ree)
                        lista_df_casos_nwlistcf.append(df)
                    df_nwlistcf_rees = pd.concat(lista_df_casos_nwlistcf)
                    df_nwlistcf_rees.to_csv(self.diretorio_saida+"/df_nwlistcf_rees"+self.estudo+".csv")

                    lista_rees = df_nwlistcf_rees["REE"].unique()

                    lista_df_casos_estados = []
                    for caso in self.casos:
                        df_est = self.processa_ESTADOS(unity, caso)
                        lista_df_casos_estados.append(df_est)
                    df_estados_rees = pd.concat(lista_df_casos_estados)
                    df_estados_rees.to_csv(self.diretorio_saida+"/df_estados_rees"+self.estudo+".csv")

                    if(self.ree != None):
                        lista_rees = [int(self.ree)]

                    for u_ree in lista_rees:
                        df_nwlistcf_ree = df_nwlistcf_rees.loc[(df_nwlistcf_rees["REE"] == u_ree) & (df_nwlistcf_rees["ITEc"] != 1)]
                        df_nwlistcf_ree = self.filtra_data_frame(df_nwlistcf_ree)

                        df_estados_ree = df_estados_rees.loc[(df_estados_rees["REE"] == u_ree) & (df_estados_rees["ITEc"] != 1)]
                        df_estados_ree = self.filtra_data_frame(df_estados_ree)

                        Variavel_ESTADO  = "EARM"
                        Variavel_PIV = "PIEARM"
                        if(self.box == "True"):
                            self.gera_grafico_boxplot_por_serie_para_cada_periodo_todas_iteracoes(Variavel_PIV, df_nwlistcf_ree, u_ree)
                            self.gera_grafico_boxplot_por_periodo_todas_series_e_iteracoes(Variavel_PIV, df_nwlistcf_ree, u_ree)
                            self.gera_grafico_boxplot_por_periodo_todas_series_e_iteracoes(Variavel_ESTADO, df_estados_ree, u_ree)

                        if(self.linhas == "True"):
                            self.gera_grafico_evolucao_temporal_por_serie_para_cada_iteracao(Variavel_PIV, df_nwlistcf_ree, u_ree)
                            self.gera_grafico_evolucao_temporal_por_serie_para_cada_iteracao(Variavel_ESTADO, df_estados_ree, u_ree)

                        self.gera_grafico_nuvem_PIVs_por_Armazanamento_Scatter(Variavel_ESTADO, Variavel_PIV, df_nwlistcf_ree, df_estados_ree, u_ree)


    def filtra_data_frame(self, df):
        df_entrada = df.copy()
        if(self.series != None):
            lista_aux = []
            for elem in self.series:
                lista_aux.append(df_entrada.loc[(df_entrada["SIMc"] == int(elem))])
            df_entrada = pd.concat(lista_aux)
        if(self.iters != None):
            lista_aux = []
            for elem in self.iters:
                lista_aux.append(df_entrada.loc[(df_entrada["ITEc"] == int(elem))])
            df_entrada = pd.concat(lista_aux)
        if(self.periodos != None):
            lista_aux = []
            for elem in self.periodos:
                lista_aux.append( df_entrada.loc[(df_entrada["SIMc"] == int(elem))])
            df_entrada = pd.concat(lista_aux)
        return df_entrada

    def gera_grafico_boxplot_por_serie_para_cada_periodo_todas_iteracoes(self, Variavel, df_nwlistcf_ree, u_ree):
        #BOXPLOT PARA CADA SERIE
        lista_series = df_nwlistcf_ree["SIMc"].unique()
        Variavel  = "PIEARM"
        for ser in lista_series:
            print("IMPRIMINDO GRAFICO DA SERIE: ", ser)
            df_serie = df_nwlistcf_ree.loc[(df_nwlistcf_ree["SIMc"] == ser) & (df_nwlistcf_ree["ITEc"] != 1)].copy()
            fig = go.Figure()
            lista_periodos = df_nwlistcf_ree["PERIODO"].unique()
            for per in lista_periodos:
                df_per = df_serie.loc[(df_serie["PERIODO"] == per) & (df_serie["ITEc"] != 1)].copy()
                ly = df_per[Variavel].tolist()
                fig.add_trace(go.Box( y = ly, boxpoints = False, name = str(per), marker_color = 'blue'))
                fig.update_layout(title="PIs Temporal "+str(u_ree) + " Serie "+str(ser))
                fig.update_xaxes(title_text="Periodos")
                fig.update_yaxes(title_text="R$/MWh")
                fig.update_yaxes(range=[self.yinf,self.ysup])
                fig.update_xaxes(range=[self.xinf,self.xsup])
                fig.update_layout(font=dict(size= self.tamanho_texto), showlegend=False)
                fig.write_image(
                    os.path.join(self.diretorio_saida+str(u_ree)+"_serie_"+str(ser)+"_temporal.png"),
                    width=self.largura,
                    height=self.altura)

    def gera_grafico_boxplot_por_periodo_todas_series_e_iteracoes(self,Variavel, df_estados_ree, u_ree):
        #BOXPLOT POR PERIODO
        print("IMPRIMINDO GRAFICO TEMPORAL")
        fig = go.Figure()
        lista_periodos = df_estados_ree["PERIODO"].unique()
        for per in lista_periodos:
            df_per = df_estados_ree.loc[(df_estados_ree["PERIODO"] == per) & (df_estados_ree["ITEc"] != 1)].copy()
            ly = df_per[Variavel].tolist()
            fig.add_trace(go.Box( y = ly, boxpoints = False, name = str(per), marker_color = 'blue'))
        fig.update_layout(title=Variavel+" Temporal"+str(u_ree))
        fig.update_xaxes(title_text="Periodos")
        fig.update_yaxes(title_text="MW")
        fig.update_yaxes(range=[self.yinf,self.ysup])
        fig.update_xaxes(range=[self.xinf,self.xsup])
        fig.update_layout(font=dict(size= self.tamanho_texto), showlegend=False)

        fig.write_image(
            os.path.join(self.diretorio_saida+"/estados_"+str(u_ree)+"_temporal.png"),
            width=self.largura,
            height=self.altura)

    def gera_grafico_evolucao_temporal_por_serie_para_cada_iteracao(self,Variavel, df_estados_ree, u_ree):
        lista_series = df_estados_ree["SIMc"].unique()
        for ser in lista_series:
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
            fig.update_layout(title=Variavel+" Por Iteracao Temporal "+str(u_ree) + " Serie "+str(ser))
            fig.update_xaxes(title_text="Periodos")
            fig.update_yaxes(title_text="MW")
            fig.update_yaxes(range=[self.yinf,self.ysup])
            fig.update_xaxes(range=[self.xinf,self.xsup])
            fig.update_layout(font=dict(size= self.tamanho_texto), showlegend=True)
            fig.write_image(
                os.path.join(self.diretorio_saida+"/36_earm_iteracao_linhas_"+str(u_ree)+"_serie_"+str(ser)+"_temporal.png"),
                width=self.largura,
                height=self.altura)

    def gera_grafico_nuvem_PIVs_por_Armazanamento_Scatter(self, Variavel_ESTADO, Variavel_PIV, df_nwlistcf_ree, df_estados_ree, u_ree):
        print("GRAFICO PIVs por EARMs  SCATTER")
        cores = ["255,0,0", "0,255,0","0,0,255", "0,0,0"]
        lista_periodos = df_nwlistcf_ree["PERIODO"].unique()
        lista_iteracoes = df_nwlistcf_ree["ITEc"].unique()
        lista_series = df_nwlistcf_ree["SIMc"].unique()
        print(lista_periodos)
        print(lista_iteracoes)
        print(lista_series)
        for per in lista_periodos:
            fig = go.Figure()
            degradee = 1.0/11
            tonalidade = 0.95
            cor = cores[0]
            contador_cores = -1
            for it in lista_iteracoes:
                if(it%10 == 0.0):
                    contador_cores += 1
                    #print(it, " contador: ", contador_cores)
                    cor = cores[contador_cores]
                    tonalidade = 0.95
                if(it != 1):
                    aparece = True
                    for ser in lista_series:
                        valor_piv = df_nwlistcf_ree.loc[(df_nwlistcf_ree["PERIODO"] == per) & (df_nwlistcf_ree["ITEc"] == it) & (df_nwlistcf_ree["SIMc"] == ser)][Variavel_PIV].iloc[0]
                        valor_earm = df_estados_ree.loc[(df_estados_ree["PERIODO"] == per) & (df_estados_ree["ITEc"] == it) & (df_estados_ree["SIMc"] == ser)][Variavel_ESTADO].iloc[0]

                        fig.add_trace(go.Scatter( y = [valor_piv], x = [valor_earm], name = str(it), showlegend = aparece, marker_color = "rgba("+cor+","+str(tonalidade)+")"))
                        aparece = False
                    tonalidade -= degradee
            fig.update_layout(title=Variavel_PIV+" x "+Variavel_ESTADO+" REE "+str(u_ree)+" PERIODO "+str(per))
            fig.update_xaxes(title_text=Variavel_ESTADO)
            fig.update_yaxes(title_text=Variavel_PIV)
            fig.update_yaxes(range=[self.yinf,self.ysup])
            fig.update_xaxes(range=[self.xinf,self.xsup])
            fig.update_layout(font=dict(size= self.tamanho_texto))
            diretorio_saida_nuvem = self.diretorio_saida+"/nuvem"
            os.makedirs(diretorio_saida_nuvem, exist_ok=True)
            fig.write_image(
                os.path.join(diretorio_saida_nuvem+"/scatter_REE_"+str(u_ree)+"_PERIODO_"+str(per)+"_temporal.png"),
                width=self.largura,
                height=self.altura)
            
    def processa_ESTADOS(self, unity, caso):
        dado = Estados.read(caso.caminho+"/nwlistcf/estados.rel")
        df = dado.estados
        return df





    def processa_NWLISTCF(self, unity, caso, ree):
        dado = Nwlistcfrel.read(caso.caminho+"/nwlistcf/nwlistcf.rel")
        df = dado.cortes

        dado_dger = Dger.read(caso.caminho+"/dger.dat")
        num_fw = dado_dger.num_forwards
        print("num_fw: ", num_fw)

        REEs = Ree.read(caso.caminho+"/ree.dat")
        df_rees = REEs.rees
        #print(df_rees)
        numero_rees = df_rees["codigo"].unique()

        numero_rees = df_rees["codigo"].unique() if (self.ree is None) else [int(self.ree)]
        lista_data_frame_rees = []
        for n_ree in numero_rees:
            df_teste = df.copy()
            df_teste = df_teste.loc[(df_teste["REE"] == n_ree)]
            lista_df = []
            periodos = df_teste["PERIODO"].unique()
            contador = 0
            for per in periodos:
                df_temporal = df_teste.loc[(df_teste["PERIODO"] == per)].copy()
                menor_registro = df_temporal["IREG"].min() -1 
                print(menor_registro)
                valor_maior_proximo_registro = df_temporal["IREG"].min() + num_fw
                print(valor_maior_proximo_registro)
                menor_registro_proximo = df_temporal.loc[(df_temporal["IREG"] > valor_maior_proximo_registro)]["IREG"].min() - 1
                print(menor_registro_proximo)
                print(menor_registro_proximo - menor_registro)
                exit(1)
                #df_temporal["ITEc"] = (((df_temporal["IREG"]-22400 + 200*contador)/22800)+1).astype("int")
                df_temporal["ITEc"] = (((df_temporal["IREG"]-menor_registro + num_fw*contador)/22800)+1).astype("int")
                #print(df_temporal)
                iteracoes = df_temporal["ITEc"].unique()
                contador += 1
                #print(iteracoes)
                for it in iteracoes:
                    df_temp = df_temporal.loc[(df_temporal["ITEc"] == it)].reset_index(drop = True)
                    #print(df_temp)
                    registro_0 = df_temp["IREG"].iloc[-1] -1
                    #print("MENOR REGISTRO: ", registro_0)
                    df_temp["SIMc"] = df_temp["IREG"] - registro_0
                    #print(df_temp)
                    lista_df.append(df_temp)
            df_concat = pd.concat(lista_df).reset_index(drop = True)
            lista_data_frame_rees.append(df_concat)
        df_concat_rees =    pd.concat(lista_data_frame_rees).reset_index(drop = True)
        #print(df_concat_rees)
        return df_concat_rees














