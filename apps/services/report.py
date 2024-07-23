

from apps.interface.dados_json_caso import Dados_json_caso
from apps.indicadores.eco_indicadores import EcoIndicadores

from inewave.newave import Pmo
from idecomp.decomp import Relato
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import os
import json
import subprocess
import re
import base64
import os
import subprocess
import shutil

class Report:
    def __init__(self,outpath, json, txt, titulo):
        
        #self.outpath = outpath
        self.json = json
        self.txt = txt
        self.titulo = titulo
        path = __file__.split("/")
        path.pop()
        path.pop()
        arquivo_template = "/".join(path)+"/template.txt" if self.txt is None else self.txt
        if(self.json is not None):
            data = Dados_json_caso(self.json)
            self.eco_indicadores = EcoIndicadores(data.casos)

        # Example usage
        with open(arquivo_template, "r") as file:
            #html_template = file.read()
            lines = file.readlines()

        titulo_html = "output.html" if self.titulo == " " else self.titulo
        with open(titulo_html, "w") as html_file:
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
        table {
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
        }

        td, th {
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
        }

        tr:nth-child(even) {
        background-color: #dddddd;
        }


        .centered-image {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 50vh; /* 50% of the viewport height */
            margin-top: 20px;
        }

        .centered-image img {
            max-width: 100%;
            height: auto;
        }

        @media (max-width: 768px) {
            .sidebar {
                width: 200px;
            }

            .content {
                margin-left: 210px;
            }
        }

        @media (max-width: 480px) {
            .sidebar {
                width: 100%;
                height: auto;
                position: relative;
            }

            .content {
                margin-left: 0;
            }

            .centered-image {
                height: auto;
            }
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

            html_file.write("</ul>"+"\n")
            html_file.write("</div>"+"\n")
            html_file.write('<div class="content">'+"\n")
            flag = 0
            for line in lines:
                if line.strip():

                    if("###" in line):
                        pass
                    elif("</h" in line):
                        html_file.write(line.strip()+"\n")
                    elif("\page{") in line:
                        nome_pagina = line.split("{")[1].split("}")[0]
                        if(flag == 1):
                            html_file.write('</div>'+"\n")
                        pagina_ativa = "page active" if flag == 0 else "page"
                        if(nome_pagina == "Infos" or nome_pagina == "Info"):
                            flag = 1
                            html_file.write('<div id="'+nome_pagina+'" class="'+pagina_ativa+'">'+"\n")
                            Inicio_tabela = """
    <table>
    <tr>
        <th>Nome do Caso</th>
        <th>Caminho</th>
        <th>Modelo</th>
        <th>Cor</th>
    </tr>
"""                         
                            Template_tabela_caso = """
    <tr>
        <td>nome</td>
        <td>caminho</td>
        <td>modelo</td>
        <td>cor</td>
    </tr>
"""
                            html_file.write(Inicio_tabela)
                            html_file.write("<h1>Informações Gerais do Estudo</h1>"+"\n")
                            for caso in data.casos:
                                temp = Template_tabela_caso
                                temp = temp.replace("nome", caso.nome)
                                temp = temp.replace("caminho", caso.caminho)
                                temp = temp.replace("modelo", caso.modelo)
                                temp = temp.replace("cor", caso.cor)
                                html_file.write(temp)
                            html_file.write("</table>"+"\n")

### TABELA DE INFORMACOES OPERACIONAIS

                            Inicio_tabela = """
    <table>
    <tr>
        <th>Caso</th>
        <th>Modelo</th>
        <th>Versao</th>
        <th>Tempo Total (min)</th>
        <th>Iter</th>
        <th>Zinf</th>
        <th>Custo Total</th>
    </tr>
"""                         
                            Template_tabela_caso = """
  <tr>
    <td>nome</td>
	<td>modelo</td>
    <td>versao</td>
	<td>tempo_total</td>
    <td>iteracoes</td>
    <td>zinf</td>
    <td>custo_total</td>
  </tr>
"""
                            html_file.write(Inicio_tabela)
                            html_file.write("<h2>Informações Operacionais</h2>"+"\n")
                            df_temp = self.eco_indicadores.retorna_df_concatenado("TEMPO")
                            for caso in data.casos:
                                temp = Template_tabela_caso
                                temp = temp.replace("nome", caso.nome)
                                temp = temp.replace("modelo", caso.modelo)
                                tempo_total = 0
                                iteracoes= 0 
                                zinf = 0
                                custo_total=0
                                if(caso.modelo == "NEWAVE"):
                                    data_pmo = Pmo.read(caso.caminho+"/pmo.dat")
                                    df_caso = df_temp.loc[(df_temp["caso"] == caso.nome)]
                                    tempo_total = df_caso.loc[(df_caso["etapa"] == "Tempo Total")]["tempo"].iloc[0]/60
                                    iteracoes = data_pmo.convergencia["iteracao"].iloc[-1]
                                    zinf = data_pmo.convergencia["zinf"].iloc[-1]
                                    custo_total = data_pmo.custo_operacao_total
                                    versao = data_pmo.versao_modelo
                                if(caso.modelo == "DECOMP"):
                                    extensao = ""
                                    with open(caso.caminho+"/caso.dat") as f:
                                        extensao = f.readline().strip('\n')
                                    if extensao == "":
                                        raise FileNotFoundError(f"Arquivo caso.dat não encontrado.") 
                                    data_relato = Relato.read(caso.caminho+"/relato."+extensao).convergencia
                                    df_caso = df_temp.loc[(df_temp["caso"] == caso.nome)]
                                    #print(data_relato)
                                    #print(df_caso)
                                    tempo_total = df_caso.loc[(df_caso["etapa"] == "Tempo Total")]["tempo"].iloc[0]/60
                                    iteracoes = data_relato["iteracao"].iloc[-1]
                                    zinf = data_relato["zinf"].iloc[-1]
                                    custo_total = "X"
                                    versao = "X"
                                temp = temp.replace("versao", versao)
                                temp = temp.replace("tempo_total", str(tempo_total))
                                temp = temp.replace("iteracoes", str(iteracoes))
                                temp = temp.replace("zinf", str(zinf))
                                temp = temp.replace("custo_total", str(custo_total))
                                html_file.write(temp)
                            html_file.write("</table>"+"\n")


                        else:
                            flag = 1
                            html_file.write('<div id="'+nome_pagina+'" class="'+pagina_ativa+'">'+"\n")
                            print(nome_pagina)
                    elif("plotador" in line):
                        cli_command = line.strip() if "--outpath" in line else  line.strip()+" --outpath report"
                        print(f"Executing CLI command: {cli_command}")
                        if("arquivo_json" in cli_command):
                            cli_command = cli_command.replace("arquivo_json", self.json)
                        if("ADD_SBMS" in cli_command):
                            submercados = "SE,S,NE,N" if data.casos[0].modelo != "NEWAVE" else "SUDESTE,SUL,NORDESTE,NORTE"
                            cli_command = cli_command.replace("ADD_SBMS", submercados)
                        if(data.casos[0].modelo == "DECOMP" and "convergencia" in cli_command):
                            cli_command = " "
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
                        if(extensao == ".html"):
                            with open(caminho_saida+"/"+nome_arquivo+extensao, "r") as file:
                                html_plotly = file.read()
                                html_file.write(html_plotly+"\n")
                                #html_file.write(nome_arquivo+"\n")
                        else:
                            with open(caminho_saida+"/"+nome_arquivo+extensao, "rb") as image_file:
                                base64_string = base64.b64encode(image_file.read()).decode('utf-8')
                                html_file.write('<img src="data:image/png;base64,'+base64_string+'" alt="Centered Image" style="max-width: 100%; height: auto;">'+"\n")
                                            #<img src="data:image/png;base64,INSERT_BASE64_ENCODED_STRING_HERE" alt="Centered Image" style="max-width: 100%; height: auto;">

                    else:
                        html_file.write("<p>"+line.strip()+"</p>\n")
                    #print(line)

            html_file.write('</div>'+"\n")

            script_html = """
    <script>
        function showPage(pageId) {
            // Hide all pages
            var pages = document.querySelectorAll('.page');
            pages.forEach(function(page) {
                page.classList.remove('active');
            });

            // Show the selected page
            var selectedPage = document.getElementById(pageId);
            selectedPage.classList.add('active');
        }
    </script>
            """
            html_file.write(script_html)
            html_file.write('</body>\n')
            html_file.write('</html>\n')


        print("Report saved as report.html")



