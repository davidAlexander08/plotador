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
from idecomp.decomp.custos import Custos
from idecomp.decomp.fcfnw import Fcfnw
from idecomp.decomp.caso import Caso

import os
import json

class FCF:


    def __init__(self, data):
        self.estudo = data.estudo
        self.casos = data.casos
        self.indicadores_temporais = IndicadoresTemporais(data.casos)
        self.graficos = Graficos(data)
        diretorio_saida = f"resultados/{self.estudo}/fcf"
        os.makedirs(diretorio_saida, exist_ok=True)

        set_modelos =set({})
        for caso in self.casos:
            set_modelos.add(caso.modelo)
        if(len(set_modelos) != 1):
            print("ERRO: Tentativa de plotar FCF Com mais de um modelo no JSON")
            exit(1)
        modelo = list(set_modelos)[0]

        for arg in data.args:
            if(arg.chave == "UHE"):
                sts = Sintese("VAGUA_UHE_EST") #SINTESE DUMMY
                conj = ConjuntoUnidadeSintese(sts, arg, "estagios", data.limites, data.tamanho_texto)
                for unity in conj.listaUnidades:
                    print(unity.arg.nome)
                    if(modelo == "DECOMP"):
                        for caso in self.casos:
                            self.cortes_ativos_decomp(caso)
                    

                    #mapa_temporal[unity] = df_temporal

    def cortes_ativos_decomp(self, caso):
        extensao = ""
        with open(caso.caminho+"/caso.dat") as f:
            extensao = f.readline().strip('\n')
        if extensao == "":
            raise FileNotFoundError(f"Arquivo caso.dat não encontrado.") 

        arq_memcal = caso.caminho+"/memcal."+extensao
        if(os.path.isfile(arq_memcal)):
            f = open(arq, "r")
            Lines = f.readlines()
            flag = 0
            for line in Lines:
                if(usina[0] in line):
                    flag = 1
                if(flag == 1 and "SOMATORIO PRODT_65%=" in line):
                    #print(line[25:50])
                    f_prodt_65 = float(line[25:50].strip())
                    flag = 0
        else:
            raise FileNotFoundError(f"Arquivo memcal.rvx não encontrado.") 