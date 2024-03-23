import click
import os
import json
from apps.utils.log import Log
import pandas as pd
import plotly.graph_objects as go
@click.group()
def cli():
    """
    Aplicação para reproduzir estudos de metodologias
    de planejamento energético feitos no âmbito
    da CPAMP pelo ONS.
    """
    pass


@click.command("analise-pareto")
@click.argument(
    "arquivo_json",
)
def analise_pareto(arquivo_json):
    """
    Calibração do CVaR.
    """
    from apps.model.caso import CasoCalibracaoCVAR
    from apps.model.usina import UsinaAvalicao
    from apps.indicadores.eco_indicadores import EcoIndicadores
    from apps.model.unidade import UnidadeSintese
    from apps.graficos.graficos import GraficosCalibracaoCVAR
    from apps.indicadores.indicadores_medios import IndicadoresMedios
    
    if os.path.isfile(arquivo_json):
        with open(arquivo_json, "r") as f:
            dados = json.load(f)
        # Lê dados de entrada
        estudo = dados["estudo"]
        nome_caso_referencia = dados["nome_caso_referencia"]
        # Cria objetos do estudo
        casos = [CasoCalibracaoCVAR.from_dict(d) for d in dados["casos"]]
        usinas = [UsinaAvalicao.from_dict(d) for d in dados["usinas"]]
        
        eco_indicadores = EcoIndicadores(casos, nome_caso_referencia,usinas)
        indicadores_medios = IndicadoresMedios(casos, nome_caso_referencia,usinas)
        graficos = GraficosCalibracaoCVAR(casos)
        # Gera saídas do estudo
        diretorio_saida = f"resultados/{estudo}/pareto"
        os.makedirs(diretorio_saida, exist_ok=True)


        graficos.gera_pareto_fast(
            indicadores_medios.retorna_df_concatenado("CTER_SIN_EST"),
            indicadores_medios.retorna_df_concatenado("EARPF_SIN_EST"), 
            indicadores_medios.retorna_df_std_concatenado("CTER_SIN_EST"),
            indicadores_medios.retorna_df_std_concatenado("EARPF_SIN_EST"), 
            "CGT SIN Med (MiR$)",
            "EARPF SIN Med (%)",          
            #100,
            #0,
            #indicadores_medios.retorna_df_concatenado("CTER_SIN_EST")["valor"].max() * 1.5,
            #0,
            None,
            None,
            None,
            None,
            "Fronteira de Pareto: EARP x CGT - "+estudo
        ).write_image(
            os.path.join(diretorio_saida, "Newave_pareto_EARPF_CGT"+estudo+".png"),
            width=800,
            height=600,
        )

        graficos.gera_pareto_fast(
            indicadores_medios.retorna_df_concatenado("GTER_SIN_EST"),
            indicadores_medios.retorna_df_concatenado("EARPF_SIN_EST"), 
            indicadores_medios.retorna_df_std_concatenado("GTER_SIN_EST"),
            indicadores_medios.retorna_df_std_concatenado("EARPF_SIN_EST"), 
            "GT SIN Med (MWmes)",
            "EARPF SIN Med (%)",          
            #100,
            #0,
            #indicadores_medios.retorna_df_concatenado("CTER_SIN_EST")["valor"].max() * 1.5,
            #0,
            None,
            None,
            None,
            None,
            "Fronteira de Pareto: EARP x GT - "+estudo
        ).write_image(
            os.path.join(diretorio_saida, "Newave_pareto_EARPF_GT"+estudo+".png"),
            width=800,
            height=600,
        )

        graficos.gera_pareto_fast(
            indicadores_medios.retorna_df_concatenado("GTER_SIN_EST"),
            indicadores_medios.retorna_df_concatenado("EARMF_SIN_EST"), 
            indicadores_medios.retorna_df_std_concatenado("GTER_SIN_EST"),
            indicadores_medios.retorna_df_std_concatenado("EARMF_SIN_EST"), 
            "GT SIN Med (MWmes)",
            "EARM SIN Med (MWmes)",          
            #100,
            #0,
            #indicadores_medios.retorna_df_concatenado("CTER_SIN_EST")["valor"].max() * 1.5,
            #0,
            None,
            None,
            None,
            None,
            "Fronteira de Pareto: EARM x GT - "+estudo
        ).write_image(
            os.path.join(diretorio_saida, "Newave_pareto_EARM_GT"+estudo+".png"),
            width=800,
            height=600,
        )

        graficos.gera_pareto_fast(
            indicadores_medios.retorna_df_concatenado("CTER_SIN_EST"),
            indicadores_medios.retorna_df_concatenado("EARMF_SIN_EST"), 
            indicadores_medios.retorna_df_std_concatenado("CTER_SIN_EST"),
            indicadores_medios.retorna_df_std_concatenado("EARMF_SIN_EST"), 
            "CGT SIN Med (Mi R$)",
            "EARM SIN Med (MWmes)",          
            #100,
            #0,
            #indicadores_medios.retorna_df_concatenado("CTER_SIN_EST")["valor"].max() * 1.5,
            #0,
            None,
            None,
            None,
            None,
            "Fronteira de Pareto: EARM x CGT - "+estudo
        ).write_image(
            os.path.join(diretorio_saida, "Newave_pareto_EARM_CGT"+estudo+".png"),
            width=800,
            height=600,
        )


        eixoY_temp = indicadores_medios.retorna_df_concatenado("CDEF_SIN_EST")["valor"].max()*1.5
        eixoY_sup =  eixoY_temp if eixoY_temp > 500 else 500
        graficos.gera_pareto_fast(
            indicadores_medios.retorna_df_concatenado("CTER_SIN_EST"), 
            indicadores_medios.retorna_df_concatenado("CDEF_SIN_EST"),
            indicadores_medios.retorna_df_std_concatenado("CTER_SIN_EST"),
            indicadores_medios.retorna_df_std_concatenado("CDEF_SIN_EST"), 
            "Custo GT (MiR$)",
            "Custo DEF (MiR$)",
            #eixoY_sup,
            #-20,
            None,
            None,
            #indicadores_medios.retorna_df_concatenado("CTER_SIN_EST")["valor"].max()*2,
            #0,
            None,
            None,
            "Fronteira de Pareto: Custo GT x Custo DEF - "+estudo
        ).write_image(
            os.path.join(diretorio_saida, "Newave_pareto_CGT_CDEF"+estudo+".png"),
            width=800,
            height=600,
        )




        #graficos.gera_pareto_fast(
        #    indicadores_medios.retorna_DF_cenario_medio_incremental_percentual("EARPF_SIN_EST", dropar = False),
        #    indicadores_medios.retorna_df_concatenado("CTER_SIN_EST"), 
        #    indicadores_medios.retorna_DF_std_incremental_percentual("EARPF_SIN_EST", dropar = False),
        #    indicadores_medios.retorna_df_std_concatenado("CTER_SIN_EST"), 
        #    "Ganho EARPF SIN Med (%)",
        #    "Custo GT (R$)",
        #    indicadores_medios.retorna_df_concatenado("CTER_SIN_EST")["valor"].max()*1.5,
        #    0,
        #    None,
        #    None,
        #    "Fronteira de Pareto: Ganho EARPF x Custo GT - "+estudo
        #).write_image(
        #    os.path.join(diretorio_saida, "Newave_pareto_ganhoEarm_CGT"+estudo+".png"),
        #    width=800,
        #    height=600,
        #)



        


        #graficos.gera_pareto_fast(
        #    indicadores_medios.retorna_DF_cenario_medio_incremental_percentual("EARPF_SIN_EST", dropar = False),
        #    indicadores_medios.retorna_DF_cenario_medio_incremental_percentual("CTER_SIN_EST", dropar = False),
        #    indicadores_medios.retorna_DF_std_incremental_percentual("EARPF_SIN_EST", dropar = False),
        #    indicadores_medios.retorna_DF_std_incremental_percentual("CTER_SIN_EST", dropar = False), 
        #    "Ganho EARPF (MWmes)",
        #    "Ganho CT (R$)",
        #    None,
        #    None,
        #    None,
        #    None,
        #    "Fronteira de Pareto: Ganho EARPF x ganho CT - "+estudo
        #).write_image(
        #    os.path.join(diretorio_saida, "Newave_pareto_ganhoEarpf_ganhoct"+estudo+".png"),
        #    width=800,
        #    height=600,
        #)

    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")










