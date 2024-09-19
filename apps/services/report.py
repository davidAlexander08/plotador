

from apps.interface.dados_json_caso import Dados_json_caso
from apps.indicadores.eco_indicadores import EcoIndicadores
from apps.model.argumento import Argumento
from apps.report.info.info import Info
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
import json

class Report():
    def __init__(self,outpath, arq_json, txt, titulo):
        #self.outpath = outpath
        self.json = arq_json
        self.txt = txt
        self.titulo = titulo
        path = __file__.split("/")
        path.pop()
        path.pop()
        arquivo_template = "/".join(path)+"/template.txt" if self.txt is None else self.txt
        if(self.json is not None):
            data = Dados_json_caso(self.json)
            self.eco_indicadores = EcoIndicadores(data.casos)
        if(self.txt is None and self.json is None):
            flag_diretorio = 0
            path = __file__.split("/")
            path.pop()
            path.pop()
            arq_json_exemplo = "/".join(path)+"/exemplo.json"
            current_directory = os.getcwd()
            #shutil.copy(arq_json_exemplo, current_directory+"/exemplo.json")
            with open(arq_json_exemplo, "r") as file:
                dados = json.load(file)
                dados["casos"][0]["estudo"] = "_default"
                dados["casos"][0]["nome"] = " "
                dados["casos"][0]["caminho"] = os.getcwd()
                if os.path.isfile("dger.dat"):
                    dados["casos"][0]["modelo"] = "NEWAVE"
                    dados["argumentos"][0]["args"] = ["SUDESTE","NORDESTE","NORTE","SUL"]
                elif os.path.isfile("decomp.tim"):
                    dados["casos"][0]["modelo"] = "DECOMP"
                    dados["argumentos"][0]["args"] = ["SE","NE","N","S"]
                elif os.path.isfile("entdados.dat"):
                    dados["casos"][0]["modelo"] = "DESSEM"
                    dados["argumentos"][0]["args"] = ["SE","NE","N","S"]
                else: 
                    raise FileNotFoundError(f"NAO SE ENCONTRA NA PASTA DE UM CASO OU ARQUIVO JSON NAO EXISTE.")
            with open("exemplo.json", 'w') as file:
                json.dump(dados, file, indent=4)  # Write the updated dictionary back to the JSON file with indentation for readability

            self.json = "exemplo.json"
            data = Dados_json_caso(self.json)


            self.eco_indicadores = EcoIndicadores(data.casos)

        with open(arquivo_template, "r") as file:
            lines = file.readlines()

        titulo_html = "output.html" if self.titulo == " " else self.titulo
        with open(titulo_html, "w") as html_file:
            with open("/".join(path)+"/report/head.txt", 'r', encoding='utf-8') as arquivo:
                conteudo = arquivo.read()
                html_file.write(conteudo)
            head_html = """
    <div class="sidebar">
        <div class="company-name">ONS</div>
        <ul>
            """
            html_file.write(head_html)
            for line in lines:
                if("\page{") in line:
                    nome_pagina = line.split("{")[1].split("}")[0]
                    print(nome_pagina)
                    html_file.write('<li><a href="#" onclick="showSidebarPage(\''+nome_pagina+'\')">'+nome_pagina+'</a></li>'+"\n")

            html_file.write("</ul>"+"\n")
            html_file.write("</div>"+"\n")
            html_file.write('<div class="content">'+"\n")
            flag_primeira_pagina = True
            flag_primeira_subpagina = True

            for line in lines:
                if line.strip():
                    if("###" in line):
                        pass
                    elif("</h" in line):
                        html_file.write(line.strip()+"\n")

                    elif("\info{") in line:
                        nome_argumento_info = line.split("{")[1].split("}")[0]
                        args = nome_argumento_info.split("/")
                        chave = args[0]
                        argumentos = nome_argumento_info.split("/")[1].split(",") if(len(args) > 1) else None
                        print(chave)
                        print(argumentos)
                        exit(1)

                        info = Info(html_file, data, nome_argumento_info)
                        html_file.write(info.text_html+"\n")

                    elif("\page{") in line:
                        if(flag_primeira_pagina == False):
                            html_file.write('</div>'+"\n")
                        if(flag_primeira_subpagina == False):
                            html_file.write('</div>'+"\n")
                        nome_pagina = line.split("{")[1].split("}")[0]
                        pagina_ativa = "page active" if flag_primeira_pagina == True else "page"
                        html_file.write('<div id="'+nome_pagina+'" class="'+pagina_ativa+'">'+"\n")
                        flag_primeira_pagina = False
                        flag_primeira_subpagina = True
                            
                    elif("\subpage{") in line:
                        if(flag_primeira_subpagina == False):
                            html_file.write('</div>'+"\n")

                        if(flag_primeira_subpagina == True):
                            html_file.write('</div>'+"\n")
                            html_file.write('<div id="'+nome_pagina+'-subpages'+'" class="top-bar-menu">'+"\n")
                        
                        flag_primeira_subpagina = False
                        nome_sub_pagina = line.split("{")[1].split("}")[0]
                        html_file.write('<div id="'+nome_sub_pagina+'" class="page">'+"\n")
                            
                    elif("plotador" in line):
                        cli_command = line.strip() if "--outpath" in line else  line.strip()+" --outpath report"
                        print(f"Executing CLI command: {cli_command}")
                        if( (data.casos[0].modelo == "DECOMP" or data.casos[0].modelo == "DESSEM") and "convergencia" in cli_command):
                            pass
                        else:
                            if("arquivo_json" in cli_command):
                                cli_command = cli_command.replace("arquivo_json", self.json)
                            if("ADD_SBMS" in cli_command):
                                submercados = "SE,S,NE,N" if data.casos[0].modelo != "NEWAVE" else "SUDESTE,SUL,NORDESTE,NORTE"
                                cli_command = cli_command.replace("ADD_SBMS", submercados)
                            if(data.casos[0].modelo == "NEWAVE" and "--eixox" not in cli_command and "temporal" in cli_command):
                                cli_command = cli_command + " --eixox dataInicio"
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
                                    #html_file.write(nome_arquivo+"\n")
                                    html_file.write(html_plotly+"\n")
                            else:
                                with open(caminho_saida+"/"+nome_arquivo+extensao, "rb") as image_file:
                                    base64_string = base64.b64encode(image_file.read()).decode('utf-8')
                                    html_file.write('<img src="data:image/png;base64,'+base64_string+'" alt="Centered Image" style="max-width: 100%; height: auto;">'+"\n")
                                                #<img src="data:image/png;base64,INSERT_BASE64_ENCODED_STRING_HERE" alt="Centered Image" style="max-width: 100%; height: auto;">
                    else:
                        html_file.write("<p>"+line.strip()+"</p>\n")

            html_file.write('</div>'+"\n")

            with open("/".join(path)+"/report/script.txt", 'r', encoding='utf-8') as arquivo:
                conteudo = arquivo.read()
                html_file.write(conteudo)

        print("Report saved as report.html")

