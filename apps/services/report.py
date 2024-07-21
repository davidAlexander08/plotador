

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


        with open("template.txt", "r") as file:
            #html_template = file.read()
            lines = file.readlines()

        with open("output.html", "w") as html_file:
            html_file.write('<!DOCTYPE html>\n')
            html_file.write('<html lang="en">\n')
            html_file.write('<head>\n')
            html_file.write('<meta charset="UTF-8">\n')
            html_file.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
            html_file.write('<title>Generated HTML</title>\n')
            html_file.write('<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>\n')
            html_file.write('<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>\n')
            #html_file.write("<style>")
            #html_file.write("iframe {width: 100%; height: 600px; border: none;")
            #html_file.write("}")
            #html_file.write("<\style>")
            html_file.write('</head>\n')
            html_file.write('<body>\n')
            #html_file.write('<iframe src="docs/_build/html/index.html"></iframe>\n')
            for line in lines:
                if line.strip():
                    if("</h" in line):
                        html_file.write(line.strip()+"\n")
                    elif("plotador" in line):
                        cli_command = line.strip() if "--outpath" in line else  line.strip()+" --outpath report"
                        print(f"Executing CLI command: {cli_command}")
                        cli_output = subprocess.check_output(cli_command, shell=True).decode("utf-8")
                        lista_commands_cli = cli_command.split()
                        print(lista_commands_cli)
                        caminho_saida = "report"
                        nome_arquivo  = "sem_nome"
                        extensao = ".png"
                        contador = 0 
                        for comando in lista_commands_cli:
                            if(comando == "--outpath"):
                                caminho_saida = lista_commands_cli[contador+1]
                            if(comando == "--titulo"):
                                nome_arquivo = lista_commands_cli[contador+1].replace("_"," ")
                            if(comando == "--html"):
                                extensao = ".html"
                            contador += 1
                        with open(caminho_saida+"/"+nome_arquivo+extensao, "r") as file:
                            html_plotly = file.read()
                            #html_file.write(html_plotly+"\n")
                            html_file.write(nome_arquivo+"\n")
                    else:
                        html_file.write("<p>"+line.strip()+"</p>\n")
                    print(line)
            html_file.write('</body>\n')
            html_file.write('</html>\n')


        print("Report saved as report.html")