@click.command("eco")
@click.argument(
    "arquivo_json",
)
def eco(arquivo_json):
    """
    Calibração do CVaR.
    """
    from apps.model.caso import Caso
    from apps.model.usina import UsinaAvalicao
    from apps.model.ree import Ree
    from apps.model.submercado import Submercado
    from apps.model.sintese import Sintese
    from apps.indicadores.eco_indicadores import EcoIndicadores
    from apps.model.unidade import UnidadeSintese
    from apps.graficos.graficos import Graficos

    if os.path.isfile(arquivo_json):
        with open(arquivo_json, "r") as f:
            dados = json.load(f)
        # Lê dados de entrada
        estudo = dados["estudo"]
        nome_caso_referencia = dados["nome_caso_referencia"]
        # Cria objetos do estudo
        casos = [Caso.from_dict(d) for d in dados["casos"]]
        usinas = [UsinaAvalicao.from_dict(d) for d in dados["usinas"]]
        rees = [Ree.from_dict(d) for d in dados["rees"]]
        submercados = [Submercado.from_dict(d) for d in dados["submercados"]]
        sinteses = [Sintese.from_dict(d) for d in dados["sinteses"]]

        
        eco_indicadores = EcoIndicadores(casos)
        graficos = Graficos(casos)
        # Gera saídas do estudo
        diretorio_saida = f"resultados/{estudo}/eco"
        os.makedirs(diretorio_saida, exist_ok=True)

        for sts in sinteses:
            Log.log().info("Gerando eco "+ sts.sintese +" para o estudo: "+ estudo)
            eco = eco_indicadores.retorna_df_concatenado(sts.sintese)
            eco.to_csv(
                os.path.join(diretorio_saida, "eco_"+sts.sintese+"_"+estudo+".csv"),
                index=False,
            )

        df_custos = eco_indicadores.retorna_df_concatenado("CUSTOS")
        #df_custos = df_custos.loc[(df_custos["mean"] != 0)] #Remove colunas com 0
        df_custos = df_custos.loc[(df_custos["mean"] > 10)] #Remove colunas menores que 10, pois nao sao significantes
        df_custos = df_custos.sort_values(by="mean", ascending=False)
        df_custos = df_custos.round(0)
        fig = graficos.gera_grafico_barras_diferentes(df_custos, "parcela", "mean", "caso",  "parcelas", "R$", 0, "Custos Totais Casos")
        fig.write_image(
            os.path.join(diretorio_saida, "Newave_"+"Custos Totais Casos"+"_"+estudo+".png"),
            width=800,
            height=600,
        )
        for c in casos:
            df_plot = df_custos.loc[(df_custos["caso"] == c.nome)]
            fig = graficos.gera_grafico_barras_diferentes(df_plot, "parcela", "mean", "caso",  "parcelas", "R$", 0, "Custos Totais "+c.nome)
            fig.write_image(
                os.path.join(diretorio_saida, "Newave_"+"Custos Totais "+"_"+c.nome+"_"+estudo+".png"),
                width=800,
                height=600,
            )

        df_convergencia = eco_indicadores.retorna_df_concatenado("CONVERGENCIA")
        #lista = ["zinf","zsup"]
        #mapFormatLine = {"zinf": "dot", "zsup":"dash"}
        lista = ["zinf"]
        mapFormatLine = {"zinf": "dot"}
        fig = graficos.gera_grafico_linhas_diferentes(df_convergencia,lista, mapFormatLine, "R$ (10 6)", "iteracoes", "Convergencia")
        fig.write_image(
            os.path.join(diretorio_saida, "Newave_"+"Convergencias"+"_"+estudo+".png"),
            width=800,
            height=600,
        )



    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")


