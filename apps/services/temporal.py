import pandas as pd
from typing import Dict
from apps.model.unidade import UnidadeSintese
from apps.model.conjuntoUnidade import ConjuntoUnidadeSintese
from apps.graficos.graficos import Graficos
from apps.indicadores.indicadores_temporais import IndicadoresTemporais
from apps.indicadores.eco_indicadores import EcoIndicadores
from apps.model.caso import Caso
from apps.model.sintese import Sintese
from apps.model.argumento import Argumento
from apps.model.unidadeArgumental import UnidadeArgumental
from apps.graficos.figura import Figura
from apps.model.caso import Caso
import os 
import json

class Temporal:


    def __init__(self, data, xinf, xsup,estagio, cenario, sintese, largura, altura, eixox, cronologico, labely, booltitulo, titulo, showlegend, labelx, argumentos, chave, tamanho, boxplot,csv, html, outpath, ysup, yinf, y2, y2sup, y2inf, patamar, liminf, limsup):
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
        self.y2 = y2
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
        self.chave = chave
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
        self.eco_indicadores = EcoIndicadores(data.conjuntoCasos[0].casos)
        self.graficos = Graficos(data)
        # Gera saídas do estudo


        diretorio_saida = f"resultados/{self.estudo}/temporal" if outpath is None else outpath
        os.makedirs(diretorio_saida, exist_ok=True)

        meta_dados = self.eco_indicadores.retorna_df(data.conjuntoCasos[0].casos[0], "METADADOS_OPERACAO")
        df_chave = meta_dados.loc[(meta_dados["chave"] == self.sintese)]
        titulo_meta = df_chave["nome_longo_variavel"]
        if(self.labely is None):
            self.labely = df_chave["unidade"].iloc[0]
            

        if(self.argumentos is not None and self.chave is None):
            print("FALTA DECLARAR A CHAVE DO ARGUMENTO")
            exit(1)
        if(self.chave is not None and self.argumentos is None):
            print("FALTA DECLARAR O ARGUMENTO DO ARGUMENTO")
            exit(1)
        if(self.chave is not None and self.argumentos is not None):
            lista_argumentos = self.argumentos.split(",")
            list_arg = []
            for arg in lista_argumentos:
                list_arg.append(arg.replace("_"," "))
            lista_argumentos = list_arg
            data.args = [Argumento(lista_argumentos, self.chave, "out")] 
            if(len(lista_argumentos) == 1 and self.titulo == " "): 
                self.titulo = lista_argumentos[0]

        #NOVIDADE
        if(self.sintese is None):
            print("POR FAVOR DECLARAR UMA SINTESE COM O ARGUMENTO --sintese")
            exit(1)
        self.sts = Sintese(self.sintese)

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
                if(self.sts.espacial == arg.chave):
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
        mapa_eco = self.eco_indicadores.retornaMapaDF(self.sts.sintese)
        print(mapa_eco)
        for unity in conjUnity.listaUnidades:
            print("INICIOU retornar temporal")
            #df_temporal = self.indicadores_temporais.retorna_df_concatenado(unity, self.boxplot)
            df_temporal = self.retorna_df_concatenado(mapa_eco, unity, self.boxplot)
            print("Retornou Temporal")
            if(self.xsup < df_temporal["estagio"].max()):
                df_temporal = df_temporal.loc[(df_temporal["estagio"] <= self.xsup)]
            if(self.xinf > df_temporal["estagio"].min()):
                df_temporal = df_temporal.loc[(df_temporal["estagio"] >= self.xinf)]
            print("Limitou os eixos")
            mapa_temporal[unity] = df_temporal
            print("Guardou no mapa")
            #mapa_temporal[unity] = pd.concat(lista_data_frame)
            if(self.csv == "True"): self.indicadores_temporais.exportar(mapa_temporal[unity], diretorio_saida_arg,  "Temporal "+conjUnity.titulo+unity.titulo+self.estudo)
        print("PASSO 2")
        if(self.boxplot == "True"):
            mapaGO = self.graficos.gera_grafico_boxplot(mapa_temporal, colx = self.eixox)
            titulo_padrao = "Boxplot Temporal "+conjUnity.titulo+self.estudo
        else:
            mapaGO = self.graficos.gera_grafico_linha(mapa_temporal, colx = self.eixox, cronologico = self.cronologico, eixo_y2 = self.y2, liminf = self.liminf, limsup = self.limsup)
            titulo_padrao = "Temporal "+conjUnity.titulo+self.estudo


        print("PASSO 3")
        

        tituloFigura = titulo_padrao if self.booltitulo == "True" else " "
        tituloFigura = titulo_padrao if self.titulo == " " else self.titulo.replace("_", " ")

        figura = Figura(conjUnity, mapaGO, tituloFigura, self.yinf, self.ysup, self.y2, self.y2sup, self.y2inf)
        if(self.showlegend == "False"):
            figura.fig.update_layout(showlegend= False)
        self.graficos.exportar(figura.fig, diretorio_saida_arg, tituloFigura, self.html, self.largura, self.altura)
        
        print("PASSO 4")
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

            print("PASSO 5")
            #unity = UnidadeSintese("EARPF_SIN_EST", None, "%", "Energia_Armazenada_Percentual_Final_SIN_CREF "+estudo)
            #df_unity = indicadores_temporais.retorna_df_concatenado(unity)
            #graficos.gera_graficos_linha_Newave_CREF(df_unity, indicadores_temporais.df_cref, "EARPF", unity.legendaEixoY, unity.titulo, None).write_image(
            #    os.path.join(diretorio_saida, "SIN_EARPF_CREF"+estudo+".png"),
            #    width=800,
            #    height=600
            #    )
            #graficos.gera_graficos_linha_Newave_CREF(df_unity, indicadores_temporais.df_cref, "EARPF", unity.legendaEixoY, unity.titulo+"_2024", "2024").write_image(
            #    os.path.join(diretorio_saida, "SIN_EARPF_CREF_2024"+estudo+".png"),
            #    width=800,
            #    height=600
            #    )
            #graficos.gera_graficos_linha_Newave_CREF(df_unity, indicadores_temporais.df_cref, "EARPF", unity.legendaEixoY, unity.titulo+"_Ano_Vigente", "ADEQUA").write_image(
            #    os.path.join(diretorio_saida, "SIN_EARPF_CREF_AnoCaso"+estudo+".png"),
            #    width=800,
            #    height=600
            #    )
            #df_EARPF_mean_p10_p90 = indicadores_temporais.gera_df_mean_p10_p90("EARPF_SIN_EST")
            #graficos.gera_graficos_linha_mean_p10_p90_CREF(df_EARPF_mean_p10_p90,indicadores_temporais.df_cref, "EARPF", "%", "Energia Armazenada Cenarios CREF"+estudo, None ).write_image(
            #    os.path.join(diretorio_saida, "Energia_Armazenada_Media_P10_P90_"+estudo+".png"),
            #    width=800,
            #    height=600
            #    )
    
    def retorna_df_concatenado(self, eco_mapa, unidade, boxplot):
        return pd.concat(self.retorna_mapaDF_cenario_medio_temporal(eco_mapa, unidade, boxplot))
    
    def __retorna_mapa_media_parquet(self, mapa):
        dict = {}
        for c in self.casos:
            df = mapa[c]
            #print(df)
            if(c.modelo == "NEWAVE" or c.modelo == "DECOMP"):
                dict[c] = df.loc[(df["cenario"] == c.tipo) & (df["patamar"] == c.patamar)].reset_index(drop = True)
            if(c.modelo == "DESSEM"):   
                dict[c] = df.reset_index(drop = True) 
        return dict

    def retorna_mapaDF_cenario_medio_temporal(self, eco_mapa, unidade, boxplot):
        mapa_temporal = {}
        if( (unidade.sintese.filtro is None) & (unidade.filtroArgumento is None) ):
            if(boxplot =="True"):
                return eco_mapa
            else:
                return self.__retorna_mapa_media_parquet(eco_mapa)
        else: 
            mapa_argumentos = self.retornaMapaDF(unidade.sintese.espacial)
            
            coluna_filtro = unidade.sintese.filtro.split("_")[1]
            for c in self.casos:
                cod_arg = mapa_argumentos[c].loc[(mapa_argumentos[c][coluna_filtro] == unidade.filtroArgumento)][unidade.sintese.filtro].iloc[0]
                eco_mapa[c] = eco_mapa[c].loc[eco_mapa[c][unidade.sintese.filtro] == cod_arg]
                
            if(boxplot =="True"):
                mapa_temporal = eco_mapa
            else:
                mapa_temporal = self.__retorna_mapa_media_parquet(eco_mapa)
        return mapa_temporal