
from apps.report.info.geral.NEWAVE.eco.estruturas import Estruturas
from apps.indicadores.eco_indicadores import EcoIndicadores
from inewave.newave import Pmo
from inewave.newave import Dger
from inewave.newave import Cvar
import os

class InfoGeralEcoNewave(Estruturas):
    def __init__(self, data):
        Estruturas.__init__(self)
        self.eco_indicadores = EcoIndicadores(data.conjuntoCasos[0].casos)
        self.lista_text = []
        self.lista_text.append(self.Tabela_Eco_Entrada)
        for caso in data.conjuntoCasos[0].casos:
            if(caso.modelo == "NEWAVE"):
                temp = self.preenche_modelo_tabela_modelo(caso)
                self.lista_text.append(temp)
        self.lista_text.append("</table>"+"\n")

        self.text_html = "\n".join(self.lista_text)

    def preenche_modelo_tabela_modelo(self,caso):


        tempo_total = iteracoes = zinf = custo_total = desvio_custo = 0
        versao = "0"
        temp = self.template_Tabela_Eco_Entrada
        temp = temp.replace("Caso", caso.nome)
        temp = temp.replace("Modelo", caso.modelo)

        if(os.path.isfile(caso.caminho+"/dger.dat")):  
            data_dger = Dger.read(caso.caminho+"/dger.dat")
            temp = temp.replace("Mes_I", str(data_dger.mes_inicio_estudo))
            temp = temp.replace("Ano_I", str(data_dger.ano_inicio_estudo))
            temp = temp.replace("Anos_Pos", str(data_dger.num_anos_pos_estudo))
            temp = temp.replace("It_Max", str(data_dger.num_max_iteracoes))
            temp = temp.replace("It_Min", str(data_dger.num_minimo_iteracoes))
            temp = temp.replace("FW", str(data_dger.num_forwards))
            temp = temp.replace("BK", str(data_dger.num_aberturas))
            temp = temp.replace("N_series_sim_final", str(data_dger.num_series_sinteticas))
            tipo_sim_fin = "Ind" if data_dger.agregacao_simulacao_final == 1 else "Agr"
            temp = temp.replace("SF_Ind", tipo_sim_fin)

        if(os.path.isfile(caso.caminho+"/cvar.dat")): 
            data_cvar = Cvar.read(caso.caminho+"/cvar.dat")
            temp = temp.replace("CVAR", str(round(data_cvar.valores_constantes[0],0))+"x"+str(round(data_cvar.valores_constantes[1],0)))
        return temp