@click.command("temporal")
@click.argument(
    "arquivo_json",
)
def analise_temporal(arquivo_json):

    from apps.model.caso import Caso
    from apps.model.sintese import Sintese
    from apps.indicadores.indicadores_temporais import IndicadoresTemporais
    from apps.model.unidade import UnidadeSintese
    from apps.model.argumento import Argumento
    from apps.graficos.graficos import Graficos

    if os.path.isfile(arquivo_json):
        with open(arquivo_json, "r") as f:
            dados = json.load(f)
        # Lê dados de entrada
        estudo = dados["estudo"]
        nome_caso_referencia = dados["nome_caso_referencia"]
        # Cria objetos do estudo
        casos = [Caso.from_dict(d) for d in dados["casos"]]
        sinteses = [Sintese.from_dict(d) for d in dados["sinteses"]]
        args = [Argumento.from_dict(d) for d in dados["argumentos"]]
        
        indicadores_temporais = IndicadoresTemporais(casos)
        graficos = Graficos(casos)
        # Gera saídas do estudo
        diretorio_saida = f"resultados/{estudo}/temporal"
        os.makedirs(diretorio_saida, exist_ok=True)
        
        listaUnidadesGraficas = []
        for sts in sinteses:
            espacial = sts.sintese.split("_")[1]
            for arg in args:
                if(espacial == arg.chave):
                    unity = UnidadeSintese(sts, "estagios", arg)
                    diretorio_saida_arg = diretorio_saida+"/"+arg.chave+"/"+arg.nome
                    os.makedirs(diretorio_saida_arg, exist_ok=True)
                    
                    df_unity = indicadores_temporais.retorna_df_concatenado(unity.sintese, unity.fitroColuna , unity.filtroArgumento )
                    indicadores_temporais.exportar(df_unity, diretorio_saida_arg,  "eco_"+unity.titulo+"_"+estudo)
                    
                    fig = graficos.gera_grafico_linha(df_unity, unity.legendaEixoY , unity.legendaEixoX, unity.titulo+"_"+estudo)
                    graficos.exportar(fig, diretorio_saida_arg, "eco_"+unity.titulo+"_"+estudo)
                    
                    df_unity_2_mes = indicadores_temporais.retorna_df_concatenado_medio_2_mes(unity.sintese, unity.fitroColuna , unity.filtroArgumento )
                    indicadores_temporais.exportar(df_unity_2_mes, diretorio_saida_arg,  "eco_"+unity.titulo+"_2_mes_"+estudo)
                    
                    fig = graficos.gera_grafico_barra(df_unity_2_mes["valor"], df_unity_2_mes["caso"],  unity.legendaEixoX, unity.legendaEixoY, 2, unity.titulo+"2_mes")
                    graficos.exportar(fig, diretorio_saida_arg, unity.titulo+"_2_mes_"+estudo)

        
        
        #unity = UnidadeSintese("EARPF_SIN_EST", None, "%", "Energia_Armazenada_Percentual_Final_SIN_CREF "+estudo)
        #df_unity = indicadores_temporais.retorna_df_concatenado(unity.sintese, unity.fitroColuna , unity.filtroArgumento )
        #graficos.gera_graficos_linha_Newave_CREF(df_unity, indicadores_temporais.df_cref, "EARPF", unity.legendaEixoY, unity.titulo, None).write_image(
        #    os.path.join(diretorio_saida, "SIN_EARPF_CREF"+estudo+".png"),
        #    width=800,
        #    height=600
        #    )
        #graficos.gera_graficos_linha_Newave_CREF(df_unity, indicadores_temporais.df_cref, "EARPF", unity.legendaEixoY, unity.titulo+"_2024", "2024").write_image(
        #    os.path.join(diretorio_saida, "SIN_EARPF_CREF_2024"+estudo+".png"),
        #    width=800,
        #    height=600
        #    )
        #graficos.gera_graficos_linha_Newave_CREF(df_unity, indicadores_temporais.df_cref, "EARPF", unity.legendaEixoY, unity.titulo+"_Ano_Vigente", "ADEQUA").write_image(
        #    os.path.join(diretorio_saida, "SIN_EARPF_CREF_AnoCaso"+estudo+".png"),
        #    width=800,
        #    height=600
        #    )
        #df_EARPF_mean_p10_p90 = indicadores_temporais.gera_df_mean_p10_p90("EARPF_SIN_EST")
        #graficos.gera_graficos_linha_mean_p10_p90_CREF(df_EARPF_mean_p10_p90,indicadores_temporais.df_cref, "EARPF", "%", "Energia Armazenada Cenarios CREF"+estudo, None ).write_image(
        #    os.path.join(diretorio_saida, "Energia_Armazenada_Media_P10_P90_"+estudo+".png"),
        #    width=800,
        #    height=600
        #    )


    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")



