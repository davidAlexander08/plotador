

from apps.interface.dados_json_caso import Dados_json_caso
from apps.model.argumento import Argumento
from apps.report.info.info import Info
from apps.utils.log import Log
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import os
import json
import subprocess
import re
import base64
import shutil

class Report():
    def __init__(self,outpath, arq_json, txt, titulo, tipo, cronologico, conjunto, html):
        #self.outpath = outpath
        self.json = arq_json
        #print("Arquivo JSON: ", self.json)
        self.txt = txt
        self.titulo = titulo
        path = __file__.split("/")
        path.pop()
        path.pop()
        arquivo_template = ""
        

        if(self.json is not None):
            data = Dados_json_caso(self.json)
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
                print(dados["conjuntos"])
                dados["conjuntos"]["casos"][0]["estudo"] = "_default"
                dados["conjuntos"]["casos"][0]["nome"] = " "
                dados["conjuntos"]["casos"][0]["caminho"] = os.getcwd()
                if os.path.isfile("dger.dat"):
                    dados["conjuntos"]["casos"][0]["modelo"] = "NEWAVE"
                    dados["argumentos"][0]["args"] = ["SUDESTE","NORDESTE","NORTE","SUL"]
                elif os.path.isfile("decomp.tim"):
                    dados["conjuntos"]["casos"][0]["modelo"] = "DECOMP"
                    dados["argumentos"][0]["args"] = ["SE","NE","N","S"]
                elif os.path.isfile("entdados.dat"):
                    dados["conjuntos"]["casos"][0]["modelo"] = "DESSEM"
                    dados["argumentos"][0]["args"] = ["SE","NE","N","S"]
                else: 
                    raise FileNotFoundError(f"NAO SE ENCONTRA NA PASTA DE UM CASO OU ARQUIVO JSON NAO EXISTE.")
            with open("exemplo.json", 'w') as file:
                json.dump(dados, file, indent=4)  # Write the updated dictionary back to the JSON file with indentation for readability
            self.json = "exemplo.json"
            data = Dados_json_caso(self.json)

        arquivo_template = ""
        if(self.txt is None):
            if(conjunto =="False"):
                if(data.conjuntoCasos[0].casos[0].modelo == "NEWAVE"):
                    arquivo_template = "/".join(path)+"/template_simples.txt" 
                elif(data.conjuntoCasos[0].casos[0].modelo == "DESSEM" and cronologico == "True"):
                    arquivo_template = "/".join(path)+"/template_dessem_cronologico.txt" 
                elif(data.conjuntoCasos[0].casos[0].modelo == "DESSEM"):
                    arquivo_template = "/".join(path)+"/template_dessem.txt" 
                elif(data.conjuntoCasos[0].casos[0].modelo == "DECOMP"):
                    arquivo_template = "/".join(path)+"/template_decomp.txt" 
                else:
                    print("Tipo definido errado: Simples ou Completo")
                    exit(1)
            elif(conjunto == "True"):
                if(data.conjuntoCasos[0].casos[0].modelo == "DESSEM"):
                    arquivo_template = "/".join(path)+"/template_dessem_conjuntos.txt" 
                else:
                    print("Tipo definido errado: Simples ou Completo")
                    exit(1)
            else:
                print("Tipo definido errado: Simples ou Completo")
                exit(1)
        else:
            arquivo_template = self.txt
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
                    #print(nome_pagina)
                    html_file.write('<li><a href="#" onclick="showSidebarPage(\''+nome_pagina+'\')">'+nome_pagina+'</a></li>'+"\n")

            html_file.write("</ul>"+"\n")
            html_file.write("</div>"+"\n")
            html_file.write('<div class="content">'+"\n")
            flag_primeira_pagina = True
            flag_primeira_subpagina = True

            Log.log().info("-----------Gerando relatorio----------")
            for line in lines:
                if line.strip():
                    if("###" in line):
                        pass
                    elif("</h" in line):
                        html_file.write(line.strip()+"\n")

                    elif("\info{") in line:
                        Log.log().info("Gerando " + line)
                        nome_argumento_info = line.split("{")[1].split("}")[0]
                        args = nome_argumento_info.split("/")
                        chave = args[0]
                        argumentos = nome_argumento_info.split("/")[1].split(",") if(len(args) > 1) else None
                        par_dados = (chave, argumentos)
                        info = Info(data, par_dados)
                        html_file.write(info.text_html+"\n")

                    elif("\page{") in line:
                        
                        if(flag_primeira_pagina == False):
                            html_file.write('</div>'+"\n")
                        if(flag_primeira_subpagina == False):
                            html_file.write('</div>'+"\n")
                        nome_pagina = line.split("{")[1].split("}")[0]
                        Log.log().info("Gerando pagina "+ nome_pagina)
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
                        Log.log().info("Gerando subpagina "+ nome_sub_pagina)
                        html_file.write('<div id="'+nome_sub_pagina+'" class="page">'+"\n")
                            
                    elif("plotador" in line):
                        cli_command = line.strip() if "--outpath" in line else  line.strip()+" --outpath report"
                        
                        if( (data.conjuntoCasos[0].casos[0].modelo == "DECOMP" or data.conjuntoCasos[0].casos[0].modelo == "DESSEM") and "convergencia" in cli_command):
                            pass
                        else:
                            if("arquivo_json" in cli_command):
                                cli_command = cli_command.replace("arquivo_json", self.json)
                            if("ADD_SBMS" in cli_command):
                                submercados = "SE,S,NE,N" if data.conjuntoCasos[0].casos[0].modelo != "NEWAVE" else "SUDESTE,SUL,NORDESTE,NORTE"
                                cli_command = cli_command.replace("ADD_SBMS", submercados)
                            if(data.conjuntoCasos[0].casos[0].modelo == "NEWAVE" and "--eixox" not in cli_command and "temporal" in cli_command):
                                cli_command = cli_command + " --eixox data_inicio"
                            #if(html == "True" and "html" not in cli_command):
                            if(html == None):
                                cli_command = cli_command + " --html True"
                            if(data.conjuntoCasos[0].casos[0].modelo == "NEWAVE" and "--eixox" not in cli_command and "temporal" in cli_command):
                                cli_command = cli_command + " --eixox data_inicio"
                            try:
                                Log.log().info(cli_command)
                                cli_output = subprocess.check_output(cli_command, shell=True).decode("utf-8")
                                print(f"Command Output: {cli_output}")                            
                            except subprocess.CalledProcessError as e:
                                print(f"Command failed with exit status {e.returncode}")
                                print(f"Error Output: {e.output.decode('utf-8') if e.output else 'No output'}")
                            lista_commands_cli = cli_command.split()
                            #print(lista_commands_cli)
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
                                try:
                                    with open(caminho_saida+"/"+nome_arquivo+extensao, "r") as file:
                                        html_plotly = file.read()
                                        #html_file.write(nome_arquivo+"\n")
                                        html_file.write(html_plotly+"\n")
                                except IOError as e:
                                    # Handle other I/O errors (e.g., permission denied, etc.)
                                    print(f"An I/O error occurred: {e}")
                            else:
                                try:
                                    with open(caminho_saida+"/"+nome_arquivo+extensao, "rb") as image_file:
                                        base64_string = base64.b64encode(image_file.read()).decode('utf-8')
                                        html_file.write('<img src="data:image/png;base64,'+base64_string+'" alt="Centered Image" style="max-width: 100%; height: auto;">'+"\n")
                                                #<img src="data:image/png;base64,INSERT_BASE64_ENCODED_STRING_HERE" alt="Centered Image" style="max-width: 100%; height: auto;">
                                except IOError as e:
                                    # Handle other I/O errors (e.g., permission denied, etc.)
                                    print(f"An I/O error occurred: {e}")
                    else:
                        html_file.write("<p>"+line.strip()+"</p>\n")

            html_file.write('</div>'+"\n")

            with open("/".join(path)+"/report/script.txt", 'r', encoding='utf-8') as arquivo:
                conteudo = arquivo.read()
                html_file.write(conteudo)
        Log.log().info("-----------Fim do Report----------")
        #print("Report saved as report.html")

