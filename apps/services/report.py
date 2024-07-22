

import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import os
import json
import subprocess
import re

import os
import subprocess
import shutil

class Report:
    def __init__(self):
        # Example usage
        with open("template.txt", "r") as file:
            #html_template = file.read()
            lines = file.readlines()

        with open("output.html", "w") as html_file:
            head_html = """
<!DOCTYPE html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Relatorio ONS</title>
<style>

        body {
            margin: 0;
            font-family: Arial, sans-serif;
        }

        .sidebar {
            height: 100%;
            width: 250px;
            position: fixed;
            top: 0;
            left: 0;
            background-color: #333;
            padding-top: 20px;
            color: white;
            box-shadow: 2px 0 5px rgba(0,0,0,0.3);
        }
        
        .company-name {
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            padding: 20px 0;
            border-bottom: 1px solid #575757;
        }

        .sidebar ul {
            list-style-type: none; /* Removes default bullets */
            padding: 0;
            margin: 20px 0 0; /* Adjusts menu position */
        }

        .sidebar li {
            margin: 0;
        }

        .sidebar a {
            padding: 15px 20px;
            text-decoration: none;
            font-size: 18px;
            color: white;
            display: block;
            border-left: 4px solid transparent; /* Space for hover effect */
        }

        .sidebar a:hover {
            background-color: #575757;
            border-left: 4px solid #ffcc00; /* Highlight color on hover */
        }

        .content {
            margin-left: 260px;
            padding: 20px;
        }


        .page {
            display: none;
        }

        .page.active {
            display: block;
        }

        h1 {
            color: #333;
        }

</style>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
    <div class="sidebar">
        <div class="company-name">ONS</div>
        <ul>
            """
            html_file.write(head_html)
            for line in lines:
                if("\page{") in line:
                    nome_pagina = line.split("{")[1].split("}")[0]
                    print(nome_pagina)
                    html_file.write('<li><a href="#" onclick="showPage(\''+nome_pagina+'\')">'+nome_pagina+'</a></li>'+"\n")



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
                            #tml_file.write(html_plotly+"\n")
                            html_file.write(nome_arquivo+"\n")
                    else:
                        html_file.write("<p>"+line.strip()+"</p>\n")
                    print(line)
            html_file.write('</body>\n')
            html_file.write('</html>\n')


        print("Report saved as report.html")



