

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
        self.create_sphinx_project(
            project_name='MyProject',
            author='Your Name',
            version='0.1',
            release='0.1.0'
        )

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




    def create_sphinx_project(self, project_name, author, version, release, language='en'):
        # Define the project directory
        project_dir = os.path.join(os.getcwd(), project_name)
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
        # Run sphinx-quickstart to initialize the Sphinx project
        subprocess.run([
            'sphinx-quickstart',
            '--no-batchfile',   # Don't create make.bat file for Windows
            '--no-makefile',    # Don't create Makefile for Unix
            '--quiet',
            '--project', project_name,
            '--author', author,
            '--version', version,
            '--release', release,
            '--language', language,
            '--sep', ' ',
            '--no-interactive'
        ], cwd=project_dir)

        # Copy additional files or modify configuration if needed
        modify_conf_file(project_dir)
        add_documentation_content(project_dir)

        # Build the documentation
        build_sphinx_docs(project_dir)

    def modify_conf_file(self, project_dir):
        # Path to the conf.py file
        conf_path = os.path.join(project_dir, 'source', 'conf.py')

        # Read the conf.py file
        with open(conf_path, 'r') as file:
            conf_lines = file.readlines()

        # Modify conf.py settings (example: setting the theme)
        with open(conf_path, 'w') as file:
            for line in conf_lines:
                if line.startswith('html_theme ='):
                    file.write('html_theme = \'alabaster\'\n')
                else:
                    file.write(line)

    def add_documentation_content(self, project_dir):
        # Add content to index.rst
        index_path = os.path.join(project_dir, 'source', 'index.rst')
        with open(index_path, 'w') as file:
            file.write("""\
        Welcome to Your Project’s Documentation!
        =========================================

        Introduction
        ------------

        This is the beginning of your documentation. Replace this text with your actual content.

        Getting Started
        ---------------

        Provide information on getting started with your project.

        Usage
        -----

        Provide usage instructions for your project.
        """)

    def build_sphinx_docs(self, project_dir):
        # Change directory to the Sphinx project directory
        os.chdir(project_dir)

        # Build the documentation
        subprocess.run(['make', 'html'], cwd=os.path.join(project_dir, 'docs'))

