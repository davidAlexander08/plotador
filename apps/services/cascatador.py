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
                    print("CABECEIRA: ", key)
                    lista_cod_cabeceiras.append(key)
    
            #PEGANDO MAR
            lista_cod_mar = []
            for key in mapa_codigo_nos:
                no = mapa_codigo_nos[key]
                if(len(no.filhos) == 0):
                    print("MAR: ", key)
                    lista_cod_mar.append(key)

            no_cabeceira = mapa_codigo_nos[lista_cod_mar[0]]
            nivel = 0
            no_cabeceira.x = 10
            no_cabeceira.y = nivel
            fig = go.Figure()
            fig.add_trace(go.Scatter(x = [no_cabeceira.x], y = [no_cabeceira.y], text =[no_cabeceira.nome], mode = "markers", marker_color="rgba(0,0,255,1.0)" , marker=dict(symbol="triangle-down", size=15)))
            self.add_scatter_graph(fig, no_cabeceira, nivel)
            fig.update_layout(title="Cascata", showlegend = False)
            self.graficos.exportar(fig, diretorio_saida, "cascata"+self.estudo+".png")


            #img = Image.new(mode='RGB', size=(2500, 2500 ), color='black')
            #draw = ImageDraw.Draw(img)
            #
            #lista_cod_mar = [lista_cod_mar[0]]
            #for key_cab in lista_cod_mar:
            #    no_cabeceira = mapa_codigo_nos[key_cab]
            #    nivel = 0
            #    print("cod: ", no_cabeceira.codigo, " nivel: ", nivel)
            #    self.desenha_circulo(draw, no_cabeceira, nivel)
            #    
            ## save image
            #img.save(diretorio_saida+"/im.png")

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
            self.define_n_nivel(pais)
            pai.x = 10 + pai.n_nivel
            pai.y = nivel
            print("cod: ", pai.codigo, " nivel: ", nivel)
            fig.add_trace(go.Scatter(x = [pai.x], y = [pai.y], text=[pai.nome], mode = "markers", marker_color="rgba(0,0,255,1.0)" , marker=dict(symbol="triangle-down", size=15)))
            fig.add_trace(go.Scatter(x = [no.x, pai.x], y = [no.y, pai.y], mode = "lines"))

            self.add_scatter_graph(fig, pai, nivel)

    def define_n_nivel(self, pais):
        if(len(pais) == 0):
            pass
        if(len(pais) == 1):
            for pai in pais:
                pai.n_nivel = 0
        if(len(pais) == 2):
            pais[0].n_nivel = -1
            pais[1].n_nivel = 1
        if(len(pais) == 3):
            pais[0].n_nivel = -1
            pais[1].n_nivel = 0
            pais[2].n_nivel = 1
        if(len(pais) == 4):
            pais[0].n_nivel = -2
            pais[1].n_nivel = -1
            pais[2].n_nivel = 1
            pais[3].n_nivel = 2
        if(len(pais) == 5):
            pais[0].n_nivel = -2
            pais[1].n_nivel = -1
            pais[2].n_nivel = 0
            pais[3].n_nivel = 1
            pais[4].n_nivel = 2


    #def desenha_circulo(self,draw ,no, nivel):
    #    pais = no.getPais()
    #    nivel += 1
    #    for pai in pais:
    #        print("cod: ", pai.codigo, " nivel: ", nivel)
    #        x = 500 
    #        y = 2000 - 100*nivel
    #        draw.regular_polygon((x, y,50), 3, rotation=180, fill="blue", outline=None, width=1)
    #        draw.text((x, y,50), pai.nome)
    #        self.desenha_circulo(draw, pai, nivel)
    


class Node():
    def __init__(self):

        self.pais = []
        self.filhos = []
        self.codigo = None 
        self.nome = None 
        self.posto = None
        self.codigo_jusante = None 
        self.ree = None 
        self.nivel = None
        self.n_nivel = None
        self.x = None 
        self.y = None

    def getPais(self):
        return self.pais

    def getFilhos(self):
        return self.filhos