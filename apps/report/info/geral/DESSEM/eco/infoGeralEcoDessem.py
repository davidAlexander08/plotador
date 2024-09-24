
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
        temp = temp.replace("Versao", data_des_log.versao)
        temp = temp.replace("Data", str(data_des_log.data_estudo))


        temp = temp.replace("Tempo", str(data_des_log.tempo_processamento))
        print(data_des_log.versao)
        print(data_des_log.data_estudo)
        print(data_des_log.tempo_processamento)
        print(data_des_log.variaveis_otimizacao)
        

        return temp
