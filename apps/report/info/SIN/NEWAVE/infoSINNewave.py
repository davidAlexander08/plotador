
from apps.report.info.SIN.NEWAVE.estruturas import Estruturas
from apps.indicadores.eco_indicadores import EcoIndicadores
from inewave.newave import Pmo
from inewave.newave import Dger
from inewave.newave import Cvar


class InfoSINNewave(Estruturas):
    def __init__(self, data):
        Estruturas.__init__(self)
        self.eco_indicadores = EcoIndicadores(data.casos)
        self.lista_text = []
        self.lista_text.append(self.Tabela_Eco_Entrada)
        for caso in data.casos:
            if(caso.modelo == "NEWAVE"):
                temp = self.preenche_modelo_tabela_modelo_NEWAVE(caso)
                self.lista_text.append(temp)
        self.lista_text.append("</table>"+"\n")

        self.text_html = "\n".join(self.lista_text)

    def preenche_modelo_tabela_modelo_NEWAVE(self,caso):

        df_temp = self.eco_indicadores.retorna_df_concatenado("TEMPO")

        tempo_total = iteracoes = zinf = custo_total = desvio_custo = 0
        versao = "0"
        temp = self.template_Tabela_Eco_Entrada
        temp = temp.replace("Caso", caso.nome)
        temp = temp.replace("Modelo", caso.modelo)
        data_pmo = Pmo.read(caso.caminho+"/pmo.dat")
        data_dger = Dger.read(caso.caminho+"/dger.dat")
        data_cvar = Cvar.read(caso.caminho+"/cvar.dat")
        temp = temp.replace("Versao", data_pmo.versao_modelo)

        earm_max = data_pmo.energia_armazenada_maxima
        earmi = data_pmo.energia_armazenada_inicial
        varmi = data_pmo.volume_armazenado_inicial
        
        earm_max_first_per = earm_max.loc[(earm_max["configuracao"] == 1)]["valor_MWmes"].sum()
        earmi_first_per = earmi["valor_MWmes"].sum()
        varmi_first_per = varmi["valor_hm3"].sum()
        print(earm_max)
        print(earmi)
        print(varmi)


        print(earm_max_first_per)
        print(earmi_first_per)

        print(varmi_first_per)
        exit(1)
        



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
#
        #    <td>Caso</td>
        #    <td>Modelo</td>
        #    <td>Versao</td>
        #    <td>EARPI</td>
        #    <td>2_Mes_GT</td>
        #    <td>2_Mes_GH</td>
        #    <td>2_Mes_EARPF</td>
        #    <td>Media_GT</td>
        #    <td>Media_GH</td>
        #    <td>Media_EARPF</td>


        return temp
