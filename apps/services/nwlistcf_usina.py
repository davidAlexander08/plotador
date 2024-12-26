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


    def __init__(self, data, xinf, xsup, largura, altura, eco, yinf, ysup, box, linhas, series, iters, usinas):
        self.xinf = xinf
        self.xsup = xsup
        self.largura = largura
        self.altura = altura
        self.eco = eco
        self.yinf = yinf
        self.ysup = ysup
        self.box = box
        self.linhas = linhas
        self.tamanho_texto = data.tamanho_texto
        self.series = series.split(",") if series is not None else None
        self.iters = iters.split(",") if iters is not None else None
        self.usinas = usinas.split(",") if usinas is not None else None

        self.estudo = data.estudo
        self.casos = data.casos
        self.indicadores_temporais = IndicadoresTemporais(data.casos)
        self.graficos = Graficos(data)
        self.diretorio_saida = f"resultados/{self.estudo}/nwlistcf"
        os.makedirs(self.diretorio_saida, exist_ok=True)

        if(list(set_modelos)[0] != "NEWAVE"):
            print("ERRO: NWLISTCF e valido apenas para o modelo NEWAVE")
            exit(1)
        modelo = list(set_modelos)[0]

        if(self.iters == None):
            self.iters = list(range(1, 51 + 1))
        if(self.series == None):
            self.series = list(range(1, 201 + 1))

        if(os.path.isfile(caso.caminho+"/nwlistcf.rel")):
            pass
        elif(os.path.isfile(caso.caminho+"/sintese/CORTES.parquet")):
            df_cortes_usinas = pd.read_parquet(caso.caminho+"/sintese/CORTES.parquet",engine = "pyarrow")
            dados_dger = Dger.read(caso.caminho+"/dger.dat")

            for codigo_usi in self.usinas:
                df_usina = df_cortes_usinas.loc[df_cortes_usinas["UHE"] == int(codigo_usi)].reset_index(drop = True)
                lista_forwards = list(range(1, 200 + 1))
                lista_iters = list(range(1, 50 + 1))
                lista_df = []
                numfw = 200
                valor_antigo = 0
                for it in lista_iters:
                    valor_fw = it*numfw
                    df_temp = df_usina.loc[(df_usina["IREG"] <= valor_fw) & (df_usina["IREG"] > valor_antigo)].reset_index(drop = True)
                    valor_antigo = valor_fw
                    df_temp["ITEc"] = it
                    df_temp["SIMc"] = list(range(1, 200 + 1))[::-1]
                    #print(df_temp)
                    lista_df.append(df_temp)
                df_conc = pd.concat(lista_df)
                df_conc = df_conc.sort_values(by="IREG", ascending=False).reset_index(drop = True)




        else:
            print("SEM CORTES.parquet e SEM nwlistcf.rel. Impossível realizar a análise")
            exit(1)

        

        print( self.yinf, " ",  self.ysup)        


        df_nwlistcf_rees = self.processa_NWLISTCF(self.casos[0], self.ree)
        df_nwlistcf_rees.to_csv(self.diretorio_saida+"/df_nwlistcf_rees"+self.estudo+".csv")

        lista_rees = df_nwlistcf_rees["REE"].unique()

        
        flag_existe_estados = 0
        lista_df_casos_estados = []
        if(os.path.isfile(caso.caminho+"/nwlistcf/estados.rel")):
            flag_existe_estados = 1
            df_est = self.processa_ESTADOS(self.casos[0])
            lista_df_casos_estados.append(df_est)

        if(flag_existe_estados == 1):
            df_estados_rees = pd.concat(lista_df_casos_estados)
            df_estados_rees.to_csv(self.diretorio_saida+"/df_estados_rees"+self.estudo+".csv")

        if(self.ree != None):
            lista_rees = [int(self.ree)]

        for u_ree in lista_rees:
            df_nwlistcf_ree = df_nwlistcf_rees.loc[(df_nwlistcf_rees["REE"] == u_ree) & (df_nwlistcf_rees["ITEc"] != 1)]
            df_nwlistcf_ree = self.filtra_data_frame(df_nwlistcf_ree)

            if(flag_existe_estados == 1):
                df_estados_ree = df_estados_rees.loc[(df_estados_rees["REE"] == u_ree) & (df_estados_rees["ITEc"] != 1)]
                df_estados_ree = self.filtra_data_frame(df_estados_ree)

            Variavel_ESTADO  = "EARM" 
            Variavel_PIV = "PIEARM" #PIV para versao 28.0.3 e PIEARM para versao 29.4
            self.gera_grafico_boxplot_por_periodo_todas_series_e_iteracoes(Variavel_PIV, df_nwlistcf_ree, u_ree)

            if(self.box == "True"):    
                self.gera_grafico_boxplot_por_serie_para_cada_periodo_todas_iteracoes(Variavel_PIV, df_nwlistcf_ree, u_ree)
                if(flag_existe_estados == 1): 
                    self.gera_grafico_boxplot_por_periodo_todas_series_e_iteracoes(Variavel_ESTADO, df_estados_ree, u_ree)

            if(self.linhas == "True"):
                self.gera_grafico_evolucao_temporal_por_serie_para_cada_iteracao(Variavel_PIV, df_nwlistcf_ree, u_ree)
                if(flag_existe_estados == 1): 
                    self.gera_grafico_evolucao_temporal_por_serie_para_cada_iteracao(Variavel_ESTADO, df_estados_ree, u_ree)

            if(flag_existe_estados == 1): 
                self.gera_grafico_nuvem_PIVs_por_Armazanamento_Scatter(Variavel_ESTADO, Variavel_PIV, df_nwlistcf_ree, df_estados_ree, u_ree)

        #for arg in data.args:
        #    sts = Sintese("VAGUA_UHE_EST") #SINTESE DUMMY
        #    conj = ConjuntoUnidadeSintese(sts, arg, "estagios", data.limites, data.tamanho_texto)
        #    if(arg.chave == "REE"):
        #        for unity in conj.listaUnidades:


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

    def gera_grafico_boxplot_por_periodo_todas_series_e_iteracoes(self, df):
        #BOXPLOT POR PERIODO
        print("IMPRIMINDO GRAFICO TEMPORAL")
        fig = go.Figure()
        lista_periodos = df_estados_ree["PERIODO"].unique()
        for per in lista_periodos:
            df_per = df_estados_ree.loc[(df_estados_ree["PERIODO"] == per) & (df_estados_ree["ITEc"] != 1)].copy()
            ly = df["PIVARM"].tolist()
            fig.add_trace(go.Box( y = ly, boxpoints = False, name = str(per), marker_color = 'blue'))
        fig.update_layout(title=Variavel+" Temporal"+str(u_ree))
        fig.update_xaxes(title_text="Periodos")
        fig.update_yaxes(title_text="R$/MWh")
        fig.update_yaxes(range=[self.yinf,self.ysup])
        fig.update_xaxes(range=[self.xinf,self.xsup])
        fig.update_layout(font=dict(size= self.tamanho_texto), showlegend=False)

        fig.write_image(
            os.path.join(self.diretorio_saida+"/"+Variavel+"_"+str(u_ree)+"_temporal.png"),
            width=self.largura,
            height=self.altura)


    def gera_grafico_evolucao_temporal_eixo_x_Iteracoes(self,Variavel, df, usina):
        lista_series = df["SIMc"].unique()
        degradee = 1.0/(len(lista_series) + 1)
        tonalidade = 0.95
        for ser in lista_series:
            print("IMPRIMINDO GRAFICO DA SERIE: ", ser)
            df_serie = df.loc[(df["SIMc"] == ser) & (df["ITEc"] != 1) ].copy()
            fig = go.Figure()
            ly = df_serie["PIVARM"].tolist()
            fig.add_trace(go.Scatter( y = ly, name = str(it), marker_color = "rgba(0,0,155,"+str(tonalidade)+")")) #x = lista_per, 
            tonalidade -= degradee
            fig.update_layout(title=Variavel+" Por Iteracao Temporal "+str(usina) + " Serie "+str(ser))
            fig.update_xaxes(title_text="Periodos")
            fig.update_yaxes(title_text="MW")
            fig.update_yaxes(range=[self.yinf,self.ysup])
            fig.update_xaxes(range=[self.xinf,self.xsup])
            fig.update_layout(font=dict(size= self.tamanho_texto), showlegend=True)
            fig.write_image(
                os.path.join(self.diretorio_saida+"/36_"+Variavel+"iteracao_linhas_"+str(usina)+"_serie_"+str(ser)+"_temporal.png"),
                width=self.largura,
                height=self.altura)


    def gera_grafico_evolucao_temporal_por_serie_para_cada_iteracao(self,Variavel, df, usina):
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
                ly = df_iter["PIVARM"].tolist()
                fig.add_trace(go.Scatter( y = ly, x = lista_per, name = str(it), marker_color = "rgba(0,0,155,"+str(tonalidade)+")"))
                tonalidade -= degradee
            fig.update_layout(title=Variavel+" Por Iteracao Temporal "+str(usina) + " Serie "+str(ser))
            fig.update_xaxes(title_text="Periodos")
            fig.update_yaxes(title_text="MW")
            fig.update_yaxes(range=[self.yinf,self.ysup])
            fig.update_xaxes(range=[self.xinf,self.xsup])
            fig.update_layout(font=dict(size= self.tamanho_texto), showlegend=True)
            fig.write_image(
                os.path.join(self.diretorio_saida+"/36_"+Variavel+"iteracao_linhas_"+str(usina)+"_serie_"+str(ser)+"_temporal.png"),
                width=self.largura,
                height=self.altura)
