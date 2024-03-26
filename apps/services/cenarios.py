from typing import Dict
from apps.model.unidade import UnidadeSintese
from apps.graficos.graficos import Graficos
from apps.indicadores.indicadores_cenarios import IndicadoresCenarios
from apps.model.caso import Caso
from apps.model.sintese import Sintese
from apps.model.argumento import Argumento
import plotly.graph_objects as go

import os
import json

class Cenarios:
    def __init__(self, arquivo_json):
        with open(arquivo_json, "r") as f:
            dados = json.load(f)
        # Lê dados de entrada
        self.estudo = dados["estudo"]
        # Cria objetos do estudo
        self.casos = [Caso.from_dict(d) for d in dados["casos"]]
        self.indicadores_cenarios = IndicadoresCenarios(self.casos)
        self.graficos = Graficos(self.casos)
        sinteses = [Sintese.from_dict(d) for d in dados["sinteses"]]
        args = [Argumento.from_dict(d) for d in dados["argumentos"]]
        # Gera saídas do estudo
        diretorio_saida = f"resultados/{self.estudo}/cenarios"
        os.makedirs(diretorio_saida, exist_ok=True)
        lista_ree = ['BMONTE', 'IGUACU', 'ITAIPU', 'MADEIRA', 'MAN-AP', 'NORDESTE', 'NORTE', 'PARANA', 'PRNPANEMA', 'SUDESTE', 'SUL', 'TPIRES']
        lista_sbm = ["NORDESTE", "NORTE", "SUDESTE", "SUL"]
        lista_par_enaa = []
        sinteses_validas = ["FOR", "SF"]
        for sts in sinteses:
            prefixo_cenarios = sts.sintese.split("_")[2]
            prefixo_grandeza = sts.sintese.split("_")[0]
            if(prefixo_cenarios in sinteses_validas):
                espacial = sts.sintese.split("_")[1]
                sts_for = Sintese(prefixo_grandeza+"_"+espacial+"_FOR")
                sts_sf = Sintese(prefixo_grandeza+"_"+espacial+"_SF")
                if(espacial == "SIN"):
                    arg = Argumento(None, None)
                    diretorio_saida_arg = diretorio_saida+"/"+espacial
                    os.makedirs(diretorio_saida_arg, exist_ok=True)
                    unity_for = UnidadeSintese(sts_for, "", arg)
                    unity_sf = UnidadeSintese(sts_sf, "", arg)
                    par = (unity_for, unity_sf)
                    self.executa(par,diretorio_saida_arg )
                else:
                    for arg in args:
                        if(espacial == arg.chave):
                            diretorio_saida_arg = diretorio_saida+"/"+arg.chave+"/"+arg.nome
                            os.makedirs(diretorio_saida_arg, exist_ok=True)
                            unity_for = UnidadeSintese(sts, "casos", arg)
                            unity_sf = UnidadeSintese(sts, "casos", arg)
                            par = (unity_for, unity_sf)
                            self.executa(par,diretorio_saida_arg )
            else:
                print("SINTESE: ",sts.sintese," NAO VALIDA PARA ANALISE DE CENARIOS")

        
    def executa(self, par_unity, diretorio_saida_arg):
        df_fw = self.indicadores_cenarios.retorna_df_concatenado(par_unity[0])
        df_sf = self.indicadores_cenarios.retorna_df_concatenado(par_unity[1])

        filtro_for_1_arg = par_unity[0].fitroColuna if par_unity[0].fitroColuna is not None else "" 
        filtro_sf_1_arg = par_unity[1].fitroColuna if par_unity[1].fitroColuna is not None else "" 

        filtro_for = par_unity[0].filtroArgumento if par_unity[0].filtroArgumento is not None else "SIN" 
        filtro_sf = par_unity[1].filtroArgumento if par_unity[1].filtroArgumento is not None else "SIN" 

        df_fw =  df_fw[df_fw[['cenario']].apply(lambda x: x[0].isdigit(), axis=1)]
        df_sf =  df_sf[df_sf[['cenario']].apply(lambda x: x[0].isdigit(), axis=1)]

        self.indicadores_cenarios.exportar(df_fw , diretorio_saida_arg, "eco_for_"+par_unity[0].titulo+"_"+filtro_for+"_"+self.estudo+".csv" )
        self.indicadores_cenarios.exportar(df_sf , diretorio_saida_arg, "eco_for_"+par_unity[0].titulo+"_"+filtro_sf+"_"+self.estudo+".csv" )

        
        #SOMA DE TODOS OS ESTAGIOS, TODAS ITERACOES NO EIXO X
        for c in self.casos:
            df_caso_fw = df_fw.loc[(df_fw["caso"] == c.nome)].copy()
            df_caso_sf = df_sf.loc[(df_sf["caso"] == c.nome)].copy()
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
