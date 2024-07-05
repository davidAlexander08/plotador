import click
import os
import json
from apps.interface.dados_json_caso import Dados_json_caso
from apps.utils.log import Log
@click.group()
def cli():
    """
    Aplicação para reproduzir estudos de metodologias
    de planejamento energético feitos no âmbito
    da CPAMP pelo ONS.
    """
    pass

@click.command("pareto")
@click.argument(
    "arquivo_json",
)
def analise_pareto(arquivo_json):
    from apps.services.pareto import Pareto
    if os.path.isfile(arquivo_json):

        Pareto(arquivo_json)
    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")

@click.command("eco")
@click.argument(
    "arquivo_json",
)
def eco(arquivo_json):
    from apps.services.eco import Eco
    if os.path.isfile(arquivo_json):
        data = Dados_json_caso(arquivo_json)
        Eco(data)
    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")

@click.command("temporal")
@click.option(
    "--xinf",
    default=0,
    help="Ponto Inferior do Eixo X",
)
@click.option(
    "--xsup",
    default=60,
    help="Ponto Superior do Eixo X",
)
@click.option(
    "--estagio",
    default="",
    help="Estagio Especifico para Plotar",
)
@click.option(
    "--cenario",
    default="mean",
    help="Cenario Especifico para Plotar",
)
@click.option(
    "--sintese",
    default="",
    help="Sintese Especifica a ser Plotada",
)
@click.option(
    "--argumento",
    default = None,
    help="Argumento Especifico a ser plotado como SUDESTE, TRES MARIAS, etc... ",
)
@click.option(
    "--chave",
    default = None,
    help="Chaves para o argumento: None, SBM, REE, UHE",
)
@click.option(
    "--largura",
    default="1500", #VALOR INTERESSANTE PARA RELATORIOS E 1200
    help="Sintese Especifica a ser Plotada",
)
@click.option(
    "--altura",
    default="1200", #VALOR INTERESSANTE PARA RELATORIOS E 375 e 550
    help="Sintese Especifica a ser Plotada",
)
@click.option(
    "--eixox",
    default="estagio",
    help="Eixo X, valores como estagio, dataInicio, dataFim",
)
@click.option(
    "--cronologico",
    default="False", 
    help="Sintese Especifica a ser Plotada",
)
@click.option(
    "--labely",
    default=None, 
    help="Label Y para todos os graficos Plotados",
)
@click.option(
    "--labelx",
    default=None, 
    help="Label X para todos os graficos Plotados",
)
@click.option(
    "--booltitulo",
    default="True", 
    help="Ativa ou desativa o titulo de figuras",
)
@click.option(
    "--titulo",
    default=" ", 
    help="Nome do Titulo de Todas as Imagens",
)
@click.option(
    "--showlegend",
    default=" ", 
    help="True default. False desativa legendas",
)
@click.argument(
    "arquivo_json",
)
def analise_temporal(arquivo_json, xinf, xsup, estagio, cenario, sintese, argumento, chave, largura, altura, eixox, cronologico, labely, booltitulo, titulo, showlegend, labelx):
    from apps.services.temporal import Temporal
    if os.path.isfile(arquivo_json):
        data = Dados_json_caso(arquivo_json)
        Temporal(data, xinf, xsup, estagio, cenario, sintese, largura, altura, eixox, cronologico, labely, booltitulo, titulo, showlegend, labelx, argumento, chave)
    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")

@click.command("media")
@click.argument(
    "arquivo_json",
)
def analise_media(arquivo_json):
    from apps.services.media import Media
    if os.path.isfile(arquivo_json):
        data = Dados_json_caso(arquivo_json)
        Media(data)
    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")

@click.command("anual")
@click.argument(
    "arquivo_json",
)
def analise_anual(arquivo_json):
    from apps.services.anual import Anual
    if os.path.isfile(arquivo_json):
        data = Dados_json_caso(arquivo_json)
        Anual(data)             
    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")


@click.command("cenarios")
@click.argument(
    "arquivo_json",
)
def analise_cenarios(arquivo_json):
    from apps.services.cenarios import Cenarios
    if os.path.isfile(arquivo_json):
        data = Dados_json_caso(arquivo_json)
        Cenarios(data)
    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")

@click.command("conjunto")
@click.option(
    "--xinf",
    default=0,
    help="Ponto Inferior do Eixo X",
)
@click.option(
    "--xsup",
    default=60,
    help="Ponto Superior do Eixo X",
)
@click.option(
    "--estagio",
    default="",
    help="Estagio Especifico para Plotar",
)
@click.option(
    "--cenario",
    default="mean",
    help="Cenario Especifico para Plotar",
)
@click.option(
    "--sintese",
    default="",
    help="Sintese Especifica a ser Plotada",
)
@click.option(
    "--largura",
    default="1500", #VALOR INTERESSANTE PARA RELATORIOS E 1200
    help="Sintese Especifica a ser Plotada",
)
@click.option(
    "--altura",
    default="1200", #VALOR INTERESSANTE PARA RELATORIOS E 375 e 550
    help="Sintese Especifica a ser Plotada",
)
@click.option(
    "--eixox",
    default="estagio",
    help="Eixo X, valores como estagio, dataInicio, dataFim",
)
@click.option(
    "--cronologico",  #plotador conjunto --cronologico True --xsup 48 conjunto.json #DESSEM
    default="False", 
    help="Sintese Especifica a ser Plotada",
)
@click.argument(
    "arquivo_json",
)
def analise_conjuntoCasos(arquivo_json, xinf, xsup, estagio, cenario, sintese, largura, altura, eixox, cronologico):
    from apps.services.conjunto import Conjunto
    if os.path.isfile(arquivo_json):
        data = Dados_json_caso(arquivo_json)
        Conjunto(data, xinf, xsup, estagio, cenario, sintese, largura, altura, eixox, cronologico)
    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")
    
