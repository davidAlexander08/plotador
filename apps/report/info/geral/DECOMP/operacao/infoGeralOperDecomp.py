
from apps.report.info.geral.NEWAVE.operacao.estruturas import Estruturas
from apps.indicadores.eco_indicadores import EcoIndicadores
from idecomp.decomp.relato import Relato
from idecomp.decomp.caso import Caso
import os
import pandas as pd
import math 
class InfoGeralOperDecomp(Estruturas):
    def __init__(self, data):
        Estruturas.__init__(self)
        self.eco_indicadores = EcoIndicadores(data.conjuntoCasos[0].casos)
        self.lista_text = []
        self.lista_text.append(self.Tabela_Operacao)
        for caso in data.conjuntoCasos[0].casos:
            if(caso.modelo == "DECOMP"):
                temp = self.preenche_operacao(caso)
                self.lista_text.append(temp)
        self.lista_text.append("</table>"+"\n")
        self.text_html = "\n".join(self.lista_text)

    def preenche_operacao(self,caso):

        
        temp = self.template_Tabela_Operacao
        temp = temp.replace("Caso", caso.nome)
        temp = temp.replace("Modelo", caso.modelo)

        extensao = ""
        with open(caso.caminho+"/caso.dat") as f:
            extensao = f.readline().strip('\n')
        if extensao == "":
            raise FileNotFoundError(f"Arquivo caso.dat não encontrado.") 

        if(os.path.isfile(caso.caminho+"/relato."+extensao)):
            data_relato = Relato.read(caso.caminho+"/relato."+extensao)
            
            ultima_iteracao = data_relato.convergencia["iteracao"].iloc[-1]
            ultimo_zinf = data_relato.convergencia["zinf"].iloc[-1]
            ultimo_zsup = data_relato.convergencia["zsup"].iloc[-1]
            ultimo_gap = data_relato.convergencia["gap_percentual"].iloc[-1]
            ultimo_tempo = data_relato.convergencia["tempo"].iloc[-1]

            custo_presente_med = data_relato.relatorio_operacao_custos["custo_presente"].mean()
            custo_futuro_med   = data_relato.relatorio_operacao_custos["custo_futuro"].mean()
            gerao_term_med  = data_relato.relatorio_operacao_custos["geracao_termica"].mean()
            cmo_SE_1_est   = data_relato.relatorio_operacao_custos["cmo_SE"].iloc[0]
            cmo_NE_1_est   = data_relato.relatorio_operacao_custos["cmo_NE"].iloc[0]
            cmo_SE_mean   = data_relato.relatorio_operacao_custos["cmo_SE"].mean()
            cmo_NE_mean   = data_relato.relatorio_operacao_custos["cmo_NE"].mean()

            temp = temp.replace("Versao", "v")
            temp = temp.replace("Zinf",             str(ultimo_zinf       )  )
            temp = temp.replace("Zsup",             str(ultimo_zsup       )  )
            temp = temp.replace("Gap",              str(ultimo_gap        )  )
            temp = temp.replace("Tempo",            str(ultimo_tempo      )  )
            temp = temp.replace("Custo_P. (avg)",   str(custo_presente_med)  )
            temp = temp.replace("Custo_Fut. (avg)", str(custo_futuro_med  )  )
            temp = temp.replace("CMO_SE (avg)",     str(cmo_SE_1_est      )  )
            temp = temp.replace("CMO_NE (avg)",     str(cmo_NE_1_est      )  )
            temp = temp.replace("CMO_SE (1 est)",   str(cmo_SE_mean       )  )
            temp = temp.replace("CMO_SE (1 est)",   str(cmo_NE_mean       )  )
            )
        
            #<td>Zinf</td>
            #<td>Zsup</td>
            #<td>Gap</td>
            #<td>Iter</td>
            #<td>Tempo</td>
            #<td>Custo_P. (avg)</td>
            #<td>Custo_Fut. (avg)</td>
            #<td>CMO_SE (avg)</td>
            #<td>CMO_NE (avg)</td>
            #<td>CMO_SE (1 est)</td>
            #<td>CMO_SE (1 est)</td>

            #print(data_relato.convergencia)
            #print(data_relato.convergencia.columns)
            #print(data_relato.relatorio_operacao_custos.columns)
            #print(data_relato.relatorio_operacao_custos)

       #if(os.path.isfile(caso.caminho+"/sintese/TEMPO.parquet")):
       #    df_temp = self.eco_indicadores.retorna_df_concatenado("TEMPO")
       #    df_caso = df_temp.loc[(df_temp["caso"] == caso.nome)]
       #    tempo_politica = df_caso.loc[(df_caso["etapa"] == "Calculo da Politica")]["tempo"].iloc[0]/60
       #    tempo_sf = df_caso.loc[(df_caso["etapa"] == "Simulacao Final")]["tempo"].iloc[0]/60
       #    tempo_total = df_caso["tempo"].sum()/60

       #    h_tempo_politica =    0 if tempo_politica < 60 else math.floor(tempo_politica/60)
       #    h_tempo_sf =          0 if tempo_sf       < 60 else math.floor(tempo_sf/60)
       #    h_tempo_total =       0 if tempo_total    < 60 else math.floor(tempo_total/60)

       #    min_tempo_politica =    round(tempo_politica,0)  if h_tempo_politica == 0 else  round(tempo_politica - h_tempo_politica*60 ,0)
       #    min_tempo_sf =          round(tempo_sf,0)        if h_tempo_sf       == 0 else  round(tempo_sf - h_tempo_sf*60 ,0)
       #    min_tempo_total =       round(tempo_total,0)     if h_tempo_total    == 0 else  round(tempo_total - h_tempo_total*60 ,0)

       #    #temp = temp.replace("tempo_politica", str(round(tempo_politica, 2)))
       #    #temp = temp.replace("tempo_sf", str(round(tempo_sf, 2)))
       #    #temp = temp.replace("tempo_total", str(round(tempo_total, 2)))


       #    temp = temp.replace("tempo_politica", str(h_tempo_politica)+ " h " + str(min_tempo_politica) + " min")
       #    temp = temp.replace("tempo_sf", str(h_tempo_sf)+ " h " + str(min_tempo_sf) + " min")
       #    temp = temp.replace("tempo_total", str(h_tempo_total)+ " h " + str(min_tempo_total) + " min")
       #else:
       #    pass

       #if(os.path.isfile(caso.caminho+"/sintese/CONVERGENCIA.parquet")):
       #    df_temp = self.eco_indicadores.retorna_df_concatenado("CONVERGENCIA")
       #    df_caso = df_temp.loc[(df_temp["caso"] == caso.nome)]
       #    iteracoes = df_caso["iteracao"].iloc[-1]
       #    zinf = df_caso["zinf"].iloc[-1]
       #    temp = temp.replace("iteracoes", str(iteracoes))
       #    temp = temp.replace("zinf", str(zinf))




        return temp

