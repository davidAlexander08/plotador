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
from idecomp.decomp.dadger import Dadger
from idecomp.decomp.hidr import Hidr
import pandas as pd
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
                            self.cortes_ativos_decomp(unity, caso)
                    

                    #mapa_temporal[unity] = df_temporal

    def cortes_ativos_decomp(self, unity, caso):
        extensao = ""
        with open(caso.caminho+"/caso.dat") as f:
            extensao = f.readline().strip('\n')
        if extensao == "":
            raise FileNotFoundError(f"Arquivo caso.dat não encontrado.") 

        arq = caso.caminho+"/custos."+extensao
        custo = Custos.read(arq)
        tabela = custo.relatorio_fcf
        ultimo_estagio = tabela["estagio"].unique()[-1]
        custo_5 = tabela.loc[(tabela["estagio"] == ultimo_estagio)].reset_index(drop = True)
        cenarios = custo_5["cenario"].unique()
        coef_pi = custo_5["parcela_pi"].max()
        print(coef_pi)
        print(custo_5)
        arq_fcfnwi = caso.caminho+"/fcfnwi."+extensao
        fcf = pd.DataFrame()
        if(os.path.isfile(arq_fcfnwi)):
            fcf = Fcfnw.read(arq_fcfnwi)
            df = fcf.cortes
            fcf = df.loc[(df["UHE"] == unity.arg.nome)].reset_index(drop = True)
        
        
        arq_fcfnwn = caso.caminho+"/fcfnwn."+extensao
        arq_dadger = caso.caminho+"/dadger."+extensao
        arq_hidr = caso.caminho+"/hidr.dat"
        f_prodt_65 = 0
        if(not os.path.isfile(arq_fcfnwi)):
            hid = Hidr.read(arq_hidr)
            df_hidr = hid.cadastro.reset_index(drop = False)
            codigo = df_hidr.loc[df_hidr["nome_usina"] == unity.arg.nome]["codigo_usina"].iloc[0]
            dadger = Dadger.read(arq_dadger)
            dadger_uh = dadger.uh(df = True)
            codigo_ree = dadger_uh.loc[dadger_uh["codigo_usina"] == codigo]["codigo_ree"].iloc[0]
            fcf = Fcfnw.read(arq_fcfnwn)
            df = fcf.cortes
            fcf = df.loc[(df["REE"] == codigo_ree)].reset_index(drop = True)

            arq_memcal = caso.caminho+"/memcal."+extensao
            if(os.path.isfile(arq_memcal)):
                pass
                f = open(arq_memcal, "r")
                Lines = f.readlines()
                flag = 0
                for line in Lines:
                    if(unity.arg.nome in line):
                        flag = 1
                    if(flag == 1 and "SOMATORIO PRODT_65%=" in line):
                        #print(line[25:50])
                        f_prodt_65 = float(line[25:50].strip())
                        flag = 0
            else:
                raise FileNotFoundError(f"Arquivo memcal.rvx não encontrado.") 


        for cenario in cenarios:
            cortes_ativos = custo_5.loc[(custo_5["cenario"]) == cenario]
            lista_cortes_ativos = cortes_ativos["indice_corte"].unique()
            #print(cortes_ativos)
            valor_coef = 0
            for corte in lista_cortes_ativos:
                if(not os.path.isfile(arq_fcfnwi)):
                    coef_fcf_corte = ((fcf.loc[(fcf["corte"] == corte)]["coef_earm"].iloc[0]*f_prodt_65*10000)/36)/1000 ## PARANAUE
                if(os.path.isfile(arq_fcfnwi)):
                    print(fcf)
                    coef_fcf_corte = fcf.loc[(fcf["corte"] == corte)]["coef_varm"].iloc[0]
                parcela_pi = cortes_ativos.loc[(cortes_ativos["indice_corte"]==corte)]["parcela_pi"].iloc[0]
                valor_coef += coef_fcf_corte*parcela_pi
            valor_coef = valor_coef/coef_pi
            df_atv = pd.DataFrame({"cenario":[cenario], "coef":[valor_coef]})
            lista_df_cortes_ativos_ponderados.append(df_atv)
        df_cortes_ativos_ponderados = pd.concat(lista_df_cortes_ativos_ponderados).reset_index(drop=True)
        df_cortes_ativos_ponderados["caso"] = caso.nome
        print(df_cortes_ativos_ponderados)
        return df_cortes_ativos_ponderados














