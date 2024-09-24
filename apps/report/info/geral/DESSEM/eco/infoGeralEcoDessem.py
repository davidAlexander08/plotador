
from apps.report.info.geral.DESSEM.eco.estruturas import Estruturas
from apps.indicadores.eco_indicadores import EcoIndicadores
from idessem.dessem.des_log_relato import DesLogRelato
from inewave.newave import Dger
from inewave.newave import Cvar


class InfoGeralEcoDessem(Estruturas):
    def __init__(self, data):
        Estruturas.__init__(self)
        self.eco_indicadores = EcoIndicadores(data.casos)
        self.lista_text = []
        self.lista_text.append(self.Tabela_Eco_Entrada)
        for caso in data.casos:
            if(caso.modelo == "DESSEM"):
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
        data_des_log = DesLogRelato.read(caso.caminho+"/DES_LOG_RELATO.DAT")
        #temp = temp.replace("Versao", data_des_log.versao)
        #temp = temp.replace("Data", str(data_des_log.data_estudo))

        print(data_des_log.versao)
        print(data_des_log.data_estudo)
        print(data_des_log.tempo_processamento)
        print(data_des_log.variaveis_otimizacao)
        

        exit(1)

        #ENTDADOS
        #GAP CONVERGENCIA


        data_dger = Dger.read(caso.caminho+"/dger.dat")
        data_cvar = Cvar.read(caso.caminho+"/cvar.dat")
        
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
        temp = temp.replace("CVAR", str(data_cvar.valores_constantes[0])+"x"+str(data_cvar.valores_constantes[1]))
        return temp
