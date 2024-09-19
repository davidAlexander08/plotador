
from apps.report.info.geral.NEWAVE.estruturas import Estruturas
from apps.report.info.geral.NEWAVE.eco.InfoGeralEcoNewave import InfoGeralEcoNewave
from apps.indicadores.eco_indicadores import EcoIndicadores
from inewave.newave import Pmo
from inewave.newave import Dger
from inewave.newave import Cvar


class InfoGeralNewave():
    def __init__(self, data):
        self.eco_indicadores = EcoIndicadores(data.casos)
        self.lista_text = []

        self.lista_text.append(InfoGeralEcoNewave(data).text_html)

        Tabela_Operacao_NEWAVE = """
        <tr>
            <th>Caso</th>
            <th>Modelo</th>
            <th>Temp. Tot(min)</th>
            <th>Iter</th>
            <th>Zinf</th>
            <th>Custo Total</th>
            <th>Desvio Custo</th>
        </tr>
    """      

        #self.lista_text.append("<h2>Operacao</h2>"+"\n")
        #
        #flag_nw = flag_deco = flag_dss = True
        #for caso in data.casos:
        #    if(caso.modelo == "NEWAVE"):
        #        if(flag_nw == True):
        #            self.lista_text.append(self.mapa_tabela_modelo[caso.modelo])
        #            flag_nw = False
        #        temp = self.preenche_operacao_NEWAVE(caso)
        #    self.lista_text.append(temp)
        #self.lista_text.append("</table>"+"\n")

        self.text_html = "\n".join(self.lista_text)

    def preenche_operacao_NEWAVE(self,caso):

        #df_temp = self.eco_indicadores.retorna_df_concatenado("TEMPO")
        #temp = self.mapa_template_tabela_modelo[caso.modelo]
        #temp = temp.replace("Caso", caso.nome)
        #temp = temp.replace("Modelo", caso.modelo)
        #data_pmo = Pmo.read(caso.caminho+"/pmo.dat")
        #data_dger = Dger.read(caso.caminho+"/dger.dat")
        #data_cvar = Cvar.read(caso.caminho+"/cvar.dat")
        #print(data_dger.num_series_sinteticas)
        #temp = temp.replace("Versao", data_pmo.versao_modelo)
        #temp = temp.replace("Mes_I", str(data_dger.mes_inicio_estudo))
        #temp = temp.replace("Ano_I", str(data_dger.ano_inicio_estudo))
        #temp = temp.replace("Anos_Pos", str(data_dger.num_anos_pos_estudo))
        #temp = temp.replace("It_Max", str(data_dger.num_max_iteracoes))
        #temp = temp.replace("It_Min", str(data_dger.num_minimo_iteracoes))
        #temp = temp.replace("FW", str(data_dger.num_forwards))
        #temp = temp.replace("BK", str(data_dger.num_aberturas))
        #temp = temp.replace("N_series_sim_final", str(data_dger.num_series_sinteticas))
        #tipo_sim_fin = "Ind" if data_dger.agregacao_simulacao_final == 1 else "Agr"
        #temp = temp.replace("SF_Ind", tipo_sim_fin)
        #temp = temp.replace("CVAR", str(data_cvar.valores_constantes[0])+"x"+str(data_cvar.valores_constantes[1]))
        ##df_caso = df_temp.loc[(df_temp["caso"] == caso.nome)]
        ##tempo_total = df_caso.loc[(df_caso["etapa"] == "Tempo Total")]["tempo"].iloc[0]/60
        ##iteracoes = data_pmo.convergencia["iteracao"].iloc[-1]
        ##zinf = data_pmo.convergencia["zinf"].iloc[-1]
        ##custo_total = data_pmo.custo_operacao_total
        ##desvio_custo = data_pmo.desvio_custo_operacao_total*1.96
        ##temp = temp.replace("tempo_total", str(tempo_total))
        ##temp = temp.replace("iteracoes", str(iteracoes))
        ##temp = temp.replace("zinf", str(zinf))
        ##temp = temp.replace("custo_total", str(custo_total))
        ##temp = temp.replace("desvio_custo", str(desvio_custo))
#
        #return temp
        pass