@click.command("media")
@click.argument(
    "arquivo_json",
)
def analise_media(arquivo_json):

    from apps.model.caso import Caso
    from apps.model.sintese import Sintese
    from apps.indicadores.indicadores_medios import IndicadoresMedios
    from apps.indicadores.indicadores_temporais import IndicadoresTemporais
    from apps.model.unidade import UnidadeSintese
    from apps.model.argumento import Argumento
    from apps.graficos.graficos import Graficos

    if os.path.isfile(arquivo_json):
        with open(arquivo_json, "r") as f:
            dados = json.load(f)
        # Lê dados de entrada
        estudo = dados["estudo"]
        nome_caso_referencia = dados["nome_caso_referencia"]
        # Cria objetos do estudo
        casos = [Caso.from_dict(d) for d in dados["casos"]]
        sinteses = [Sintese.from_dict(d) for d in dados["sinteses"]]
        args = [Argumento.from_dict(d) for d in dados["argumentos"]]
        
        indicadores_medios = IndicadoresMedios(casos, nome_caso_referencia)
        indicadores_temporais = IndicadoresTemporais(casos)
        graficos = Graficos(casos)
        # Gera saídas do estudo
        diretorio_saida = f"resultados/{estudo}/media"
        os.makedirs(diretorio_saida, exist_ok=True)
        for sts in sinteses:
            espacial = sts.sintese.split("_")[1]
            for arg in args:
                if(espacial == arg.chave):
                    unity = UnidadeSintese(sts, "estagios", arg)
                    diretorio_saida_arg = diretorio_saida+"/"+arg.chave+"/"+arg.nome
                    os.makedirs(diretorio_saida_arg, exist_ok=True)
                   
                    df_unity = indicadores_medios.retorna_df_concatenado(unity.sintese, unity.fitroColuna , unity.filtroArgumento )
                    indicadores_medios.exportar(df_unity, diretorio_saida_arg,  "medias_"+unity.titulo+"_"+estudo)

                    fig = graficos.gera_grafico_barra(df_unity["valor"], df_unity["caso"],  unity.legendaEixoX, unity.legendaEixoY, 2, unity.titulo)
                    graficos.exportar(fig, diretorio_saida_arg, "medias_"+unity.titulo+"_"+estudo)

                    df_unity_incr = indicadores_medios.retorna_DF_cenario_medio_incremental_percentual(unity.sintese, unity.fitroColuna , unity.filtroArgumento )
                    indicadores_medios.exportar(df_unity_incr, diretorio_saida_arg, "medias_incr_"+unity.titulo+"_"+estudo)
                    
                    fig = graficos.gera_grafico_barra(df_unity_incr["valor"], df_unity_incr["caso"],  unity.legendaEixoX, unity.legendaEixoY, 2, unity.titulo)
                    graficos.exportar(fig, diretorio_saida_arg, "medias_incr_"+unity.titulo+"_"+estudo)
    
    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")




