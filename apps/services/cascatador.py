from typing import Dict
from apps.model.unidade import UnidadeSintese
from apps.indicadores.indicadores_cenarios import IndicadoresCenarios
from apps.model.caso import Caso
from apps.model.sintese import Sintese
from apps.model.argumento import Argumento
from apps.indicadores.indicadores_temporais import IndicadoresTemporais
import plotly.graph_objects as go
import pandas as pd
from scipy import stats
from apps.interface.metaData import MetaData
from apps.model.conjuntoUnidade import ConjuntoUnidadeSintese
from inewave.newave import Confhd
from inewave.newave import Hidr
from inewave.newave import Modif

from apps.indicadores.eco_indicadores import EcoIndicadores

import os
import json
from PIL import Image, ImageDraw

class Cascatador(MetaData):
    def __init__(self, data):
        MetaData.__init__(self)
        self.estudo = data.estudo
        self.casos = data.casos
        self.indicadores_cenarios = IndicadoresCenarios(self.casos)
        diretorio_saida = f"resultados/{self.estudo}/cascatador"
        os.makedirs(diretorio_saida, exist_ok=True)
        print(self.casos[0].caminho)
        for c in self.casos:
            #defluencia_usinas = self.eco_indicadores.retorna_df_concatenado("QDEF_UHE_EST")
            #defluencia_usinas_mean = defluencia_usinas.loc[defluencia_usinas["cenario"] == "mean"].round(0)
#
            #qincr_usinas = self.eco_indicadores.retorna_df_concatenado("QINC_UHE_EST")
            #qincr_usinas_mean = qincr_usinas.loc[qincr_usinas["cenario"] == "mean"].round(0)
#
            #qafl_usinas = self.eco_indicadores.retorna_df_concatenado("QAFL_UHE_EST")
            #qafl_usinas_mean = qafl_usinas.loc[qafl_usinas["cenario"] == "mean"].round(0)
#
            #qtur_usinas = self.eco_indicadores.retorna_df_concatenado("QTUR_UHE_EST")
            #qtur_usinas_mean = qtur_usinas.loc[qtur_usinas["cenario"] == "mean"].round(0)
#
            #qver_usinas = self.eco_indicadores.retorna_df_concatenado("QVER_UHE_EST")
            #qver_usinas_mean = qver_usinas.loc[qver_usinas["cenario"] == "mean"].round(0)
#
            #vdef_min_usinas = self.eco_indicadores.retorna_df_concatenado("VDEFMIN_UHE_EST")
            #vdef_min_usinas_mean = vdef_min_usinas.loc[vdef_min_usinas["cenario"] == "mean"].round(0)

            arquivo_hidr = c.caminho+"/hidr.dat"
            d_hidr = Hidr.read(arquivo_hidr).cadastro
            print(d_hidr)

            arquivo_confhd = c.caminho+"/confhd.dat"
            d_usi = Confhd.read(arquivo_confhd).usinas
            print(d_usi)
            print(d_usi.loc[d_usi["codigo_usina"] == 2])
            mapa_codigo_nos = {}   
            for index, row in d_usi.iterrows():
                no = Node()
                no.pais =           []
                no.filhos =         []
                no.codigo =         row["codigo_usina"]
                no.nome =           row["nome_usina"]
                no.posto =          row["posto"]
                no.ree =            row["ree"] 
                no.nivel =          None
                mapa_codigo_nos[no.codigo] = no

            #usinas_mar = d_usi.loc[d_usi["codigo_usina_jusante"] == 0]
            #lista_no_aux = list(mapa_codigo_nos.keys())
            contador = 0
            for cod_usi in mapa_codigo_nos:
                lista_nos_pais = []
                lista_nos_filhos = []
                pais = d_usi.loc[d_usi["codigo_usina_jusante"] == cod_usi]
                if(not pais.empty):
                    for index, row in pais.iterrows():
                        no_pai = mapa_codigo_nos[row["codigo_usina"]]
                        #print("usina: ", cod_usi, "pai: ", no_pai.codigo)
                        lista_nos_pais.append(no_pai)
                    
                filho = d_usi.loc[d_usi["codigo_usina"] == cod_usi]
                if(filho["codigo_usina_jusante"].iloc[0] != 0):
                    no_filho = mapa_codigo_nos[filho["codigo_usina_jusante"].iloc[0]] 
                    #print("usina: ", cod_usi, "filho: ", no_filho.codigo)
                    lista_nos_filhos.append(no_filho)
                no = mapa_codigo_nos[cod_usi]
                no.pais = lista_nos_pais
                no.filhos = lista_nos_filhos
                contador += 1

            #PEGANDO MONTANTES
            lista_cod_cabeceiras = []
            for key in mapa_codigo_nos:
                no = mapa_codigo_nos[key]
                if(len(no.pais) == 0):
                    #print("CABECEIRA: ", key)
                    lista_cod_cabeceiras.append(key)
    
            #PEGANDO MAR
            lista_cod_mar = []
            for key in mapa_codigo_nos:
                no = mapa_codigo_nos[key]
                if((len(no.filhos) == 0) and (len(no.pais) != 0)):
                    lista_cod_mar.append(no)

            #estagios = defluencia_usinas_mean["estagio"].unique()
            #est_1 = [estagios[0]]
            #for est in est_1:#estagios:
            #defluencia_usinas_mean_est = defluencia_usinas_mean.loc[defluencia_usinas_mean["estagio"] == est]
            #qincr_usinas_mean_est = qincr_usinas_mean.loc[qincr_usinas_mean["estagio"] == est]
            #qafl_usinas_mean_est = qafl_usinas_mean.loc[qafl_usinas_mean["estagio"] == est]
