
from apps.report.info.geral.DESSEM.eco.estruturas import Estruturas
from apps.indicadores.eco_indicadores import EcoIndicadores
from idessem.dessem.des_log_relato import DesLogRelato
from idessem.dessem.dessopc import Dessopc
import os

class InfoGeralEcoDessem(Estruturas):
    def __init__(self, data):
        Estruturas.__init__(self)
        self.eco_indicadores = EcoIndicadores(data.conjuntoCasos[0].casos)
        self.lista_text = []
        self.lista_text.append(self.Tabela_Eco_Entrada)
        for caso in data.conjuntoCasos[0].casos:
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
        if(os.path.isfile(caso.caminho+"/DES_LOG_RELATO.DAT")):
            data_des_log = DesLogRelato.read(caso.caminho+"/DES_LOG_RELATO.DAT")
            temp = temp.replace("Versao", data_des_log.versao)
            temp = temp.replace("Data", str(data_des_log.data_estudo))

        if(os.path.isfile(caso.caminho+"/dessopc.dat")):
            data_dessopc = Dessopc.read(caso.caminho+"/dessopc.dat")
            ucterm = data_dessopc.ucterm #INCLUSAO OU NAO UCTERM
            crossover = data_dessopc.crossover #ALTERACOES DO CROSSOVER
            #engolimento = data_dessopc.engolimento #CONSIDERA ENGOLIMENTO MAXIMO
            #tratainviabilha = data_dessopc.tratainviabilha #TRATA INVIAB ILHA
            string_ucterm = "None" if ucterm is None else str(ucterm)
            string_crossover = "None" if crossover is None else ' '.join(map(str, crossover[:-1]))

            temp = temp.replace("Ucterm", string_ucterm)
            temp = temp.replace("Crossover", string_crossover)
        

        return temp