@click.command("operacao")
@click.argument(
    "arquivo_json",
)
def analise_operacional(arquivo_json):
    from apps.services.anual import Anual
    from apps.services.media import Media
    from apps.services.temporal import Temporal
    if os.path.isfile(arquivo_json):
        data = Dados_json_caso(arquivo_json)
        Temporal(data)
        Media(data)
        Anual(data )             
    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")


@click.command("fcf")
@click.argument(
    "arquivo_json",
)
@click.option(
    "--xinf",
    default=None,
    help="Ponto Inferior do Eixo X",
)
@click.option(
    "--xsup",
    default=None,
    help="Ponto Superior do Eixo X",
)
@click.option(
    "--largura",
    default="1500", #VALOR INTERESSANTE PARA RELATORIOS E 1200
    help="Largura Figura",
)
@click.option(
    "--altura",
    default="1200", #VALOR INTERESSANTE PARA RELATORIOS E 375 e 550
    help="Altura Figura",
)
@click.option(
    "--eco",
    default="False", #VALOR INTERESSANTE PARA RELATORIOS E 375 e 550
    help="Plota tambem o eco dos cortes",
)
@click.option(
    "--yinf",
    default=None,
    help="Ponto Inferior do Eixo Y",
)
@click.option(
    "--ysup",
    default=None,
    help="Ponto Superior do Eixo Y",
)

def analise_fcf(arquivo_json, xinf, xsup, largura, altura, eco, yinf, ysup):
    from apps.services.fcf import FCF
    if os.path.isfile(arquivo_json):
        data = Dados_json_caso(arquivo_json)
        FCF(data, xinf, xsup, largura, altura, eco, yinf, ysup)          
    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")



@click.command("nwlistcf")
@click.argument(
    "arquivo_json",
)
@click.option(
    "--xinf",
    default=None,
    help="Ponto Inferior do Eixo X",
)
@click.option(
    "--xsup",
    default=None,
    help="Ponto Superior do Eixo X",
)
@click.option(
    "--largura",
    default="1500", #VALOR INTERESSANTE PARA RELATORIOS E 1200
    help="Largura Figura",
)
@click.option(
    "--altura",
    default="1200", #VALOR INTERESSANTE PARA RELATORIOS E 375 e 550
    help="Altura Figura",
)
@click.option(
    "--eco",
    default="False", #VALOR INTERESSANTE PARA RELATORIOS E 375 e 550
    help="Plota tambem o eco dos cortes",
)
@click.option(
    "--yinf",
    default=None,
    help="Ponto Inferior do Eixo Y",
)
@click.option(
    "--ysup",
    default=None,
    help="Ponto Superior do Eixo Y",
)

@click.option(
    "--ree",
    default=None,
    help="REE para impressao. Um REE unico.",
)

@click.option(
    "--box",
    default="True",
    help="True default. False desativa Boxplots",
)

@click.option(
    "--linhas",
    default="True",
    help="True default. False desativa graficos de Linha",
)

@click.option(
    "--series",
    default=None,
    help="Lista de series separadas por virgula a serem investigadas. Ex: 192,194",
)

@click.option(
    "--iters",
    default=None,
    help="Lista de iteracoes separados por virgula a serem investigadas. Ex: 3,4",
)

@click.option(
    "--periodos",
    default=None,
    help="Lista de periodos separados por virgula a serem investigados. Ex: 20,21",
)

def analise_nwlistcf(arquivo_json, xinf, xsup, largura, altura, eco, yinf, ysup, ree, box, linhas, series, iters, periodos):
    from apps.services.nwlistcf import NWLISTCF
    if os.path.isfile(arquivo_json):
        data = Dados_json_caso(arquivo_json)
        NWLISTCF(data, xinf, xsup, largura, altura, eco, yinf, ysup, ree, box, linhas, series, iters, periodos)          
    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")

@click.command("tempo")
@click.argument(
    "arquivo_json",
)
@click.option(
    "--largura",
    default="1500", #VALOR INTERESSANTE PARA RELATORIOS E 1200
    help="Largura Figura",
)
@click.option(
    "--altura",
    default="1200", #VALOR INTERESSANTE PARA RELATORIOS E 375 e 550
    help="Altura Figura",
)
def analise_tempo(arquivo_json, largura, altura):
    from apps.services.tempo import Tempo
    if os.path.isfile(arquivo_json):
        data = Dados_json_caso(arquivo_json)
        Tempo(data, largura, altura)          
    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")


@click.command("cascatador")
@click.argument(
    "arquivo_json",
)
def analise_cascatador(arquivo_json):
    from apps.services.cascatador import Cascatador
    if os.path.isfile(arquivo_json):
        data = Dados_json_caso(arquivo_json)
        Cascatador(data)          
    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")

cli.add_command(analise_pareto)
cli.add_command(eco)
cli.add_command(analise_temporal)
cli.add_command(analise_media)
cli.add_command(analise_anual)
cli.add_command(analise_conjuntoCasos)
cli.add_command(analise_cenarios)
cli.add_command(analise_operacional)
cli.add_command(analise_fcf)
cli.add_command(analise_nwlistcf)
cli.add_command(analise_tempo)
cli.add_command(analise_cascatador)
