

from apps.interface.dados_json_caso import Dados_json_caso
from apps.report.estruturas import Estruturas
from apps.indicadores.eco_indicadores import EcoIndicadores
from apps.model.argumento import Argumento
from inewave.newave import Pmo
from idecomp.decomp import Relato
from idessem.dessem.des_log_relato import DesLogRelato
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

class Report(Estruturas):
    def __init__(self,outpath, arq_json, txt, titulo):
        Estruturas.__init__(self)
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
            #print(current_directory)
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
                print(conteudo)
                html_file.write(conteudo)
            head_html = """
<body>
    <div id="loader">
        <span>Carregando Visualização - ONS a energia que potencializa a vida - Gerência PEM</span>
    </div>

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
                            html_file.write('<button id="downloadAll">Baixar Gráficos</button>')
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
                            html_file.write("<h2>Informações Gerais do Estudo</h2>"+"\n")
                            for caso in data.casos:
                                temp = Template_tabela_caso
                                temp = temp.replace("nome", caso.nome)
                                temp = temp.replace("caminho", caso.caminho)
                                temp = temp.replace("modelo", caso.modelo)
                                temp = temp.replace("cor", caso.cor)
                                html_file.write(temp)
                            html_file.write("</table>"+"\n")
                            
                            html_file.write("<h2>Informações Operacionais</h2>"+"\n")
                            
                            flag_nw = flag_deco = flag_dss = True
                            for caso in data.casos:
                                if(caso.modelo == "NEWAVE"):
                                    if(flag_nw == True):
                                        html_file.write(self.mapa_tabela_modelo[caso.modelo])
                                        flag_nw = False
                                    temp = self.preenche_modelo_tabela_modelo_NEWAVE(caso)
                                if(caso.modelo == "DECOMP"):
                                    if(flag_deco == True):
                                        html_file.write(self.mapa_tabela_modelo[caso.modelo])
                                        flag_deco = False
                                    temp = self.preenche_modelo_tabela_modelo_DECOMP(caso)
                                if(caso.modelo == "DESSEM"):
                                    if(flag_dss == True):
                                        html_file.write(self.mapa_tabela_modelo[caso.modelo])
                                        flag_dss = False
                                    temp = self.preenche_modelo_tabela_modelo_DESSEM(caso)
                                html_file.write(temp)
                            html_file.write("</table>"+"\n")


                        else:
                            flag = 1
                            html_file.write('<div id="'+nome_pagina+'" class="'+pagina_ativa+'">'+"\n")
                            print(nome_pagina)
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

    

    <script>
    document.getElementById('downloadAll').addEventListener('click', function() {
        // Get all Plotly graph divs (assuming each graph is in a div with class "plotly-graph-div")
        const graphs = document.querySelectorAll('.js-plotly-plot');

        // Iterate through each graph and download it as a PNG
        graphs.forEach((graph, index) => {
            Plotly.downloadImage(graph, {
                format: 'png', // Choose the format: 'png', 'jpeg', 'webp', etc.
                filename: `graph_${index + 1}`, // Filename for each graph
                width: 1200, // Width of the image
                height: 600 // Height of the image
            });
        });
    });
    </script>

    <script>
    window.addEventListener('load', function() {
        // Remove o loader após o carregamento da página
        const loader = document.getElementById('loader');
        if (loader) {
            loader.style.display = 'none';
        }
    });
    </script>

            """
            html_file.write(script_html)
            html_file.write('</body>\n')
            html_file.write('</html>\n')


        print("Report saved as report.html")











    def preenche_modelo_tabela_modelo_NEWAVE(self,caso):

        df_temp = self.eco_indicadores.retorna_df_concatenado("TEMPO")

        tempo_total = iteracoes = zinf = custo_total = desvio_custo = 0
        versao = "0"

        temp = self.mapa_template_tabela_modelo[caso.modelo]
        temp = temp.replace("nome", caso.nome)
        temp = temp.replace("modelo", caso.modelo)

        data_pmo = Pmo.read(caso.caminho+"/pmo.dat")
        df_caso = df_temp.loc[(df_temp["caso"] == caso.nome)]
        tempo_total = df_caso.loc[(df_caso["etapa"] == "Tempo Total")]["tempo"].iloc[0]/60
        iteracoes = data_pmo.convergencia["iteracao"].iloc[-1]
        zinf = data_pmo.convergencia["zinf"].iloc[-1]
        custo_total = data_pmo.custo_operacao_total
        desvio_custo = data_pmo.desvio_custo_operacao_total*1.96
        versao = data_pmo.versao_modelo

        temp = temp.replace("versao", versao)
        temp = temp.replace("tempo_total", str(tempo_total))
        temp = temp.replace("iteracoes", str(iteracoes))
        temp = temp.replace("zinf", str(zinf))
        temp = temp.replace("custo_total", str(custo_total))
        temp = temp.replace("desvio_custo", str(desvio_custo))

        return temp


    def preenche_modelo_tabela_modelo_DECOMP(self, caso):

        df_temp = self.eco_indicadores.retorna_df_concatenado("TEMPO")

        tempo_total = iteracoes = zinf = custo_total = desvio_custo = 0
        versao = "0"

        temp = self.mapa_template_tabela_modelo[caso.modelo]
        temp = temp.replace("nome", caso.nome)
        temp = temp.replace("modelo", caso.modelo)
        extensao = ""
        with open(caso.caminho+"/caso.dat") as f:
            extensao = f.readline().strip('\n')
        if extensao == "":
            raise FileNotFoundError(f"Arquivo caso.dat não encontrado.") 
        data_relato = Relato.read(caso.caminho+"/relato."+extensao).convergencia
        df_caso = df_temp.loc[(df_temp["caso"] == caso.nome)]
        tempo_total = df_caso.loc[(df_caso["etapa"] == "Tempo Total")]["tempo"].iloc[0]/60
        iteracoes = data_relato["iteracao"].iloc[-1]
        zinf = data_relato["zinf"].iloc[-1]
        custo_total = " "
        versao = " "
        temp = temp.replace("versao", versao)
        temp = temp.replace("tempo_total", str(tempo_total))
        temp = temp.replace("iteracoes", str(iteracoes))
        temp = temp.replace("zinf", str(zinf))
        temp = temp.replace("custo_total", str(custo_total))
        return temp

    def preenche_modelo_tabela_modelo_DESSEM(self, caso):
        df_temp = self.eco_indicadores.retorna_df_concatenado("TEMPO")
        ## FALTA COMPLEMENTAR, ESTA INCOMPLETO
        data_relato = DesLogRelato.read(caso.caminho+"/DES_LOG_RELATO.DAT")
        df_caso = df_temp.loc[(df_temp["caso"] == caso.nome)]
        tempo_total = df_caso["tempo"].sum()/60
        iteracoes = " "
        zinf = " "
        custo_total = " "
        desvio_custo = " "
        versao = data_relato.versao
        return temp