#
            #qver_usinas_mean_est = qver_usinas_mean.loc[qver_usinas_mean["estagio"] == est]
            #qtur_usinas_mean_est = qtur_usinas_mean.loc[qtur_usinas_mean["estagio"] == est]
            #vdef_min_usinas_mean_est = vdef_min_usinas_mean.loc[vdef_min_usinas_mean["estagio"] == est]
            #no_mar = mapa_codigo_nos[lista_cod_mar[0]]
            lista_teste = [lista_cod_mar[0]]
            for no in lista_teste:#lista_cod_mar:
                fig = go.Figure()
                lista_traces = []

                simbolo = self.retorna_simbolo(no, d_hidr)
                #def_0 = defluencia_usinas_mean_est.loc[(defluencia_usinas_mean_est["usina"] == no.nome)]["valor"].iloc[0]
                #qinc_0 =  qincr_usinas_mean_est.loc[(qincr_usinas_mean_est["usina"] == no.nome)]["valor"].iloc[0]
                #qafl = qafl_usinas_mean_est.loc[(qafl_usinas_mean_est["usina"] == no.nome)]["valor"].iloc[0]
                #qtur = qtur_usinas_mean_est.loc[(qtur_usinas_mean_est["usina"] == no.nome)]["valor"].iloc[0]
                #qver = qver_usinas_mean_est.loc[(qver_usinas_mean_est["usina"] == no.nome)]["valor"].iloc[0]
                #vdef_min = vdef_min_usinas_mean_est.loc[(vdef_min_usinas_mean_est["usina"] == no.nome)]["valor"].iloc[0]
                #texto = no.nome + "<br> QINC:"+str(int(qinc_0)) + "QAFL:"+str(qafl) + "<br> QTUR: " + str(qtur) + " QVER: "+ str(qver) + " QDEF:" + str(def_0) + "<br> QDEFM: " + str(int(vdef_min/2.63))
                texto = no.nome
                #lista_traces.append(go.Scatter(x = [no.x], y = [no.y], textfont=dict( size=13), text =[texto], textposition="bottom center", mode = "markers+text", marker_color="rgba(0,0,255,1.0)" , marker=dict(symbol=simbolo, size=20)))
                lista_traces.append(go.Scatter(x = [no.x], y = [no.y], textfont=dict( size=13), text =[texto], textposition="bottom center", mode = "markers+text", marker_color="rgba(0,0,255,1.0)" , marker=dict(symbol=simbolo, size=20)))
                
                #self.add_scatter_graph(lista_traces, no, no.y, d_hidr, defluencia_usinas_mean_est, qincr_usinas_mean_est, qafl_usinas_mean_est, qtur_usinas_mean_est, qver_usinas_mean_est, vdef_min_usinas_mean_est)
                self.add_scatter_graph(lista_traces, no, no.y, d_hidr)
                for elemento in lista_traces:
                    fig.add_trace(elemento)
                fig.update_layout(title="Cascata", showlegend = False)

                minimo = -60
                maximo = +60
                for elemento in lista_traces:
                    if(elemento.x[0]< minimo):
                        minimo = elemento.x[0]*1.3 
                    if(elemento.x[0] > maximo):
                        maximo = elemento.x[0]*1.1
                fig.update_xaxes(range = [minimo,maximo])

                fig.update_layout(width = int(1500), height = int(1200))
                fig.write_image(
                    os.path.join(diretorio_saida, no.nome+" cascata"+self.estudo+".png"))
                fig.write_html(os.path.join(diretorio_saida, no.nome+" cascata"+self.estudo+".html"),
                    include_plotlyjs='cdn',
                    config={"modeBarButtonsToAdd": ["drawline", "eraseshape", "sendDataToCloud"]})


                exit(1)
                usinas_mar = d_usi.loc[d_usi["codigo_usina_jusante"] == 0]
                print(usinas_mar)
            print(d_usi)
            exit(1)

    def retorna_simbolo(self, no, d_hidr):
        row = d_hidr.loc[d_hidr["nome_usina"] == no.nome]
        if(row.empty):
            return "triangle-down"
        else:
            if(row["tipo_regulacao"].iloc[0] == "M"):
                return "triangle-down"
            else:
                return "circle"

    #def add_scatter_graph(self,lista_traces ,no, nivel, d_hidr, defluencia_usinas_mean_est, qincr_usinas_mean_est, qafl_usinas_mean_est, qtur_usinas_mean_est, qver_usinas_mean_est, vdef_min_usinas_mean_est):
    def add_scatter_graph(self,lista_traces ,no, nivel, d_hidr):
        pais = no.getPais()
        nivel += 1
        contador = 0
        for pai in pais:
            self.define_x(no, pais)
            #if(nivel < 5):
            #deflu = defluencia_usinas_mean_est.loc[(defluencia_usinas_mean_est["usina"] == pai.nome)]["valor"].iloc[0]
            #qinc =  qincr_usinas_mean_est.loc[(qincr_usinas_mean_est["usina"] == pai.nome)]["valor"].iloc[0]
            #qafl = qafl_usinas_mean_est.loc[(qafl_usinas_mean_est["usina"] == pai.nome)]["valor"].iloc[0]
            #qtur = qtur_usinas_mean_est.loc[(qtur_usinas_mean_est["usina"] == pai.nome)]["valor"].iloc[0]
            #qver = qver_usinas_mean_est.loc[(qver_usinas_mean_est["usina"] == pai.nome)]["valor"].iloc[0]
            #vdef_min = vdef_min_usinas_mean_est.loc[(vdef_min_usinas_mean_est["usina"] == no.nome)]["valor"].iloc[0]

            #texto = pai.nome + "<br> QI:"+str(int(qinc)) + " QA:"+str(int(qafl)) + "<br>QT:"+ str(int(qtur)) + " QV:"+ str(int(qver)) + " <br> QD:" + str(int(deflu)) + " QDM:" + str(int(vdef_min/2.63))
            texto = pai.nome
            simbolo = self.retorna_simbolo(pai, d_hidr)                                                                 #pai.text_position
            #lista_traces.append(go.Scatter(x = [pai.x], y = [pai.y], text=[ texto ], textfont=dict( size=9), textposition= "top center", mode = "markers+text", marker_color="rgba(0,0,255,1.0)" , marker=dict(symbol=simbolo, size=20)))
            lista_traces.append(go.Scatter(x = [pai.x], y = [pai.y], text=[ texto ], textfont=dict( size=13), textposition= "top center", mode = "markers+text", marker_color="rgba(0,0,255,1.0)" , marker=dict(symbol=simbolo, size=20)))
            lista_traces.append(go.Scatter(x = [pai.x, pai.x], y = [no.y, pai.y], mode = "lines",  line=dict(color='blue')))
            lista_traces.append(go.Scatter(x = [no.x, pai.x], y = [no.y, no.y], mode = "lines", line=dict(color='blue')))
            #self.add_scatter_graph(lista_traces, pai, pai.y, d_hidr, defluencia_usinas_mean_est, qincr_usinas_mean_est, qafl_usinas_mean_est, qtur_usinas_mean_est, qver_usinas_mean_est, vdef_min_usinas_mean_est)
            self.add_scatter_graph(lista_traces, pai, pai.y, d_hidr)




    def define_x(self, no,  pais):
        mapa_ramos = {0:100,1:80, 2:60, 3:40, 4:20}
        lista = []
        self.encontra_usinas_cabeceira(no, lista)
        mapa = {}
        for ino in lista:
            lista_usi_filhos = [ino.nome]
            self.encontra_numero_filhos(ino,lista_usi_filhos)
            mapa[ino.nome] = lista_usi_filhos
            #print("usina: ", ino.nome, " numero: ", len(lista_usi_filhos), " lista: ", lista_usi_filhos)
        
        contador = 0
        maximo = 0
        usi_max = ""
        for usi in mapa:
            numero = len(mapa[usi])
            if(numero > maximo):
                maximo = numero
                usi_max = usi
        lista_usi_max =   mapa[usi_max]    
        #print(lista_usi_max) 
        keys_max = mapa.keys() 
        dist = 100 - 10*(no.y)
        contador = 0

        for pai in pais:
            pai.y = no.y + 1
            if(pai.nome in lista_usi_max):
                pai.x = no.x
                pai.text_position = "top center"
            else:
                print("no: ", no.nome, " pai: ", pai.nome, " x: ", pai.x)
                sinal = 1 if(contador%2 == 0) else -1
                pai.x = no.x + sinal*dist
                contador += 1
                pai.text_position = "top right" if sinal == 1 else "top left"
                

            if(len(pais) > 1):
                if((len(pai.getPais()) == 0)):
                    pai.x = no.x + 50
                    pai.y = pai.y - 0.5
                    pai.text_position = "top right"
        
                if((len(pai.getPais()) == 1) ):
                    
                    if((len(pai.getPais()[0].getPais() )== 0)):
                        pai.x = no.x - 30
                        pai.y = pai.y - 0.5
                        pai.text_position = "top left"

                    #if((len(pai.getPais()[0].getPais()) == 1)  and(len(pai.getPais()[0].getPais()[0].getPais() )== 0)):
                    #    pai.x = no.x + 30
                    #    pai.y = pai.y - 0.5

            if(pai.nome in lista_usi_max):
                pai.x = no.x
                pai.y = no.y + 1
                pai.text_position = no.text_position
            
            if(no.nome == "JUPIA" and pai.nome == "TRES IRMAOS"):
                pai.x = -200
                pai.text_position = "top left"

            if(pai.nome == "ROSANA"):
                pai.x = 200
                pai.text_position = "top left"


            if(no.nome == "I. SOLTEIRA" and pai.nome == "FOZ R. CLARO"):
                pai.x = 130
                pai.text_position = "top left"

            if(no.nome == "I. SOLTEIRA" and pai.nome == "SAO SIMAO"):
                pai.x = -90
                pai.text_position = "top left"

            if(no.nome == "CAPIVARA"):
                pai.text_position = "top left"

            if(no.nome == "ITAIPU" and pai.nome == "P. PRIMAVERA"):
                pai.text_position = "top right"

    def encontra_numero_filhos(self, no, lista_usi_filhos):
        lista_filho = no.getFilhos()
        if(len(lista_filho) != 0):
            lista_usi_filhos.append(lista_filho[0].nome)
            self.encontra_numero_filhos(lista_filho[0], lista_usi_filhos)


    def encontra_usinas_cabeceira(self, no, lista):
        pais = no.getPais()
        for pai in pais:
            if(len(pai.getPais()) == 0): lista.append(pai)
            self.encontra_usinas_cabeceira(pai, lista)
        



class Node():
    def __init__(self):

        self.pais = []
        self.filhos = []
        self.codigo = None 
        self.nome = None 
        self.posto = None
        self.codigo_jusante = None 
        self.ree = None 
        self.x = 0 
        self.y = 0
        self.n_ramos = 0
        self.text_position = "top right"

    def getPais(self):
        return self.pais

    def getFilhos(self):
        return self.filhos