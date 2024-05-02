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
from inewave.newave import Vazoes

import os
import json

class Cenarios(MetaData):
    def __init__(self, data):
        MetaData.__init__(self)
        self.estudo = data.estudo
        self.casos = data.casos
        self.indicadores_cenarios = IndicadoresCenarios(self.casos)
        self.graficos = Graficos(self.casos)
        diretorio_saida = f"resultados/{self.estudo}/cenarios"
        os.makedirs(diretorio_saida, exist_ok=True)

        print("Apenas serao considerados as seguintes sinteses nesse modulo: ")
        ex = []
        for elemento in self.default_sts_CEN:
            ex.append(elemento.sintese)
        print(ex)

        for sts in self.default_sts_CEN:
            prefixo_cenarios = sts.sintese.split("_")[2]
            prefixo_grandeza = sts.sintese.split("_")[0]
            if(prefixo_cenarios in ["FOR", "SF"]):
                espacial = sts.sintese.split("_")[1]
                if(espacial == "SIN"):
                    arg = Argumento(None, None, "SIN")
                    diretorio_saida_arg = diretorio_saida+"/"+arg.nome
                    os.makedirs(diretorio_saida_arg, exist_ok=True)
                    conj = ConjuntoUnidadeSintese(sts,arg , "casos", data.limites, data.tamanho_texto)
                    self.executa(conj,diretorio_saida_arg )
                else:
                    for arg in data.args:
                        if(espacial == arg.chave):
                            diretorio_saida_arg = diretorio_saida+"/"+arg.nome
                            os.makedirs(diretorio_saida_arg, exist_ok=True)
                            conj = ConjuntoUnidadeSintese(sts, arg, "casos", data.limites, data.tamanho_texto)
                            self.executa(conj,diretorio_saida_arg )
            else:
                print("SINTESE: ",sts.sintese," NAO VALIDA PARA ANALISE DE CENARIOS")


    def executa(self, conj, diretorio_saida_arg):
        for unity in conj.listaUnidades:
            prefixo_grandeza = conj.sintese.sintese.split("_")[0]
            espacial = conj.sintese.sintese.split("_")[1]

            u_fw = UnidadeSintese(Sintese(prefixo_grandeza+"_"+espacial+"_FOR"),unity.arg )
            u_sf = UnidadeSintese(Sintese(prefixo_grandeza+"_"+espacial+"_SF"),unity.arg)
            
            df_fw = self.indicadores_cenarios.retorna_df_concatenado(u_fw)
            df_sf = self.indicadores_cenarios.retorna_df_concatenado(u_sf)


            filtro_for_1_arg = u_fw.fitroColuna if u_fw.fitroColuna is not None else "" 
            filtro_sf_1_arg = u_sf.fitroColuna if u_sf.fitroColuna is not None else "" 

            filtro_for = u_fw.filtroArgumento if u_fw.filtroArgumento is not None else "SIN" 
            filtro_sf = u_sf.filtroArgumento if u_sf.filtroArgumento is not None else "SIN" 

            df_fw =  df_fw[df_fw[['cenario']].apply(lambda x: x[0].isdigit(), axis=1)]
            df_sf =  df_sf[df_sf[['cenario']].apply(lambda x: x[0].isdigit(), axis=1)]

            self.indicadores_cenarios.exportar(df_fw , diretorio_saida_arg, "eco_for_"+u_fw.titulo+"_"+filtro_for+"_"+self.estudo+".csv" )
            self.indicadores_cenarios.exportar(df_sf , diretorio_saida_arg, "eco_for_"+u_sf.titulo+"_"+filtro_sf+"_"+self.estudo+".csv" )

            df_vazoes = pd.DataFrame()
            if(u_fw.filtroArgumento is None):
                if(df_vazoes.empty):
                    lista_df = []
                    for c in self.casos:
                        arquivo_vazoes = c.caminho+"/vazoes.dat"
                        print(arquivo_vazoes)
                        df = self.le_vazoes(arquivo_vazoes)
                        df["caso"] = c.nome
                        lista_df.append(df)
                    df_vazoes = pd.concat(lista_df)
                    print(df_vazoes)
            
            df_vazoes_SIN = pd.DataFrame()
            if(u_fw.filtroArgumento is None):
                if(df_vazoes_SIN.empty):
                    lista_df = []
                    for c in self.casos:
                        df_c = df_vazoes.loc[df_vazoes["caso"] == c.nome]
                        anos = df_c["ano"].unique()
                        print(anos)



            #    df_caso_fw = df_fw.loc[(df_fw["caso"] == c.nome)].copy()
            #    df_caso_sf = df_sf.loc[(df_sf["caso"] == c.nome)].copy()
            #    lista_estagios = df_caso_sf["estagio"].unique()
            #    for est in lista_estagios:
            #        lista_iter = df_caso_fw["iteracao"].unique()
            #        for iter in lista_iter:
            #            
            #            sample1 = XXX
            #            sample2 = XXX
            #            stats.ks_2samp(sample1, sample2)



            #BOXPLOT, SOMA TODOS OS ESTAGIOS, ITER 1, ITER (1-MAX) JUNTOS, SF
            for c in self.casos:
                df_caso_fw = df_fw.loc[(df_fw["caso"] == c.nome)].copy()
                df_caso_sf = df_sf.loc[(df_sf["caso"] == c.nome)].copy()
                fig = go.Figure()
                lista_estagios = df_caso_sf["estagio"].unique()
                lista_iter = df_caso_fw["iteracao"].unique()

                df_iter_fw = df_caso_fw.loc[(df_caso_fw["iteracao"] == 1)]
                if(filtro_for_1_arg == ""):
                    df_iter_fw = df_iter_fw.drop(['dataInicio', 'dataFim',"caso"], axis=1)
                else:
                    df_iter_fw = df_iter_fw.drop(['dataInicio', 'dataFim',filtro_for_1_arg,"caso"], axis=1)
                df = df_iter_fw.groupby(['cenario']).sum()
                fig.add_trace(go.Box(y=df["valor"], name="iter_1", marker_color="rgba(0,0,255,1.0)"))
                lista_df = []
                for iter in lista_iter:
                    df_iter_fw = df_caso_fw.loc[(df_caso_fw["iteracao"] == iter)]
                    if(filtro_for_1_arg == ""):
                        df_iter_fw = df_iter_fw.drop(['dataInicio', 'dataFim',"caso"], axis=1)
                    else:
                        df_iter_fw = df_iter_fw.drop(['dataInicio', 'dataFim',filtro_for_1_arg,"caso"], axis=1)
                    df = df_iter_fw.groupby(['cenario']).sum()
                    lista_df.append(df)
                df_iter_1_max = pd.concat(lista_df)
                fig.add_trace(go.Box(y=df_iter_1_max["valor"], name="1-"+str(max(lista_iter)), marker_color="rgba(0,0,255,1.0)"))
                    
                if(filtro_for_1_arg == ""):
                    df_caso_sf = df_caso_sf.drop(['dataInicio', 'dataFim',"caso"], axis=1)
                else:
                    df_caso_sf = df_caso_sf.drop(['dataInicio', 'dataFim',filtro_for_1_arg,"caso"], axis=1)
                df_sf_2 = df_caso_sf.groupby(['cenario']).sum()
                fig.add_trace(go.Box(y=df_sf_2["valor"], name="SF", marker_color="rgba(255,0,0,1.0)"))
                fig.update_layout(    title="Iteracoes soma todos estágios 1, 1-"+str(max(lista_iter))+", sf "+filtro_for_1_arg+"_"+filtro_for,    showlegend=False)
                #fig.update_layout(yaxis_range=[500000,2000000])
                self.graficos.exportar(fig, diretorio_saida_arg, filtro_for_1_arg+"_"+filtro_for+"_"+c.nome+"_iter_1_1_"+str(max(lista_iter))+"_sf_soma_todos_estagios_"+self.estudo+".png")






            #SOMA DE TODOS OS ESTAGIOS, TODAS ITERACOES NO EIXO X
            for c in self.casos:
                df_caso_fw = df_fw.loc[(df_fw["caso"] == c.nome)].copy()
                df_caso_sf = df_sf.loc[(df_sf["caso"] == c.nome)].copy()
                print(df_caso_fw)
                print(df_caso_sf)
                fig = go.Figure()
                lista_estagios = df_caso_sf["estagio"].unique()
                lista_iter = df_caso_fw["iteracao"].unique()
                for iter in lista_iter:
                    df_iter_fw = df_caso_fw.loc[(df_caso_fw["iteracao"] == iter)]
                    if(filtro_for_1_arg == ""):
                        df_iter_fw = df_iter_fw.drop(['dataInicio', 'dataFim',"caso"], axis=1)
                    else:
                        df_iter_fw = df_iter_fw.drop(['dataInicio', 'dataFim',filtro_for_1_arg,"caso"], axis=1)
                    df = df_iter_fw.groupby(['cenario']).sum()
                    fig.add_trace(go.Box(y=df["valor"], name=str(iter), marker_color="rgba(0,0,255,1.0)"))
                if(filtro_for_1_arg == ""):
                    df_caso_sf = df_caso_sf.drop(['dataInicio', 'dataFim',"caso"], axis=1)
                else:
                    df_caso_sf = df_caso_sf.drop(['dataInicio', 'dataFim',filtro_for_1_arg,"caso"], axis=1)
                df_sf_2 = df_caso_sf.groupby(['cenario']).sum()
                fig.add_trace(go.Box(y=df_sf_2["valor"], name="SF", marker_color="rgba(255,0,0,1.0)"))
                fig.update_layout(    title="Iteração para soma de todos os Estagios "+filtro_for_1_arg+"_"+filtro_for,    showlegend=False)
                self.graficos.exportar(fig, diretorio_saida_arg, filtro_for_1_arg+"_"+filtro_for+"_"+c.nome+"_soma_todos_estagios_"+self.estudo+".png")



            #FIXANDO O ESTAGIO, TODAS ITERACOES NO EIXO X
            for c in self.casos:
                df_caso_fw = df_fw.loc[(df_fw["caso"] == c.nome)].copy()
                df_caso_sf = df_sf.loc[(df_sf["caso"] == c.nome)].copy()
                lista_estagios = df_caso_sf["estagio"].unique()
                for est in lista_estagios:
                    df_filtered_iter_fw = df_caso_fw.loc[(df_caso_fw["estagio"] == est)]  
                    df_filtered_iter_sf = df_caso_sf.loc[(df_caso_sf["estagio"] == est)] 
                    lista_iter = df_filtered_iter_fw["iteracao"].unique()
                    fig = go.Figure()
                    for iter in lista_iter:
                        lista_y = df_filtered_iter_fw.loc[(df_filtered_iter_fw["iteracao"] == iter)]["valor"]
                        fig.add_trace(go.Box(y=lista_y, name=str(iter), marker_color="rgba(0,0,255,1.0)"))
                    lista_y = df_filtered_iter_sf["valor"]
                    fig.add_trace(go.Box(y=lista_y, name="SF", marker_color="rgba(255,0,0,1.0)"))
                    fig.update_layout(    title="Iterações para o Estágio "+str(est)+" "+filtro_for_1_arg+"_"+filtro_for,    showlegend=False)
                    self.graficos.exportar(fig, diretorio_saida_arg, filtro_for_1_arg+"_"+filtro_for+"_"+c.nome+"_estagio_FW_SF_"+str(est)+"_"+self.estudo+".png")




            # FIXANDO ITERACAO E VARIANDO ESTAGIO
            for c in self.casos:
                df_caso_fw = df_fw.loc[(df_fw["caso"] == c.nome)].copy()
                df_caso_sf = df_sf.loc[(df_sf["caso"] == c.nome)].copy()
                it_min = df_caso_fw["iteracao"].min()   
                it_max = df_caso_fw["iteracao"].max()  
                list_iter = list(range(it_min, it_max, 10))
                list_iter.append(it_max)
                lista_estagios = df_caso_sf["estagio"].unique()
                for iter in list_iter:
                    df_filtered_iter_fw = df_caso_fw.loc[(df_caso_fw["iteracao"] == iter)]  
                    fig = go.Figure()
                    for est in lista_estagios:
                        lista_y = df_filtered_iter_fw.loc[(df_filtered_iter_fw["estagio"] == est)]["valor"]
                        fig.add_trace(go.Box(y=lista_y, name=str(est), marker_color="rgba(0,0,255,1.0)"))
                    lista_y = df_caso_sf["valor"]
                    fig.add_trace(go.Box(y=lista_y, name="SF", marker_color="rgba(255,0,0,1.0)"))
                    fig.update_layout(    title="Estágios para Iteração "+str(iter)+" "+filtro_for_1_arg+"_"+filtro_for,    showlegend=False)
                    self.graficos.exportar(fig, diretorio_saida_arg, filtro_for_1_arg+"_"+filtro_for+"_"+c.nome+"_iteracao_FW_SF_"+str(iter)+"_"+self.estudo+".png")

                


        #sintese_fw = UnidadeSintese("ENAA_SIN_FOR", "MWmes", "casos" ,"ENA_SIN_FOR", None, None)
        #sintese_sf = UnidadeSintese("ENAA_SIN_SF", "MWmes", "casos" ,"ENA_SIN_SF", None, None)
        #par_enaa_sin = (sintese_fw, sintese_sf)
        #lista_par_enaa.append(par_enaa_sin)

        
        #for ree in lista_ree:
        #    sintese_fw = UnidadeSintese("ENAA_REE_FOR", "MWmes", "casos" ,"ENA_REE_FOR_"+ree, "ree", ree)
        #    sintese_sf = UnidadeSintese("ENAA_REE_SF", "MWmes", "casos" ,"ENA_REE_SF_"+ree, "ree", ree)
        #    par_enaa_ree = (sintese_fw, sintese_sf)
        #    lista_par_enaa.append(par_enaa_ree)

        
       # for sbm in lista_sbm:
       #     sintese_fw = UnidadeSintese("ENAA_SBM_FOR", "MWmes", "casos" ,"ENA_SBM_FOR_"+sbm, "submercado", sbm)
       #     sintese_sf = UnidadeSintese("ENAA_SBM_SF", "MWmes", "casos" ,"ENA_SBM_SF_"+sbm, "submercado", sbm)
       #     par_enaa_sbm = (sintese_fw, sintese_sf)
       #     lista_par_enaa.append(par_enaa_sbm)



       # for u in usinas:
       #     sintese_fw = UnidadeSintese("QINC_UHE_FOR", "hm3", "casos" ,"QINC_UHE_FOR_"+u.nome, "usina", u.nome)
       #     sintese_sf = UnidadeSintese("QINC_UHE_SF", "hm3", "casos" ,"QINC_UHE_SF_"+u.nome, "usina", u.nome)
       #     par_enaa_uhe = (sintese_fw, sintese_sf)
       #     lista_par_enaa.append(par_enaa_uhe)


    def le_vazoes(self, arq):
        f = open(arq, mode="rb")
        POSTOS = 320
        dic = {}
        posto = 1
        df_vazoes = pd.DataFrame(columns=["posto", "ano", "JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"])
        while True:
            chunk = f.read(4)
            if not chunk:
                break
            number = int.from_bytes(chunk, byteorder='little')
            if dic.get(posto) is None:
                dic[posto] = []
                dic[posto].append(number)
            else:
                dic[posto].append(number)
            posto = posto + 1
            if(posto == POSTOS+1):
                posto = 1
        f.close()

        ano = 1931
        print(dic)
        for posto in range(1, POSTOS+1):
            for a in range(0,int(len(dic[posto])/12)):
                lista = []
                new_row = pd.DataFrame({"posto": posto,
                                        "ano": ano,
                                        "JAN": dic[posto][0+ a*12],
                                        "FEV": dic[posto][1+ a*12],
                                        "MAR": dic[posto][2+ a*12],
                                        "ABR": dic[posto][3+ a*12],
                                        "MAI": dic[posto][4+ a*12],
                                        "JUN": dic[posto][5+ a*12],
                                        "JUL": dic[posto][6+ a*12],
                                        "AGO": dic[posto][7+ a*12],
                                        "SET": dic[posto][8+ a*12],
                                        "OUT": dic[posto][9+ a*12],
                                        "NOV": dic[posto][10+ a*12],
                                        "DEZ": dic[posto][11+ a*12]},
                                        index = [0])
                df_vazoes = pd.concat([df_vazoes.loc[:],new_row]).reset_index(drop=True)
                ano = ano + 1
            print("Leitura Vazoes Posto: ", posto)