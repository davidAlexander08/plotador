import pandas as pd
from typing import Dict
from apps.model.unidade import UnidadeSintese
from apps.model.conjuntoUnidade import ConjuntoUnidadeSintese
from apps.graficos.graficos import Graficos
from apps.indicadores.indicadores_temporais import IndicadoresTemporais
from apps.model.caso import Caso
from apps.model.sintese import Sintese
from apps.model.argumento import Argumento
from apps.model.unidadeArgumental import UnidadeArgumental
from apps.graficos.figura import Figura
from apps.model.caso import Caso
from inewave.newave import Dger
import os 
import json
from typing import List
from os.path import join
from apps.utils.log import Log
import warnings
import re
import pyarrow.parquet as pq

class Temporal:


    def __init__(self, data, xinf, xsup,estagio, cenario, sintese, largura, altura, eixox, cronologico, labely, booltitulo, titulo, showlegend, labelx, argumentos, tamanho, boxplot,csv, html, outpath, ysup, yinf, y2, y2sup, y2inf, patamar, liminf, limsup, posnw):
        self.xinf  = xinf
        self.xsup = xsup
        self.ysup = ysup
        self.yinf = yinf
        self.y2sup = y2sup
        self.y2inf = y2inf
        self.liminf = liminf
        self.limsup = limsup
        self.eixox = eixox
        self.patamar = int(patamar)
        self.estagio = estagio
        self.data = data
        self.y2 = y2
        self.posnw = posnw
        if(self.y2 == "True" and len(data.conjuntoCasos[0].casos) > 2):
            print("ERRO: Opcao y2 valida apenas para comparacao de duplas de casos")
            exit(1)
        self.cenario = [cenario] if cenario == "mean" else cenario.split(",")
        if(len(self.cenario) > 1):
            marcadores= [None,"circle","square", "diamond","x","cross"]
            dashes = ["dash", "dot"]
            novos_casos = [] 
            for caso in data.conjuntoCasos[0].casos:
                contador = 0
                contador_marcadores = 0
                for cen in self.cenario:
                    if(cen != "mean"):
                        marcador = marcadores[contador_marcadores]
                        dash = dashes[contador]

                        #rgba = rgba_str.lstrip('rgba(').rstrip(')').split(',')
                        #r, g, b, a = [float(x) for x in rgba]
                        #r = min(255, r * factor)
                        #g = min(255, g * factor)
                        #b = min(255, b * factor)
                        #brightened_rgba = f'rgba({int(r)}, {int(g)}, {int(b)}, {a})'

                        novos_casos.append(Caso(caso.nome+"_"+cen, caso.caminho, caso.cor, marcador, caso.modelo, dash, cen, self.patamar ))
                        contador += 1
                    if(contador >= len(dashes)):
                        contador = 0
                        contador_marcadores += 1
            data.conjuntoCasos[0].casos = data.conjuntoCasos[0].casos+novos_casos
        else:
            for caso in data.conjuntoCasos[0].casos:
                caso.tipo = self.cenario[0]
                caso.dash = None
                caso.marcador = None
                caso.patamar = self.patamar 

        
        
        self.sintese = sintese
        self.argumentos  = argumentos
        self.largura = largura
        self.altura = altura
        self.cronologico = cronologico
        self.labely = labely
        self.labelx = labelx
        self.booltitulo = booltitulo
        self.titulo = titulo
        self.showlegend = showlegend
        self.estudo = data.estudo
        self.boxplot = boxplot
        self.csv = csv
        self.html = html
        self.tamanho_texto = data.tamanho_texto if tamanho is None else int(tamanho)
        self.indicadores_temporais = IndicadoresTemporais(data.conjuntoCasos[0].casos)
        self.graficos = Graficos(data)

        diretorio_saida = f"resultados/{self.estudo}/temporal" if outpath is None else outpath
        os.makedirs(diretorio_saida, exist_ok=True)

        arq_meta_dados = join( data.conjuntoCasos[0].casos[0].caminho, "sintese", "METADADOS_OPERACAO"+".parquet"  )
        try:
            meta_dados = pd.read_parquet(arq_meta_dados, engine = "pyarrow")
        except:
            raise FileNotFoundError(f"Arquivo {arq_sintese} não encontrado. Caminho pode estar errado.")


        df_chave = meta_dados.loc[(meta_dados["chave"] == self.sintese)] if "ESTATISTICA" not in self.sintese else meta_dados.loc[(meta_dados["chave"] == self.sintese.espacial)] 
        titulo_meta = df_chave["nome_longo_variavel"]
        if(self.labely is None):
            self.labely = df_chave["unidade"].iloc[0]
        print(df_chave)
        self.sintese_espacial = self.sintese.split("_")[1]
            
        if(self.argumentos is not None):
            lista_argumentos = self.argumentos.split(",")
            list_arg = []
            for arg in lista_argumentos:
                list_arg.append(arg.replace("_"," "))
            lista_argumentos = list_arg
            data.args = [Argumento(lista_argumentos, self.sintese_espacial, "out")] 
            if(len(lista_argumentos) == 1 and self.titulo == " "): 
                self.titulo = lista_argumentos[0]

        self.sts = Sintese(self.sintese)
        self.mapa_argumentos = {}
        if self.sts.espacial != "SIN":
            for caso in data.conjuntoCasos[0].casos:
                arq_espacial = join( caso.caminho, "sintese", sintese_espacial+".parquet"  )
                try:
                    df = pd.read_parquet(arq_espacial, engine = "pyarrow")
                except:
                    raise FileNotFoundError(f"Arquivo {arq_sintese} não encontrado. Caminho pode estar errado.")
                df["caso"] = caso.nome
                df["modelo"] = caso.modelo
                self.mapa_argumentos[c] = df
            #self.mapa_argumentos = self.retornaMapaDF(self.sintese_espacial, self.data.conjuntoCasos[0].casos)



        if(self.argumentos is None):
            arg = Argumento(None, None, "SIN")
            conj = ConjuntoUnidadeSintese(self.sts, arg , "estagios", data.limites, self.tamanho_texto)
            if(self.labely is not None):
                conj.legendaEixoY = self.labely
            if(self.labelx is not None):
                conj.legendaEixoX = self.labelx
            diretorio_saida_arg = diretorio_saida+"/"+arg.nome if outpath is None else outpath
            os.makedirs(diretorio_saida_arg, exist_ok=True)
            self.executa(conj,diretorio_saida_arg )
        else:
            for arg in data.args:
                conj = ConjuntoUnidadeSintese(self.sts, arg, "estagios", data.limites, self.tamanho_texto)
                if(self.labely is not None):
                    conj.legendaEixoY = self.labely
                if(self.labelx is not None):
                    conj.legendaEixoX = self.labelx
                diretorio_saida_arg = diretorio_saida+"/"+arg.nome if outpath is None else outpath
                os.makedirs(diretorio_saida_arg, exist_ok=True)
                self.executa(conj,diretorio_saida_arg )
                        

 
    def executa(self, conjUnity, diretorio_saida_arg): 
        mapa_temporal = {} 
        #mapa_eco = self.eco_indicadores.retornaMapaDF(self.sts.sintese, conjUnity, self.boxplot)
        mapa_eco = self.retornaMapaDF(self.sts.sintese, self.data.conjuntoCasos[0].casos , self.boxplot)
        for unity in conjUnity.listaUnidades:
            df_temporal = pd.concat(self.retorna_mapaDF_cenario_medio_temporal(mapa_eco, unity, self.boxplot))
            #print(self.data.conjuntoCasos[0].casos)
            lista_temporal_temp = []
            for caso in self.data.conjuntoCasos[0].casos:
                #print(caso.nome, " caminho: ", caso.caminho+"/dger.dat")
                df_caso = df_temporal.loc[(df_temporal["caso"] == caso.nome)]
                #print(df_caso)
                if(caso.modelo == "NEWAVE" and self.posnw == "False"):
                    dados_dger = Dger.read(caso.caminho+"/dger.dat")
                    anos_estudo = dados_dger.num_anos_estudo
                    mes_inicial = dados_dger.mes_inicio_estudo
                    periodos_estudo = anos_estudo*12 - mes_inicial + 1
                    #print("n_anos_estudo: ", anos_estudo)
                    #print("mes_inicio_estudo: ", mes_inicial)
                    #print("numero_periodos: ", periodos_estudo)
                    df_caso = df_caso.loc[(df_caso["estagio"] <= periodos_estudo)]
                lista_temporal_temp.append(df_caso)
                #print(df_caso)
            df_temporal = pd.concat(lista_temporal_temp)
            if(self.xsup < df_temporal["estagio"].max()):
                df_temporal = df_temporal.loc[(df_temporal["estagio"] <= self.xsup)]
            if(self.xinf > df_temporal["estagio"].min()):
                df_temporal = df_temporal.loc[(df_temporal["estagio"] >= self.xinf)]


            mapa_temporal[unity] = df_temporal
            if(self.csv == "True"): self.indicadores_temporais.exportar(mapa_temporal[unity], diretorio_saida_arg,  "Temporal "+conjUnity.titulo+unity.titulo+self.estudo)
        if(self.boxplot == "True"):
            mapaGO = self.graficos.gera_grafico_boxplot(mapa_temporal, colx = self.eixox)
            titulo_padrao = "Boxplot Temporal "+conjUnity.titulo+self.estudo
        else:
            mapaGO = self.graficos.gera_grafico_linha(mapa_temporal, colx = self.eixox, cronologico = self.cronologico, eixo_y2 = self.y2, liminf = self.liminf, limsup = self.limsup)
            titulo_padrao = "Temporal "+conjUnity.titulo+self.estudo

        tituloFigura = titulo_padrao if self.booltitulo == "True" else " "
        tituloFigura = titulo_padrao if self.titulo == " " else self.titulo.replace("_", " ")

        figura = Figura(conjUnity, mapaGO, tituloFigura, self.yinf, self.ysup, self.y2, self.y2sup, self.y2inf)
        if(self.showlegend == "False"):
            figura.fig.update_layout(showlegend= False)
        self.graficos.exportar(figura.fig, diretorio_saida_arg, tituloFigura, self.html, self.largura, self.altura)
        
        if(self.estagio != ""):
            mapaEst = {self.estagio:" Estagio "+str(self.estagio)} 
            
            for est in mapaEst:
                mapa_estagio = {}
                for unity in conjUnity.listaUnidades:
                    mapa_estagio[unity] = mapa_temporal[unity].loc[mapa_temporal[unity]["estagio"] == int(est)]
                    if(self.csv == "True"): self.indicadores_temporais.exportar(mapa_estagio[unity], diretorio_saida_arg,  mapaEst[est]+"_"+unity.titulo+"_"+conjUnity.sintese.sintese+" "+self.estudo)
                        
                mapaGO = self.graficos.gera_grafico_barra(conjUnity, mapa_estagio, mapaEst[est]+conjUnity.titulo+" "+self.estudo)
                figura = Figura(conjUnity, mapaGO, mapaEst[est]+conjUnity.sintese.sintese+" "+self.estudo, self.yinf, self.ysup, self.y2, self.y2sup, self.y2inf)
                self.graficos.exportar(figura.fig, diretorio_saida_arg, figura.titulo, self.html, self.largura, self.altura) 

        #print("FECHOU EXECUTA")
    
    def __retorna_mapa_media_parquet(self, mapa):
        dict = {}
        for c in self.data.conjuntoCasos[0].casos:
            df = mapa[c]
            if(c.modelo == "NEWAVE" or c.modelo == "DECOMP"):
                dict[c] = df.loc[(df["cenario"] == c.tipo) & (df["patamar"] == c.patamar)].reset_index(drop = True)
            if(c.modelo == "DESSEM"):   
                dict[c] = df.reset_index(drop = True) 
        return dict

    def __retorna_mapa_patamar(self, mapa):
        dict = {}
        for c in self.data.conjuntoCasos[0].casos:
            df = mapa[c]
            if(c.modelo == "NEWAVE" or c.modelo == "DECOMP"):
                dict[c] = df.loc[(df["patamar"] == c.patamar)].reset_index(drop = True)
            if(c.modelo == "DESSEM"):   
                dict[c] = df.reset_index(drop = True) 
        return dict

    def retorna_mapaDF_cenario_medio_temporal(self, eco_mapa, unidade, boxplot):
        mapa_temporal = {}
        if( (unidade.sintese.filtro is None) & (unidade.filtroArgumento is None) ):
            if(boxplot =="True"):
                return self.__retorna_mapa_patamar(eco_mapa)
            else:
                return self.__retorna_mapa_media_parquet(eco_mapa)
        else: 
            #mapa_argumentos = self.eco_indicadores.retornaMapaDF(unidade.sintese.espacial)   
            coluna_filtro = unidade.sintese.filtro.split("_")[1]
            dicionario = {}
            for c in self.data.conjuntoCasos[0].casos:
                df = self.mapa_argumentos[c]
                try:
                    cod_arg = df.loc[(df[coluna_filtro] == unidade.filtroArgumento)][unidade.sintese.filtro].iloc[0]
                except:
                    print("Filtro: ", coluna_filtro)
                    print("Não encontrado: ", unidade.filtroArgumento)
                #print(c.caminho)
                #print(eco_mapa)
                #print(cod_arg)
                #print(unidade.sintese.filtro)
                dicionario[c] = eco_mapa[c].loc[eco_mapa[c][unidade.sintese.filtro] == cod_arg]                
            if(boxplot =="True"):
                mapa_temporal = self.__retorna_mapa_patamar(dicionario)
            else:
                mapa_temporal = self.__retorna_mapa_media_parquet(dicionario)
        return mapa_temporal

    #def retornaMapaDF(self, sintese, conjUnity, boxplot= "False"):
    def retornaMapaDF(self, sintese, casos, boxplot= "False"):
        result_dict  = {}
        sintese_parts = sintese.split("_")
        variavel = sintese_parts[0]
        flag_estatistica = 0
        for c in casos:
            if(os.path.isfile(c.caminho+"/sintese/"+sintese+".parquet")):
                if len(sintese_parts) > 1 and variavel not in ("ESTATISTICAS", "METADADOS") :
                    if(self.checkIfNumberOnly(c.tipo)):
                        c.tipo = int(c.tipo)
                        sintese_busca = sintese
                    else:
                        sintese_busca = "ESTATISTICAS_OPERACAO_"+sintese.split("_")[1]
                        flag_estatistica = 1
                else:
                    sintese_busca = sintese
                if(boxplot == "True"):
                    sintese_busca = sintese
                    flag_estatistica = 0
                arq_sintese = join( c.caminho, "sintese", sintese_busca+".parquet"  )
                try:
                    df = pd.read_parquet(arq_sintese, engine = "pyarrow")
                except:
                    raise FileNotFoundError(f"Arquivo {arq_sintese} não encontrado. Caminho pode estar errado.")



                if(flag_estatistica):
                    df = df.loc[(df["variavel"] == variavel)]                   
                df["caso"] = c.nome
                df["modelo"] = c.modelo
                result_dict [c] = df
            else:                    
                if(sintese in self.mapa_arquivos.keys()):
                    lista_arquivos = self.mapa_arquivos[sintese]
                    lista_df = []
                    for arquivo in lista_arquivos:
                        caminho_arquivo = c.caminho+"/"+arquivo
                        media_values = []
                        estagios = []
                        with open(caminho_arquivo, 'r') as file:
                            for line in file:
                                inicio = line[0:10].split()
                                if("MEDIA" in inicio):
                                    temp = []
                                    temp = [float(value) for value in line.split()[1:]]
                                    temp.pop()
                                    media_values = media_values + temp
                        dados_dger = Dger.read(c.caminho+"/dger.dat")
                        ano_inicio = dados_dger.ano_inicio_estudo
                        mes_inicio = dados_dger.mes_inicio_estudo
                        start_date = str(ano_inicio)+"-"+str(mes_inicio)+"-01"
                        media_values  = media_values[mes_inicio-1:]
                        estagios = list(range(1, len(media_values) + 1))
                        num_months = len(media_values)  # Change this to your desired number
                        date_range = pd.date_range(start=start_date, periods=num_months, freq='MS', tz='UTC')
                        
                        #end_date = str(ano_inicio)+"-"+str(mes_inicio)+"-01"
                        #date_range = pd.date_range(start=start_date, periods=num_months, freq='MS', tz='UTC')

                        df = pd.DataFrame({'Timestamp': date_range})
                        dicionario = {
                            "estagio":estagios,
                            "data_inicio":date_range,
                            "valor":media_values,
                            "limite_superior":media_values,
                            "limite_inferior":media_values,
                            #"data_fim":
                        }
                        df = pd.DataFrame(dicionario)
                        df["cenario"] = "mean"
                        df["patamar"] = 0
                        df["caso"] = c.nome
                        df["modelo"] = c.modelo
                        df["codigo_usina"] = None
                        df["codigo_ree"] = None
                        if(len(lista_arquivos) == 4):
                            codigo_sbm = int(re.search(r'(\d+)\.out$', arquivo).group(1))
                            df["codigo_submercado"] = codigo_sbm
                        else:
                            df["codigo_submercado"] = None
                        df["variavel"] = sintese.split("_")[0]
                        #print(df)
                        lista_df.append(df.copy())
                    df_resultado = pd.concat(lista_df)
                    #print(df_resultado)    
                    #exit(1)
                    result_dict [c] = df_resultado

        return result_dict 

    def checkIfNumberOnly(self,s):
        try:
            float(s)  # Check if string can be converted to a float
            return True
        except ValueError:
            return False