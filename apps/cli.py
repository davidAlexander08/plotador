import click
import os
import json
from apps.interface.dados_json_caso import Dados_json_caso
from apps.utils.log import Log
from pathlib import Path
from apps.model.argumento import Argumento

option_xinf = click.option("--xinf", default=0,  help="Ponto Inferior do Eixo X")
option_xsup = click.option("--xsup", default=60, help="Ponto Superior do Eixo X")
option_estagio = click.option( "--estagio",  default="",  help="Estagio Especifico para Plotar")
option_cenario = click.option("--cenario",   default="mean",  help="Cenario Especifico para Plotar")
option_sintese = click.option("--sintese",  default="",  help="Sintese Especifica a ser Plotada")
option_argumentos = click.option("--argumentos",  default = None, help="Argumentos Especifico a ser plotado como SUDESTE, TRES MARIAS, etc...  Separados por virgula")
option_chave = click.option("--chave",  default = None,  help="Chaves para o argumento: None, SBM, REE, UHE")
option_largura = click.option("--largura",  default="1500",   help="Sintese Especifica a ser Plotada") #VALOR INTERESSANTE PARA RELATORIOS E 1200
option_altura = click.option( "--altura",   default="1200",   help="Sintese Especifica a ser Plotada") #VALOR INTERESSANTE PARA RELATORIOS E 375 e 550
option_eixox = click.option( "--eixox",   default="estagio",   help="Eixo X, valores como estagio, dataInicio, dataFim")
option_cronologico = click.option("--cronologico",   default="False",    help="Sintese Especifica a ser Plotada")
option_labely = click.option("--labely",   default=None, help="Label Y para todos os graficos Plotados")
option_labelx = click.option( "--labelx",   default=None,  help="Label X para todos os graficos Plotados")
option_booltitulo = click.option("--booltitulo",   default="True", help="Ativa ou desativa o titulo de figuras")
option_titulo = click.option("--titulo",    default=" ", help="Nome do Titulo de Todas as Imagens")
option_showlegend = click.option("--showlegend",    default=" ", help="True default. False desativa legendas")
option_yinf  = click.option("--yinf", default=None, help="Ponto Inferior do Eixo Y")
option_ysup = click.option("--ysup", default=None, help="Ponto Superior do Eixo Y")
option_tamanho = click.option("--tamanho", default=None, help="Tamanho da letra")
option_json = click.option("--arquivo_json", "--json", default = None, help ="definicao do arquivo json. Caso nenhum, ele considera estar dentro da pasta do caso")
option_subplot = click.option("--subplot", default = None, help ="definicao do numero de colunas e linhas do subplot separados por virgula")
option_boxplot = click.option("--boxplot", default = None, help = "Se True ativa a opcao boxplots, habilitando graficos boxplot")
option_csv = click.option("--csv", default = "True", help = "Default True, se False nao imprime mais os csvs")
option_html = click.option("--html", default = None, help = "Default False, se True gera o html da figura")
option_outpath = click.option("--outpath", default = None, help = "Muda o caminho de saida da figura e csv a serem gerados")
option_txt = click.option("--txt", default = None, help ="definicao do arquivo txt. Caso nenhum, ele considera estar dentro da pasta do caso")

@click.group()
def cli():
    pass

@click.command("report")
@option_outpath
@option_json
@option_txt
@option_titulo
def realiza_report(outpath, arquivo_json, txt, titulo):
    from apps.services.report import Report
    Report(outpath, arquivo_json, txt, titulo)