@click.command("anual")
@click.argument(
    "arquivo_json",
)
def analise_anual(arquivo_json):

    from apps.model.caso import Caso
    from apps.model.sintese import Sintese
    from apps.indicadores.indicadores_anuais import IndicadoresAnuais
    from apps.model.unidade import UnidadeSintese
    from apps.model.argumento import Argumento
    from apps.graficos.graficos import Graficos

    if os.path.isfile(arquivo_json):
        with open(arquivo_json, "r") as f:
            dados = json.load(f)
        # Lê dados de entrada
        estudo = dados["estudo"]
        nome_caso_referencia = dados["nome_caso_referencia"]
        # Cria objetos do estudo
        casos = [Caso.from_dict(d) for d in dados["casos"]]
        sinteses = [Sintese.from_dict(d) for d in dados["sinteses"]]
        args = [Argumento.from_dict(d) for d in dados["argumentos"]]
        indicadores_anuais = IndicadoresAnuais(casos, nome_caso_referencia)
        graficos = Graficos(casos)
        # Gera saídas do estudo
        diretorio_saida = f"resultados/{estudo}/anual"
        os.makedirs(diretorio_saida, exist_ok=True)

        for sts in sinteses:
            espacial = sts.sintese.split("_")[1]
            for arg in args:
                if(espacial == arg.chave):
                    unity = UnidadeSintese(sts, "estagios", arg)
                    diretorio_saida_arg = diretorio_saida+"/"+arg.chave+"/"+arg.nome
                    os.makedirs(diretorio_saida_arg, exist_ok=True)

                    df = indicadores_anuais.retorna_df_concatenado(unity.sintese, unity.fitroColuna , unity.filtroArgumento )
                    indicadores_anuais.exportar(df, diretorio_saida_arg,  "anual_"+unity.titulo+"_"+estudo)

                    ## GRAFICOS ANOS DISCRETIZADOS
                    fig = graficos.gera_grafico_barras_diferentes(df, "anos", "valor", "caso",  unity.legendaEixoX, unity.legendaEixoY, 2, unity.titulo+"_anos_discretizados")
                    graficos.exportar(fig, diretorio_saida_arg, "anual_"+unity.titulo+"_anos_discretizados_"+estudo)

                    df_unity = indicadores_anuais.retorna_DF_cenario_anual_medio_incremental_percentual(unity.sintese, unity.fitroColuna , unity.filtroArgumento )
                    indicadores_anuais.exportar(df_unity, diretorio_saida_arg,  "anual_incr_"+unity.titulo+"_"+estudo)
                
                    #ANOS DISCRETIZADOS INCREMENTAL
                    fig = graficos.gera_grafico_barras_diferentes(df_unity, "anos", "valor", "caso",  unity.legendaEixoX, unity.legendaEixoY, 2, unity.titulo+"_incremental")
                    graficos.exportar(fig, diretorio_saida_arg, "anual_"+unity.titulo+"_anos_discretizados_incremental_"+estudo)

                    ## PRIMEIRO ANO INCREMENTAL
                    fig = graficos.gera_grafico_barras_diferentes(
                        df_unity.loc[(df_unity["anos"] == df_unity["anos"].iloc[0])], 
                        "anos", 
                        "valor", 
                        "caso",  
                        unity.legendaEixoX, 
                        unity.legendaEixoY, 
                        2, 
                        unity.titulo+"_incremental"
                    )
                    graficos.exportar(fig, diretorio_saida_arg, "anual_"+unity.titulo+"_primeiro_ano_incremental_"+estudo)
        
                    df_unity = indicadores_anuais.retorna_df_concatenado_acumulado(unity.sintese, unity.fitroColuna , unity.filtroArgumento )
                    indicadores_anuais.exportar(df_unity, diretorio_saida_arg,  "anual_acum_"+unity.titulo+"_"+estudo)
                    
                    ## GRAFICOS PRIMEIRO ANO
                    df = df_unity.loc[(df_unity["anos"] == df_unity["anos"].iloc[0])]
                    fig = graficos.gera_grafico_barra(df["valor"], df["caso"],  unity.legendaEixoX, unity.legendaEixoY, 2, unity.titulo+"_primeiro_ano")
                    graficos.exportar(fig, diretorio_saida_arg, "anual_"+unity.titulo+"_primeiro_ano_"+estudo)

                    ## OUTROS ANOS
                    df = df_unity.loc[(df_unity["anos"] != df_unity["anos"].iloc[0])]
                    fig = graficos.gera_grafico_barra(df["valor"], df["caso"],  unity.legendaEixoX, unity.legendaEixoY, 2, unity.titulo+"_outros_anos")
                    graficos.exportar(fig, diretorio_saida_arg, "anual_"+unity.titulo+"_outros_anos_"+estudo)

                    ## GRAFICOS ANO E OUTROS ANOS DISCRETIZADOS
                    fig = graficos.gera_grafico_barras_diferentes(df_unity, "anos", "valor", "caso",  unity.legendaEixoX, unity.legendaEixoY, 2, unity.titulo+"_primeiro_ano_outros_anos")
                    graficos.exportar(fig, diretorio_saida_arg, "anual_"+unity.titulo+"_primeiro_ano_e_outros_anos_"+estudo)
                            
                    df_unity = indicadores_anuais.retorna_DF_cenario_anual_acumulado_medio_incremental_percentual(unity.sintese, unity.fitroColuna , unity.filtroArgumento )
                    indicadores_anuais.exportar(df_unity, diretorio_saida_arg,  "anual_acum_incr_"+unity.titulo+"_"+estudo)
        
                    #ANOS DISCRETIZADOS INCREMENTAL
                    fig = graficos.gera_grafico_barras_diferentes(df_unity, "anos", "valor", "caso",  unity.legendaEixoX, unity.legendaEixoY, 2, unity.titulo+"_incremental")
                    graficos.exportar(fig, diretorio_saida_arg, "anual_"+unity.titulo+"_anos_discretizados_incremental_"+estudo)
        
                    ## PRIMEIRO ANO INCREMENTAL
                    df = df_unity.loc[(df_unity["anos"] != df_unity["anos"].iloc[0])]
                    fig = graficos.gera_grafico_barras_diferentes(df, "anos", "valor", "caso",  unity.legendaEixoX, unity.legendaEixoY, 2, unity.titulo+"_incremental")
                    graficos.exportar(fig, diretorio_saida_arg, "anual_"+unity.titulo+"_outros_anos_incremental_"+estudo)

                        
    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")





