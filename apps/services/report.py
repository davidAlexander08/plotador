

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
        
        if os.path.exists(project_dir):
            print(f"Directory '{project_dir}' already exists. Please remove or choose a different name.")
            return

        os.makedirs(project_dir)

        # Initialize the Sphinx project
        result = subprocess.run([
            'sphinx-quickstart',
            '--quiet',  # Suppress output
            '--project', project_name,
            '--author', author,
            '--version', version,
            '--release', release,
            '--language', language,
            '--makefile',  # Create Makefile
            '--batchfile'  # Create make.bat for Windows
        ], cwd=project_dir, text=True, capture_output=True)

        # Check if sphinx-quickstart was successful
        if result.returncode != 0:
            print(f"Error running sphinx-quickstart: {result.stderr}")
            return

        # Check if the necessary files have been created
        source_dir = os.path.join(project_dir, 'source')
        build_dir = os.path.join(project_dir, 'build')
        
        if not os.path.isdir(source_dir):
            print(f"Source directory '{source_dir}' not found. Sphinx project setup may have failed.")
            return

        if not os.path.isfile(os.path.join(source_dir, 'conf.py')):
            print(f"Configuration file 'conf.py' not found in '{source_dir}'.")
            return

        # Modify conf.py settings
        modify_conf_file(project_dir)

        # Add documentation content
        add_documentation_content(project_dir)

        # Build the documentation
        build_sphinx_docs(project_dir)

    def modify_conf_file(self, project_dir):
        # Path to the conf.py file
        conf_path = os.path.join(project_dir, 'source', 'conf.py')

        # Modify conf.py settings
        with open(conf_path, 'r') as file:
            conf_lines = file.readlines()

        with open(conf_path, 'w') as file:
            for line in conf_lines:
                if line.startswith('html_theme ='):
                    file.write('html_theme = \'alabaster\'\n')
                else:
                    file.write(line)

    def add_documentation_content(self, project_dir):
        # Add content to index.rst
        index_path = os.path.join(project_dir, 'source', 'index.rst')
        if os.path.isfile(index_path):
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
        else:
            print(f"Index file '{index_path}' not found.")

    def build_sphinx_docs(self, project_dir):
        # Check if the build directory exists
        docs_dir = os.path.join(project_dir, 'docs')
        if not os.path.isdir(docs_dir):
            print(f"Docs directory '{docs_dir}' not found.")
            return

        # Build the documentation
        result = subprocess.run(['make', 'html'], cwd=docs_dir, text=True, capture_output=True)
        if result.returncode != 0:
            print(f"Error building documentation: {result.stderr}")
        else:
            print("Documentation built successfully.")

