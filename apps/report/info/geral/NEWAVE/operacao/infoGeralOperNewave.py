
from apps.report.info.geral.NEWAVE.operacao.estruturas import Estruturas
from apps.indicadores.eco_indicadores import EcoIndicadores
from inewave.newave import Pmo
from inewave.newave import Dger
from inewave.newave import Cvar
import os
import pandas as pd
import math 
class InfoGeralOperNewave(Estruturas):
    def __init__(self, data):
        Estruturas.__init__(self)
        self.eco_indicadores = EcoIndicadores(data.conjuntoCasos[0].casos)
        self.lista_text = []
        self.lista_text.append(self.Tabela_Operacao)
        for caso in data.conjuntoCasos[0].casos:
            if(caso.modelo == "NEWAVE"):
                temp = self.preenche_operacao(caso)
                self.lista_text.append(temp)
        self.lista_text.append("</table>"+"\n")
        self.text_html = "\n".join(self.lista_text)

    def preenche_operacao(self,caso):

        
        temp = self.template_Tabela_Operacao
        temp = temp.replace("Caso", caso.nome)
        temp = temp.replace("Modelo", caso.modelo)
        
        #print("LENDO PMO.DAT")
        if(os.path.isfile(caso.caminho+"/simfinal.dat")):
            data_pmo = Pmo.read(caso.caminho+"/simfinal.dat")
            versao = "" if data_pmo.versao_modelo is None else data_pmo.versao_modelo
            custo_total = 0 if data_pmo.custo_operacao_total is None else data_pmo.custo_operacao_total
            desvio_custo = 0 if data_pmo.desvio_custo_operacao_total is None else data_pmo.desvio_custo_operacao_total*1.96
            temp = temp.replace("custo_total", str(custo_total))
            temp = temp.replace("desvio_custo", str(round(desvio_custo, 2)))
            temp = temp.replace("Versao", versao)
            
        if(os.path.isfile(caso.caminho+"/sintese/TEMPO.parquet")):
            try:
                df_temp = self.eco_indicadores.retorna_df_concatenado("TEMPO")
                df_caso = df_temp.loc[(df_temp["caso"] == caso.nome)]
                tempo_politica = df_caso.loc[(df_caso["etapa"] == "Calculo da Politica")]["tempo"].iloc[0]/60
                tempo_sf = df_caso.loc[(df_caso["etapa"] == "Simulacao Final")]["tempo"].iloc[0]/60
                tempo_total = df_caso["tempo"].sum()/60

                h_tempo_politica =    0 if tempo_politica < 60 else math.floor(tempo_politica/60)
                h_tempo_sf =          0 if tempo_sf       < 60 else math.floor(tempo_sf/60)
                h_tempo_total =       0 if tempo_total    < 60 else math.floor(tempo_total/60)

                min_tempo_politica =    round(tempo_politica,0)  if h_tempo_politica == 0 else  round(tempo_politica - h_tempo_politica*60 ,0)
                min_tempo_sf =          round(tempo_sf,0)        if h_tempo_sf       == 0 else  round(tempo_sf - h_tempo_sf*60 ,0)
                min_tempo_total =       round(tempo_total,0)     if h_tempo_total    == 0 else  round(tempo_total - h_tempo_total*60 ,0)

                temp = temp.replace("tempo_politica", str(h_tempo_politica)+ " h " + str(min_tempo_politica) + " min")
                temp = temp.replace("tempo_sf", str(h_tempo_sf)+ " h " + str(min_tempo_sf) + " min")
                temp = temp.replace("tempo_total", str(h_tempo_total)+ " h " + str(min_tempo_total) + " min")

            except Exception as e:
                print(f"TEMPO nao existe em: ", caso.caminho)
                temp = temp.replace("tempo_politica", "None")
                temp = temp.replace("tempo_sf", "None")
                temp = temp.replace("tempo_total", "None")
                

        if(os.path.isfile(caso.caminho+"/sintese/CONVERGENCIA.parquet")):
            try:
                df_temp = self.eco_indicadores.retorna_df_concatenado("CONVERGENCIA")
                df_caso = df_temp.loc[(df_temp["caso"] == caso.nome)]
                iteracoes = df_caso["iteracao"].iloc[-1]
                zinf = df_caso["zinf"].iloc[-1]
                temp = temp.replace("iteracoes", str(iteracoes))
                temp = temp.replace("zinf", str(zinf))

            except Exception as e:
                print(f"CONVERGENCIA nao existe em: ", caso.caminho)
                temp = temp.replace("iteracoes", "None")
                temp = temp.replace("zinf", "None")



        return temp