@click.command("analise-cenarios")
@click.argument(
    "arquivo_json",
)
def analise_cenarios(arquivo_json):
    """
    Calibração do CVaR.
    """
    from apps.model.caso import Caso
    from apps.model.usina import UsinaAvalicao
    from apps.indicadores.indicadores_cenarios import IndicadoresCenarios
    from apps.model.unidade import UnidadeSintese
    from apps.graficos.graficos import Graficos

    if os.path.isfile(arquivo_json):
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

            

            
    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")





@click.command("conjuntoCasos")
@click.argument(
    "arquivo_json",
)
def analise_conjuntoCasos(arquivo_json):

    from apps.model.caso import Caso
    from apps.model.sintese import Sintese
    from apps.model.unidade import UnidadeSintese
    from apps.graficos.graficos import Graficos
    from apps.model.argumento import Argumento
    from apps.model.conjuntoCasos import ConjuntoCasos
    from apps.indicadores.indicadores_medios import IndicadoresMedios
    from apps.indicadores.indicadores_anuais import IndicadoresAnuais
    from apps.indicadores.indicadores_temporais import IndicadoresTemporais
    
    if os.path.isfile(arquivo_json):
        with open(arquivo_json, "r") as f:
            dados = json.load(f)
        # Lê dados de entrada
        estudo = dados["estudo"]
        conjuntoCasos = [ConjuntoCasos.from_dict(d) for d in dados["conjuntos"]]
        nome_caso_referencia = ""

        sinteses = [Sintese.from_dict(d) for d in dados["sinteses"]]
        args = [Argumento.from_dict(d) for d in dados["argumentos"]]
        # Gera saídas do estudo
        diretorio_saida = f"resultados/{estudo}/conjunto"
        os.makedirs(diretorio_saida, exist_ok=True)

        for sts in sinteses:
            espacial = sts.sintese.split("_")[1]
            for arg in args:
                if(espacial == arg.chave):
                    unity = UnidadeSintese(sts, "estagios", arg)
                    diretorio_saida_arg = diretorio_saida+"/"+arg.chave+"/"+arg.nome
                    os.makedirs(diretorio_saida_arg, exist_ok=True)
                
                    listaConjDF = []
                    listaConjDF_Anual = []
                    listaConjDF_Temporal_Primeiro_Mes = []
                    listaConjDF_Temporal_Segundo_Mes = []
                    mapaConjDF_Temporal = {}
                    listaNomes = []
                    mapCores = {}
                    for conjunto in conjuntoCasos:
                        indicador_conj_medio = IndicadoresMedios(conjunto.casos, nome_caso_referencia)
                        indicadores_anuais = IndicadoresAnuais(conjunto.casos, nome_caso_referencia)
                        indicadores_temporais = IndicadoresTemporais(conjunto.casos)
                        graficos = Graficos(conjunto.casos)
                        
                        
                        df_unity = indicador_conj_medio.retorna_df_concatenado(unity.sintese, unity.fitroColuna , unity.filtroArgumento )
                        df_unity = df_unity.rename(columns={"valor": conjunto.nome}).reset_index(drop = True)
                        #df_unity["conjunto"] = conjunto.nome
        
                        df_anual = indicadores_anuais.retorna_df_concatenado_acumulado(unity.sintese, unity.fitroColuna , unity.filtroArgumento )
                        df_anual = df_anual.rename(columns={"valor": conjunto.nome}).reset_index(drop = True)
        
                        df_temporal = indicadores_temporais.retorna_df_concatenado(unity.sintese, unity.fitroColuna , unity.filtroArgumento )
                        df_temporal = df_temporal.rename(columns={"valor": conjunto.nome}).reset_index(drop = True)
        
                        df_temporal_primeiro_mes = df_temporal.loc[df_temporal["estagio"] == 1 ].reset_index(drop = True)
                        df_temporal_segundo_mes = df_temporal.loc[df_temporal["estagio"] == 2 ].reset_index(drop = True)
                        listaConjDF.append(df_unity)
                        listaConjDF_Anual.append(df_anual)
                        listaConjDF_Temporal_Primeiro_Mes.append(df_temporal_primeiro_mes)
                        listaConjDF_Temporal_Segundo_Mes.append(df_temporal_segundo_mes)
                        mapaConjDF_Temporal[conjunto.nome]  = df_temporal
                        
                        listaNomes.append(conjunto.nome)
                        mapCores[conjunto.nome] = conjunto.cor
        
                    df_concat = pd.concat(listaConjDF, axis=1)
                    df_concatenado = df_concat.loc[:,~df_concat.columns.duplicated()].copy()   #df_concat.T.drop_duplicates().T
        
                    df_concat_anual = pd.concat(listaConjDF_Anual, axis=1)
                    df_concatenado_anual = df_concat_anual.loc[:,~df_concat_anual.columns.duplicated()].copy()   #df_concat.T.drop_duplicates().T
        
                    df_concat_temporal_primeiro_mes = pd.concat(listaConjDF_Temporal_Primeiro_Mes, axis=1)
                    df_concatenado_temporal_primeiro_mes = df_concat_temporal_primeiro_mes.loc[:,~df_concat_temporal_primeiro_mes.columns.duplicated()].copy()   #df_concat.T.drop_duplicates().T
                    
                    df_concat_temporal_segundo_mes = pd.concat(listaConjDF_Temporal_Segundo_Mes, axis=1)
                    df_concatenado_temporal_segundo_mes = df_concat_temporal_segundo_mes.loc[:,~df_concat_temporal_segundo_mes.columns.duplicated()].copy()   #df_concat.T.drop_duplicates().T

                    indicador_conj_medio.exportar(df_concatenado, diretorio_saida_arg,  "conj_med_"+unity.titulo+"_"+estudo)
                    indicadores_anuais.exportar(df_concatenado_anual, diretorio_saida_arg,  "conj_anual_"+unity.titulo+"_"+estudo)
                    indicadores_temporais.exportar(df_concatenado_temporal_primeiro_mes, diretorio_saida_arg,  "primeiro_mes_"+unity.titulo+"_"+estudo)
                    indicadores_temporais.exportar(df_concatenado_temporal_segundo_mes, diretorio_saida_arg,  "segundo_mes_"+unity.titulo+"_"+estudo)


                    fig = graficos.gera_grafico_linhas_diferentes_casos(df_concatenado, "caso", listaNomes, mapCores, unity.legendaEixoY, unity.legendaEixoX, unity.titulo)
                    graficos.exportar(fig, diretorio_saida_arg, "conj_medias_"+unity.titulo+"_"+estudo)
                    
                    df_primeiro_ano = df_concatenado_anual.loc[(df_concatenado_anual["anos"] == df_concatenado_anual["anos"].iloc[0])]
                    fig = graficos.gera_grafico_linhas_diferentes_casos(df_primeiro_ano, "caso", listaNomes, mapCores, unity.legendaEixoY, unity.legendaEixoX, unity.titulo+"_Primeiro_Ano")
                    graficos.exportar(fig, diretorio_saida_arg, "conj_anual_"+unity.titulo+"_primeiro_ano_"+estudo)
                    
                    df_outros_anos = df_concatenado_anual.loc[(df_concatenado_anual["anos"] == df_concatenado_anual["anos"].iloc[1])]
                    fig = graficos.gera_grafico_linhas_diferentes_casos(df_outros_anos, "caso", listaNomes, mapCores, unity.legendaEixoY, unity.legendaEixoX, unity.titulo+"_Outros_Anos")
                    graficos.exportar(fig, diretorio_saida_arg, "conj_anual_"+unity.titulo+"_outros_anos_"+estudo)
                    
                    fig = graficos.gera_grafico_linhas_diferentes_casos(df_concatenado_temporal_primeiro_mes, "caso", listaNomes, mapCores, unity.legendaEixoY, unity.legendaEixoX, unity.titulo+"_Primeiro_Mes")
                    graficos.exportar(fig, diretorio_saida_arg, "conj_temporal_"+unity.titulo+"_primeiro_mes_"+estudo)
                    
                    fig = graficos.gera_grafico_linhas_diferentes_casos(df_concatenado_temporal_segundo_mes, "caso", listaNomes, mapCores, unity.legendaEixoY, unity.legendaEixoX, unity.titulo+"_Segundo_Mes")
                    graficos.exportar(fig, diretorio_saida_arg, "conj_temporal_"+unity.titulo+"_segundo_mes_"+estudo)
        
                    mapaFig = graficos.subplot_gera_grafico_linha_casos(conjuntoCasos, mapaConjDF_Temporal, unity.legendaEixoY , unity.legendaEixoX, unity.titulo)
                    for titulo in mapaFig:
                        graficos.exportar(mapaFig[titulo], diretorio_saida_arg, titulo+estudo, 2000, 900)
            
    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")


cli.add_command(analise_pareto)
cli.add_command(eco)
cli.add_command(analise_temporal)
cli.add_command(analise_media)
cli.add_command(analise_anual)
cli.add_command(analise_conjuntoCasos)
cli.add_command(analise_cenarios)
