

import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import os
import json
import subprocess
import re

class Report:
    def __init__(self):

        # Create a simple line plot
        x = [1, 2, 3, 4, 5]
        y = [10, 15, 13, 17, 20]

        fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines', name='Line Plot'))
        plot_html = pio.to_html(fig, full_html=False)
        # Read the HTML template
        with open("template.html", "r") as file:
            html_template = file.read()
            lines = file.readlines()

        for line in lines:
            print(line)

        # Find the CLI command in the HTML template
        cli_command_pattern = re.compile(r'CLI_COMMAND_PLACEHOLDER: (.*?)<', re.DOTALL)

        cli_command_match = cli_command_pattern.search(html_template)

        if cli_command_match:
            cli_command = cli_command_match.group(1).strip()
            print(f"Executing CLI command: {cli_command}")
            lista_commands_cli = cli_command.split()
            flag = 0
            caminho_saida = "sem_caminho"
            nome_arquivo  = "sem_nome"
            contador = 0 
            for comando in lista_commands_cli:
                if(comando == "--outpath"):
                    caminho_saida = lista_commands_cli[contador+1]
                if(comando == "--titulo"):
                    nome_arquivo = lista_commands_cli[contador+1].replace("_"," ")+".html"
                contador += 1

            print(cli_command.split())
            cli_output = subprocess.check_output(cli_command, shell=True).decode("utf-8")
            print(caminho_saida+"/"+nome_arquivo)
            with open(caminho_saida+"/"+nome_arquivo, "r") as file:
                htmt_plotly = file.read()
        else:
            cli_output = "No CLI command found."

        # Replace the placeholders with the Plotly plot and CLI output
        #html_report = html_template.replace("PLOT_PLACEHOLDER", plot_html)
        #html_report = html_report.replace("PLOTLY_PLACEHOLDER", htmt_plotly)

        # Save the final HTML report
        #with open("report.html", "w") as file:
        #    file.write(html_report)

        print("Report saved as report.html")