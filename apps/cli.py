import click
import os
import json
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
        Eco(arquivo_json)
    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")

@click.command("temporal")
@click.argument(
    "arquivo_json",
)
def analise_temporal(arquivo_json):
    from apps.services.temporal import Temporal
    if os.path.isfile(arquivo_json):
        Temporal(arquivo_json)
    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")

@click.command("media")
@click.argument(
    "arquivo_json",
)
def analise_media(arquivo_json):
    from apps.services.media import Media
    if os.path.isfile(arquivo_json):
        Media(arquivo_json)
    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")

@click.command("anual")
@click.argument(
    "arquivo_json",
)
def analise_anual(arquivo_json):
    from apps.services.anual import Anual
    if os.path.isfile(arquivo_json):
        Anual(arquivo_json)             
    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")

@click.command("cenarios")
@click.argument(
    "arquivo_json",
)
def analise_cenarios(arquivo_json):
    from apps.services.cenarios import Cenarios
    if os.path.isfile(arquivo_json):
        Cenarios(arquivo_json)
    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")

@click.command("conjunto")
@click.argument(
    "arquivo_json",
)
def analise_conjuntoCasos(arquivo_json):
    from apps.services.conjunto import Conjunto
    if os.path.isfile(arquivo_json):
        Conjunto(arquivo_json)
    else:
        raise FileNotFoundError(f"Arquivo {arquivo_json} não encontrado.")


cli.add_command(analise_pareto)
cli.add_command(eco)
cli.add_command(analise_temporal)
cli.add_command(analise_media)
cli.add_command(analise_anual)
cli.add_command(analise_conjuntoCasos)
cli.add_command(analise_cenarios)