@click.command("temporal")
@option_xinf
@option_xsup
@option_estagio
@option_cenario
@option_sintese
@option_argumentos
@option_chave
@option_largura
@option_altura
@option_eixox
@option_cronologico
@option_labely
@option_labelx
@option_booltitulo
@option_titulo
@option_showlegend
@option_json
@option_tamanho
@option_boxplot
@option_csv
@option_html
@option_outpath
def analise_temporal(arquivo_json, xinf, xsup, estagio, cenario, sintese, argumentos, chave, largura, altura, eixox, cronologico, labely, booltitulo, titulo, showlegend, labelx, tamanho, boxplot, csv, html, outpath):
    from apps.services.temporal import Temporal
    flag_diretorio = 0
    if(arquivo_json is None):
        path = __file__.split("/")
        path.pop()
        arquivo_json = "/".join(path)+"/exemplo.json"
        flag_diretorio  = 1
    data = Dados_json_caso(arquivo_json)
    if (flag_diretorio == 1):
        data.estudo = "_default"
        data.casos[0].nome = " "
        data.casos[0].caminho = os.getcwd()
        if os.path.isfile("dger.dat"):
            data.casos[0].modelo = "NEWAVE"
            data.args = [Argumento(["SUDESTE","NORDESTE","NORTE","SUL"], "SBM", "SBMs")]
        elif os.path.isfile("decomp.tim"):
            data.casos[0].modelo = "DECOMP"
            data.args = [Argumento(["SE","NE","N","S"], "SBM", "SBMs")]
        elif os.path.isfile("entdados.dat"):
            data.casos[0].modelo = "DESSEM"
            data.args = [Argumento(["SE","NE","N","S"], "SBM", "SBMs")]
        else: 
            raise FileNotFoundError(f"NAO SE ENCONTRA NA PASTA DE UM CASO OU ARQUIVO JSON NAO EXISTE.")
    Temporal(data, xinf, xsup, estagio, cenario, sintese, largura, altura, eixox, cronologico, labely, booltitulo, titulo, showlegend, labelx, argumentos, chave, tamanho, boxplot, csv, html, outpath)


@click.command("conjunto")
@option_xinf
@option_xsup
@option_estagio
@option_cenario
@option_sintese
@option_largura
@option_altura
@option_eixox
@option_cronologico
@option_titulo
@option_subplot
@option_argumentos
@option_chave
@option_yinf
@option_ysup
@option_labelx
@option_tamanho
@click.argument(
    "arquivo_json",
)
def analise_conjuntoCasos(arquivo_json, xinf, xsup, yinf, ysup,estagio, cenario, sintese, argumentos, chave, largura, altura, eixox, cronologico, titulo, subplot, labelx, tamanho):
    from apps.services.conjunto import Conjunto
    if os.path.isfile(arquivo_json):
        data = Dados_json_caso(arquivo_json)
        Conjunto(data, xinf, xsup, yinf, ysup,estagio, cenario, sintese, argumentos, chave, largura, altura, eixox, cronologico, titulo, subplot, labelx, tamanho)
    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")

@click.command("fcf")
@click.argument(
    "arquivo_json",
)
@option_xinf
@option_xsup
@option_largura
@option_altura
@click.option(
    "--eco",
    default="False", #VALOR INTERESSANTE PARA RELATORIOS E 375 e 550
    help="Plota tambem o eco dos cortes",
)
@option_yinf
@option_ysup

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
@option_xinf
@option_xsup
@option_largura
@option_altura
@click.option(
    "--eco",
    default="False", #VALOR INTERESSANTE PARA RELATORIOS E 375 e 550
    help="Plota tambem o eco dos cortes",
)

@option_yinf
@option_ysup

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
@option_largura
@option_altura
@option_html
@option_outpath
@option_titulo
@option_tamanho
def analise_tempo(arquivo_json, largura, altura, html, outpath, titulo, tamanho):
    from apps.services.tempo import Tempo
    if os.path.isfile(arquivo_json):
        data = Dados_json_caso(arquivo_json)
        Tempo(data, largura, altura, html, outpath, titulo, tamanho)          
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


cli.add_command(analise_pareto)
cli.add_command(eco)
cli.add_command(realiza_report)
cli.add_command(analise_temporal)
cli.add_command(analise_media)
cli.add_command(analise_anual)
cli.add_command(analise_conjuntoCasos)
cli.add_command(analise_cenarios)
cli.add_command(analise_fcf)
cli.add_command(analise_nwlistcf)
cli.add_command(analise_tempo)
cli.add_command(analise_cascatador)
