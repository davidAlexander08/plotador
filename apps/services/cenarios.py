from typing import Dict
from apps.model.unidade import UnidadeSintese
from apps.graficos.graficos import Graficos
from apps.indicadores.indicadores_temporais import IndicadoresTemporais
from apps.model.caso import Caso
from apps.model.sintese import Sintese
from apps.model.argumento import Argumento
import os
import json

class Cenarios:
    def __init__(self, arquivo_json):
        with open(arquivo_json, "r") as f:
            dados = json.load(f)
        # Lê dados de entrada
        estudo = dados["estudo"]
        nome_caso_referencia = dados["nome_caso_referencia"]
        # Cria objetos do estudo
        casos = [Caso.from_dict(d) for d in dados["casos"]]
        usinas = [UsinaAvalicao.from_dict(d) for d in dados["usinas"]]
        indicadores_cenarios = IndicadoresCenarios(casos, nome_caso_referencia,usinas)
        graficos = Graficos(casos)
        # Gera saídas do estudo
        diretorio_saida = f"resultados/{estudo}/cenarios"
        os.makedirs(diretorio_saida, exist_ok=True)

        f

        lista_ree = ['BMONTE', 'IGUACU', 'ITAIPU', 'MADEIRA', 'MAN-AP', 'NORDESTE', 'NORTE', 'PARANA', 'PRNPANEMA', 'SUDESTE', 'SUL', 'TPIRES']
        lista_sbm = ["NORDESTE", "NORTE", "SUDESTE", "SUL"]
        lista_par_enaa = []


        sintese_fw = UnidadeSintese("ENAA_SIN_FOR", "MWmes", "casos" ,"ENA_SIN_FOR", None, None)
        sintese_sf = UnidadeSintese("ENAA_SIN_SF", "MWmes", "casos" ,"ENA_SIN_SF", None, None)
        par_enaa_sin = (sintese_fw, sintese_sf)
        lista_par_enaa.append(par_enaa_sin)

        
        for ree in lista_ree:
            sintese_fw = UnidadeSintese("ENAA_REE_FOR", "MWmes", "casos" ,"ENA_REE_FOR_"+ree, "ree", ree)
            sintese_sf = UnidadeSintese("ENAA_REE_SF", "MWmes", "casos" ,"ENA_REE_SF_"+ree, "ree", ree)
            par_enaa_ree = (sintese_fw, sintese_sf)
            lista_par_enaa.append(par_enaa_ree)

        
        for sbm in lista_sbm:
            sintese_fw = UnidadeSintese("ENAA_SBM_FOR", "MWmes", "casos" ,"ENA_SBM_FOR_"+sbm, "submercado", sbm)
            sintese_sf = UnidadeSintese("ENAA_SBM_SF", "MWmes", "casos" ,"ENA_SBM_SF_"+sbm, "submercado", sbm)
            par_enaa_sbm = (sintese_fw, sintese_sf)
            lista_par_enaa.append(par_enaa_sbm)



        for u in usinas:
            sintese_fw = UnidadeSintese("QINC_UHE_FOR", "hm3", "casos" ,"QINC_UHE_FOR_"+u.nome, "usina", u.nome)
            sintese_sf = UnidadeSintese("QINC_UHE_SF", "hm3", "casos" ,"QINC_UHE_SF_"+u.nome, "usina", u.nome)
            par_enaa_uhe = (sintese_fw, sintese_sf)
            lista_par_enaa.append(par_enaa_uhe)
        
        for elemento in lista_par_enaa:
            df_fw = indicadores_cenarios.retorna_df_concatenado(elemento[0].sintese, elemento[0].fitroColuna , elemento[0].filtroArgumento )
            df_sf = indicadores_cenarios.retorna_df_concatenado(elemento[1].sintese, elemento[1].fitroColuna , elemento[1].filtroArgumento )

            filtro_for_1_arg = elemento[0].fitroColuna if elemento[0].fitroColuna is not None else "" 
            filtro_sf_1_arg = elemento[1].fitroColuna if elemento[1].fitroColuna is not None else "" 
    
            filtro_for = elemento[0].filtroArgumento if elemento[0].filtroArgumento is not None else "SIN" 
            filtro_sf = elemento[1].filtroArgumento if elemento[1].filtroArgumento is not None else "SIN" 

            Log.log().info("Gerando tabela "+elemento[0].titulo)
            df_fw.to_csv(os.path.join(diretorio_saida, "eco_for_"+elemento[0].titulo+"_"+filtro_for+"_"+estudo+".csv"),     index=False)

            Log.log().info("Gerando tabela "+elemento[1].titulo)
            df_sf.to_csv(os.path.join(diretorio_saida, "eco_sf_"+elemento[1].titulo+"_"+filtro_sf+"_"+estudo+".csv"),      index=False)

            df_fw =  df_fw[df_fw[['cenario']].apply(lambda x: x[0].isdigit(), axis=1)]
            df_sf =  df_sf[df_sf[['cenario']].apply(lambda x: x[0].isdigit(), axis=1)]
            
            #SOMA DE TODOS OS ESTAGIOS, TODAS ITERACOES NO EIXO X
            Log.log().info("Gerando gráfico soma dos estágios para cada iteração ")
            for c in casos:
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
                caminho_adicional_saida = "SIN" if filtro_for_1_arg is None else filtro_for_1_arg+"/"+filtro_for
                os.makedirs(diretorio_saida+"/"+caminho_adicional_saida, exist_ok=True)
                fig.write_image(
                    os.path.join(diretorio_saida+"/"+caminho_adicional_saida, filtro_for_1_arg+"_"+filtro_for+"_"+c.nome+"_soma_todos_estagios_"+estudo+".png"),
                    width=800,
                    height=600,
                )     
    
    
    
            #FIXANDO O ESTAGIO, TODAS ITERACOES NO EIXO X
            Log.log().info("Gerando gráfico fixado em um estágio para todas iterações ")
            for c in casos:
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
                    caminho_adicional_saida = "SIN" if filtro_for_1_arg is None else filtro_for_1_arg+"/"+filtro_for
                    os.makedirs(diretorio_saida+"/"+caminho_adicional_saida, exist_ok=True)
                    fig.write_image(
                        os.path.join(diretorio_saida+"/"+caminho_adicional_saida, filtro_for_1_arg+"_"+filtro_for+"_"+c.nome+"_estagio_FW_SF_"+str(est)+"_"+estudo+".png"),
                        width=800,
                        height=600,
                    )    




            # FIXANDO ITERACAO E VARIANDO ESTAGIO
            Log.log().info("Gerando gráfico fixado em uma iteração para todos estágios ")
            for c in casos:
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
                    caminho_adicional_saida = "SIN" if filtro_for_1_arg is None else filtro_for_1_arg+"/"+filtro_for
                    fig.write_image(
                        os.path.join(diretorio_saida+"/"+caminho_adicional_saida, filtro_for_1_arg+"_"+filtro_for+"_"+c.nome+"_iteracao_FW_SF_"+str(iter)+"_"+estudo+".png"),
                        width=800,
                        height=600,
                    )     

            

            
