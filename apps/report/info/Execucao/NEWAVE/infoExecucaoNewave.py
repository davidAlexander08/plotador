
from apps.report.info.Execucao.NEWAVE.estruturas import Estruturas
from apps.indicadores.eco_indicadores import EcoIndicadores
from inewave.newave import Pmo
from inewave.newave import Dger
from inewave.newave import Cvar
import math
import os

class InfoExecucaoNewave(Estruturas):
    def __init__(self, data):
        Estruturas.__init__(self)
        self.eco_indicadores = EcoIndicadores(data.conjuntoCasos[0].casos)
        self.lista_text = []
        self.lista_text.append(self.Tabela_Eco_Entrada)
        for caso in data.conjuntoCasos[0].casos:
            if(caso.modelo == "NEWAVE"):
                temp = self.preenche_modelo_tabela_modelo_NEWAVE(caso)
                self.lista_text.append(temp)
        self.lista_text.append("</table>"+"\n")

        self.text_html = "\n".join(self.lista_text)

    def preenche_modelo_tabela_modelo_NEWAVE(self,caso):
        temp = self.template_Tabela_Eco_Entrada
        temp = temp.replace("Caso", caso.nome)
        temp = temp.replace("Modelo", caso.modelo)

        if(os.path.isfile(caso.caminho+"/sintese/TEMPO.parquet")):
            df_temp = self.eco_indicadores.retorna_df_concatenado("TEMPO")
            df_caso = df_temp.loc[(df_temp["caso"] == caso.nome)]
            tempo_inicial = df_caso.loc[(df_caso["etapa"] == "Calculos Iniciais")]["tempo"].iloc[0]/60
            tempo_politica = df_caso.loc[(df_caso["etapa"] == "Calculo da Politica")]["tempo"].iloc[0]/60
            tempo_sf = df_caso.loc[(df_caso["etapa"] == "Simulacao Final")]["tempo"].iloc[0]/60
            tempo_total = df_caso["tempo"].sum()/60

            h_tempo_inicial =    0 if tempo_inicial < 60 else math.floor(tempo_inicial/60)
            h_tempo_politica =    0 if tempo_politica < 60 else math.floor(tempo_politica/60)
            h_tempo_sf =          0 if tempo_sf       < 60 else math.floor(tempo_sf/60)
            h_tempo_total =       0 if tempo_total    < 60 else math.floor(tempo_total/60)

            min_tempo_inicial =    round(tempo_inicial,0)  if h_tempo_inicial == 0 else  round(tempo_inicial - h_tempo_inicial*60 ,0)
            min_tempo_politica =    round(tempo_politica,0)  if h_tempo_politica == 0 else  round(tempo_politica - h_tempo_politica*60 ,0)
            min_tempo_sf =          round(tempo_sf,0)        if h_tempo_sf       == 0 else  round(tempo_sf - h_tempo_sf*60 ,0)
            min_tempo_total =       round(tempo_total,0)     if h_tempo_total    == 0 else  round(tempo_total - h_tempo_total*60 ,0)

            temp = temp.replace("Calc Inicio (min)", str(h_tempo_inicial)+ " h " + str(min_tempo_inicial) + " min")
            temp = temp.replace("Politica (min)", str(h_tempo_politica)+ " h " + str(min_tempo_politica) + " min")
            temp = temp.replace("Sim. Final (Min)", str(h_tempo_sf)+ " h " + str(min_tempo_sf) + " min")
            temp = temp.replace("Total (min)", str(h_tempo_total)+ " h " + str(min_tempo_total) + " min")

            #temp = temp.replace("Calc Inicio (min)", str(round(tempo_inicial,2)))
            #temp = temp.replace("Politica (min)", str(round(tempo_politica,2)))
            #temp = temp.replace("Sim. Final (Min)", str(round(tempo_sf,2)))
            #temp = temp.replace("Total (min)", str(round(tempo_total,2)))


        if(os.path.isfile(caso.caminho+"/sintese/CONVERGENCIA.parquet")):
            df_conv = self.eco_indicadores.retorna_df_concatenado("CONVERGENCIA")
            df_caso_conv = df_conv.loc[(df_conv["caso"] == caso.nome)]
            iteracao =      df_caso_conv["iteracao"].iloc[-1]
            zinf =          df_caso_conv["zinf"].iloc[-1]
            zsup =          df_caso_conv["zsup"].iloc[-1]
            t_ultimo_pl =   df_caso_conv["tempo"].iloc[-1]/60
            temp = temp.replace("Iter", str(round(iteracao,2)))
            temp = temp.replace("Zinf", str(round(zinf,2)))
            temp = temp.replace("Zsup", str(round(zsup,2)))
            temp = temp.replace("Ultimo PL (min)", str(round(t_ultimo_pl,2)))

        #    <td>Caso</td>
        #    <td>Modelo</td>
        #    <td>Versao</td>
        #    <td>Dados Entrada (min)</td>
        #    <td>Politica (min)</td>
        #    <td>Sim. Final (Min)</td>
        #    <td>Total (min)</td>
        #    <td>Zinf</td>
        #    <td>Zsup</td>

        return temp
