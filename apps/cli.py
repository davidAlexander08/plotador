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
    default="True", #VALOR INTERESSANTE PARA RELATORIOS E 375 e 550
    help="Sintese Especifica a ser Plotada",
)
@click.argument(
    "arquivo_json",
)
def analise_temporal(arquivo_json, xinf, xsup, estagio, cenario, sintese, largura, altura, eixox, cronologico):
    from apps.services.temporal import Temporal
    if os.path.isfile(arquivo_json):
        data = Dados_json_caso(arquivo_json)
        Temporal(data, xinf, xsup, estagio, cenario, sintese, largura, altura, eixox, cronologico)
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
@click.argument(
    "arquivo_json",
)
def analise_conjuntoCasos(arquivo_json):
    from apps.services.conjunto import Conjunto
    if os.path.isfile(arquivo_json):
        data = Dados_json_caso(arquivo_json)
        Conjunto(data)
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
def analise_fcf(arquivo_json):
    from apps.services.fcf import FCF
    if os.path.isfile(arquivo_json):
        data = Dados_json_caso(arquivo_json)
        FCF(data)          
    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")

@click.command("tempo")
@click.argument(
    "arquivo_json",
)
def analise_tempo(arquivo_json):
    from apps.services.tempo import Tempo
    if os.path.isfile(arquivo_json):
        data = Dados_json_caso(arquivo_json)
        Tempo(data)          
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
cli.add_command(analise_tempo)
cli.add_command(analise_cascatador)