#
    #def gera_grafico_nuvem_PIVs_por_Armazanamento_Scatter(self, Variavel_ESTADO, Variavel_PIV, df_nwlistcf_ree, df_estados_ree, u_ree):
    #    print("GRAFICO PIVs por EARMs  SCATTER")
    #    cores = ["255,0,0", "0,255,0","0,0,255", "0,0,0"]
    #    lista_periodos = df_nwlistcf_ree["PERIODO"].unique()
    #    lista_iteracoes = df_nwlistcf_ree["ITEc"].unique()
    #    lista_series = df_nwlistcf_ree["SIMc"].unique()
    #    print(lista_periodos)
    #    print(lista_iteracoes)
    #    print(lista_series)
    #    for per in lista_periodos:
    #        fig = go.Figure()
    #        degradee = 1.0/11
    #        tonalidade = 0.95
    #        cor = cores[0]
    #        contador_cores = -1
    #        for it in lista_iteracoes:
    #            if(it%10 == 0.0):
    #                contador_cores += 1
    #                #print(it, " contador: ", contador_cores)
    #                cor = cores[contador_cores]
    #                tonalidade = 0.95
    #            if(it != 1):
    #                aparece = True
    #                for ser in lista_series:
    #                    valor_piv = df_nwlistcf_ree.loc[(df_nwlistcf_ree["PERIODO"] == per) & (df_nwlistcf_ree["ITEc"] == it) & (df_nwlistcf_ree["SIMc"] == ser)][Variavel_PIV].iloc[0]
    #                    valor_earm = df_estados_ree.loc[(df_estados_ree["PERIODO"] == per) & (df_estados_ree["ITEc"] == it) & (df_estados_ree["SIMc"] == ser)][Variavel_ESTADO].iloc[0]
#
    #                    fig.add_trace(go.Scatter( y = [valor_piv], x = [valor_earm], name = str(it), showlegend = aparece, marker_color = "rgba("+cor+","+str(tonalidade)+")"))
    #                    aparece = False
    #                tonalidade -= degradee
    #        fig.update_layout(title=Variavel_PIV+" x "+Variavel_ESTADO+" REE "+str(u_ree)+" PERIODO "+str(per))
    #        fig.update_xaxes(title_text=Variavel_ESTADO)
    #        fig.update_yaxes(title_text=Variavel_PIV)
    #        fig.update_yaxes(range=[self.yinf,self.ysup])
    #        fig.update_xaxes(range=[self.xinf,self.xsup])
    #        fig.update_layout(font=dict(size= self.tamanho_texto))
    #        diretorio_saida_nuvem = self.diretorio_saida+"/nuvem"
    #        os.makedirs(diretorio_saida_nuvem, exist_ok=True)
    #        fig.write_image(
    #            os.path.join(diretorio_saida_nuvem+"/scatter_REE_"+str(u_ree)+"_PERIODO_"+str(per)+"_temporal.png"),
    #            width=self.largura,
    #            height=self.altura)
    #        
#
#
#
#
#







