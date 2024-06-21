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
from idecomp.decomp.custos import Custos
from idecomp.decomp.fcfnw import Fcfnw
from idecomp.decomp.caso import Caso

import os
import json

class FCF:


    def __init__(self, data):
        self.estudo = data.estudo
        self.casos = data.casos
        self.indicadores_temporais = IndicadoresTemporais(data.casos)
        self.graficos = Graficos(data)
        diretorio_saida = f"resultados/{self.estudo}/fcf"
        os.makedirs(diretorio_saida, exist_ok=True)

        for arg in data.args:
            if(arg.chave == "UHE"):
                sts = Sintese("VAGUA_UHE_EST") #SINTESE DUMMY
                conj = ConjuntoUnidadeSintese(sts, arg, "estagios", data.limites, data.tamanho_texto)
                for unity in conj.listaUnidades:
                    print(unity.arg.chave)
            print(arg.nome, " chave: ", arg.chave, " lista: ", arg.listaNomes)
        exit(1)



        set_modelos =set({})
        for caso in self.casos:
            set_modelos.add(caso.modelo)
        
        print(set_modelos)
        if(len(set_modelos) == 1):
            modelo = list(set_modelos)[0]
            if(modelo == "DECOMP"):
                extensao = ""
                with open(caso.caminho+"/caso.dat") as f:
                    extensao = f.readline().strip('\n')
                if extensao == "":
                    raise FileNotFoundError(f"Arquivo caso.dat não encontrado.") 

                arq_memcal = caso.caminho+"/memcal."+extensao
                if(os.path.isfile(arq_memcal)):
                    f = open(arq, "r")
                    Lines = f.readlines()
                    flag = 0
                    for line in Lines:
                        if(usina[0] in line):
                            flag = 1
                        if(flag == 1 and "SOMATORIO PRODT_65%=" in line):
                            #print(line[25:50])
                            f_prodt_65 = float(line[25:50].strip())
                            flag = 0
                else:
                    raise FileNotFoundError(f"Arquivo memcal.rvx não encontrado.") 

                exit(1) 


        else:
            print("ERRO: Tentativa de plotar FCF Com mais de um modelo no JSON")
            exit(1)

        exit(1)

        

                        

 
    def executa(self, conjUnity, diretorio_saida_arg): 
        mapa_temporal = {}
        for unity in conjUnity.listaUnidades:
            mapa_temporal[unity] = self.indicadores_temporais.retorna_df_concatenado(unity)
            self.indicadores_temporais.exportar(mapa_temporal[unity], diretorio_saida_arg,  "temporal "+unity.titulo+" "+self.estudo)
                
        mapaGO = self.graficos.gera_grafico_linha(mapa_temporal)
        figura = Figura(conjUnity, mapaGO, "Temporal "+conjUnity.titulo+self.estudo)
        self.graficos.exportar(figura.fig, diretorio_saida_arg, figura.titulo)
        
        ultimo_estagio = max(mapa_temporal[list(mapa_temporal.keys())[0]]["estagio"])
        mapaEst = {1:" Primeiro Est ",
                   2:" Segundo Est ",
                   ultimo_estagio:" Ultimo Est "}
        for est in mapaEst:
            mapa_estagio = {}
            for unity in conjUnity.listaUnidades:
                mapa_estagio[unity] = mapa_temporal[unity].loc[mapa_temporal[unity]["estagio"] == est]
                self.indicadores_temporais.exportar(mapa_estagio[unity], diretorio_saida_arg,  mapaEst[est]+conjUnity.sintese.sintese+" "+self.estudo)
                    
            mapaGO = self.graficos.gera_grafico_barra(conjUnity, mapa_estagio, mapaEst[est]+conjUnity.titulo+" "+self.estudo)
            figura = Figura(conjUnity, mapaGO, mapaEst[est]+conjUnity.sintese.sintese+" "+self.estudo)
            self.graficos.exportar(figura.fig, diretorio_saida_arg, figura.titulo)


        #df_unity_2_mes = self.indicadores_temporais.retorna_df_concatenado_medio_2_mes(unity)
        #self.indicadores_temporais.exportar(df_unity_2_mes, diretorio_saida_arg,  unity.titulo+"_temporal_2_mes_"+self.estudo)
        
        #fig = self.graficos.gera_grafico_barra(df_unity_2_mes["valor"], df_unity_2_mes["caso"],  unity.legendaEixoX, unity.legendaEixoY, 2, unity.titulo+"2_mes")
        #self.graficos.exportar(fig, diretorio_saida_arg, unity.titulo+"_temporal_2_mes_"+self.estudo)






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
    
