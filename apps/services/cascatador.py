from typing import Dict
from apps.model.unidade import UnidadeSintese
from apps.graficos.graficos import Graficos
from apps.indicadores.indicadores_cenarios import IndicadoresCenarios
from apps.model.caso import Caso
from apps.model.sintese import Sintese
from apps.model.argumento import Argumento
import plotly.graph_objects as go
import pandas as pd
from scipy import stats
from apps.interface.metaData import MetaData
from apps.model.conjuntoUnidade import ConjuntoUnidadeSintese
from inewave.newave import Confhd
import os
import json
from PIL import Image, ImageDraw

class Cascatador(MetaData):
    def __init__(self, data):
        MetaData.__init__(self)
        self.estudo = data.estudo
        self.casos = data.casos
        self.indicadores_cenarios = IndicadoresCenarios(self.casos)
        self.graficos = Graficos(self.casos)
        diretorio_saida = f"resultados/{self.estudo}/cascatador"
        os.makedirs(diretorio_saida, exist_ok=True)
        for c in self.casos:
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

            #no_mar = mapa_codigo_nos[lista_cod_mar[0]]
            for no in lista_cod_mar:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x = [no.x], y = [no.y], textfont=dict( size=13), text =[no.nome], textposition="bottom center", mode = "markers+text", marker_color="rgba(0,0,255,1.0)" , marker=dict(symbol="triangle-down", size=20)))
                self.add_scatter_graph(fig, no, no.y)
                fig.update_layout(title="Cascata", showlegend = False)
                self.graficos.exportar(fig, diretorio_saida, no.nome+" cascata"+self.estudo, W = 1500, H = 1200)
            exit(1)
            usinas_mar = d_usi.loc[d_usi["codigo_usina_jusante"] == 0]
            print(usinas_mar)
        print(d_usi)
        exit(1)

    def add_scatter_graph(self,fig ,no, nivel):
        pais = no.getPais()
        nivel += 1
        contador = 0
        for pai in pais:
            self.define_x(no, pais)
            #if(nivel < 5):
            fig.add_trace(go.Scatter(x = [pai.x], y = [pai.y], text=[pai.nome], textfont=dict( size=13), textposition= pai.text_position, mode = "markers+text", marker_color="rgba(0,0,255,1.0)" , marker=dict(symbol="triangle-down", size=20)))
            fig.add_trace(go.Scatter(x = [pai.x, pai.x], y = [no.y, pai.y], mode = "lines",  line=dict(color='blue')))
            fig.add_trace(go.Scatter(x = [no.x, pai.x], y = [no.y, no.y], mode = "lines", line=dict(color='blue')))
            self.add_scatter_graph(fig, pai, pai.y)

            minimo = pai.x*1.1 if pai.x < min else -50
            maximo = pai.x*1.1 if pai.x > max else 50
        
            fig.update_xaxes(range = [minimo,maximo])

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