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
from idessem.dessem.entdados import Entdados
from idessem.dessem.pdo_eco_fcfcortes import PdoEcoFcfCortes
from idessem.dessem.pdo_operacao import PdoOperacao

import pandas as pd
import os
import json
import plotly.graph_objects as go
import plotly.io as pio

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
                        lista_df_casos = []
                        for caso in self.casos:
                            df = self.cortes_ativos_decomp(unity, caso)
                            lista_df_casos.append(df)
                        df_cortes_ativos_todos_casos = pd.concat(lista_df_casos)
                        df_cortes_ativos_todos_casos.to_csv("pis_ativos"+unity.arg.nome+self.estudo+".csv")

                        fig = go.Figure()
                        casos = df_cortes_ativos_todos_casos["caso"].unique()
                        for caso in self.casos:
                            df = df_cortes_ativos_todos_casos.loc[(df_cortes_ativos_todos_casos["caso"] == caso.nome)]
                            ly = df["coef"].tolist()
                            fig.add_trace(go.Box( y = ly, boxpoints = False, name = caso.nome))
                            
                        fig.update_layout(title="PIs Ativos "+unity.arg.nome+" "+self.estudo)
                        fig.update_xaxes(title_text="Casos")
                        fig.update_yaxes(title_text="1000R$/hm3")
                        fig.update_yaxes(range=[-1400,0])
                        fig.update_layout(font=dict(size= 15))
                        fig.write_image(
                            os.path.join(diretorio_saida+"pis_ativos"+unity.arg.nome+self.estudo+".png"),
                            width=800,
                            height=600)
                    if(modelo == "DESSEM"):
                        lista_df_usi = []
                        for caso in self.casos:
                            df = self.cortes_ativos_dessem(unity)
                        df_resultado = pd.concat(lista_df_usi)
                        lista_df_usi.append(df_result)
                        print(df_resultado)

                        fig = go.Figure()
                        fig.add_trace(
                            go.Bar(
                                x = df_resultado["caso"].tolist(),
                                y = df_resultado["valor"].tolist(),
                                text = df_resultado["valor"].round(1).tolist(),
                                textposition = "inside",
                                name = "PIvs",
                                textfont=dict(size=25),
                                marker_color= "blue",
                                showlegend=True
                            )
                        )
                        fig.update_xaxes(title_text="Casos")
                        fig.update_yaxes(title_text="1000$/hm3")
                        fig.update_layout(font=dict(size= 13))
                        fig.update_layout(title=" PIvs Ativos "+unity.arg.nome)
                        fig.write_image(
                            os.path.join("_pivs_ativos_"+unity.arg.nome+self.estudo+".png"),
                            width=800,
                            height=600)
                        exit(1)


    def cortes_ativos_dessem(self, unity):
        arq = caso.caminho+"/PDO_ECO_FCFCORTES.DAT"
        df = PdoEcoFcfCortes.read(arq).tabela
        #df_rhs = df.loc[(df["tipo_coeficiente"] == "RHS")].reset_index(drop=True)
        df_varm = df.loc[(df["tipo_coeficiente"] == "VARM") & (df["tipo_entidade"] == "USIH")].reset_index(drop=True)
        df_varm_usi = df_varm.loc[(df_varm["nome_entidade"] == unity.arg.nome)]

        arq_oper = caso.caminho+"/PDO_OPERACAO.DAT"
        df_ativos = PdoOperacao.read(arq_oper).cortes_ativos 
        df_ativo = df_ativos.loc[(df_ativos["multiplicador"] > 0)]
        
        lista_coefs = []
        indices = df_ativo["indice_corte"].unique()
        coef_medio = 0
        for indice in indices:
            mult =  df_ativo.loc[( df_ativo["indice_corte"] == indice)]["multiplicador"].iloc[0]
            coef =  df_varm_usi.loc[(df_varm_usi["indice_corte"] == indice)]["valor_coeficiente"].iloc[0]
            coef_medio += mult*coef
        df_result = pd.DataFrame({"usina":[unity.arg.nome], "caso":[caso.nome], "valor":[coef_medio]})
        return df_result

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

        arq_hidr = caso.caminho+"/hidr.dat"
        hid = Hidr.read(arq_hidr)
        df_hidr = hid.cadastro.reset_index(drop = False)
        codigo = df_hidr.loc[df_hidr["nome_usina"] == unity.arg.nome]["codigo_usina"].iloc[0]
        
        arq_fcfnwi = caso.caminho+"/fcfnwi."+extensao
        df_fcf = pd.DataFrame()
        if(os.path.isfile(arq_fcfnwi)):
            fcf = Fcfnw.read(arq_fcfnwi)
            df = fcf.cortes
            df_fcf = df.loc[(df["UHE"] == codigo)].reset_index(drop = True)
        
        
        arq_fcfnwn = caso.caminho+"/fcfnwn."+extensao
        arq_dadger = caso.caminho+"/dadger."+extensao
        f_prodt_65 = 0
        if(not os.path.isfile(arq_fcfnwi)):

            dadger = Dadger.read(arq_dadger)
            dadger_uh = dadger.uh(df = True)
            codigo_ree = dadger_uh.loc[dadger_uh["codigo_usina"] == codigo]["codigo_ree"].iloc[0]
            fcf = Fcfnw.read(arq_fcfnwn)
            df = fcf.cortes
            df_fcf = df.loc[(df["REE"] == codigo_ree)].reset_index(drop = True)

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

        lista_df_cortes_ativos_ponderados = []
        for cenario in cenarios:
            cortes_ativos = custo_5.loc[(custo_5["cenario"]) == cenario]
            lista_cortes_ativos = cortes_ativos["indice_corte"].unique()
            #print(cortes_ativos)
            valor_coef = 0
            for corte in lista_cortes_ativos:
                if(not os.path.isfile(arq_fcfnwi)):
                    coef_fcf_corte = ((df_fcf.loc[(df_fcf["corte"] == corte)]["coef_earm"].iloc[0]*f_prodt_65*10000)/36)/1000 ## PARANAUE
                if(os.path.isfile(arq_fcfnwi)):
                    coef_fcf_corte = df_fcf.loc[(df_fcf["corte"] == corte)]["coef_varm"].iloc[0]
                parcela_pi = cortes_ativos.loc[(cortes_ativos["indice_corte"]==corte)]["parcela_pi"].iloc[0]
                valor_coef += coef_fcf_corte*parcela_pi
            valor_coef = valor_coef/coef_pi
            df_atv = pd.DataFrame({"cenario":[cenario], "coef":[valor_coef]})
            lista_df_cortes_ativos_ponderados.append(df_atv)
        df_cortes_ativos_ponderados = pd.concat(lista_df_cortes_ativos_ponderados).reset_index(drop=True)
        df_cortes_ativos_ponderados["caso"] = caso.nome
        return df_cortes_ativos_ponderados














