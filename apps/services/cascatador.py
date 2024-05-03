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
    


            # size of image
            canvas = (400, 300)

            # scale ration
            scale = 5
            thumb = canvas[0]/scale, canvas[1]/scale

            # rectangles (width, height, left position, top position)
            frames = [(50, 50, 5, 5), (60, 60, 100, 50), (100, 100, 205, 120)]

            # init canvas
            im = Image.new('RGBA', canvas, (255, 255, 255, 255))
            draw = ImageDraw.Draw(im)

            # draw rectangles
            for frame in frames:
                x1, y1 = frame[2], frame[3]
                x2, y2 = frame[2] + frame[0], frame[3] + frame[1]
                draw.rectangle([x1, y1, x2, y2], outline=(0, 0, 0, 255))

            # make thumbnail
            im.thumbnail(thumb)

            # save image
            im.save(diretorio_saida+"/im.png')

            exit(1)
            usinas_mar = d_usi.loc[d_usi["codigo_usina_jusante"] == 0]
            print(usinas_mar)
        print(d_usi)
        exit(1)

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