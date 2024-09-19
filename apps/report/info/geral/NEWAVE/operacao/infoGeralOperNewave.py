
from apps.report.info.geral.NEWAVE.operacao.estruturas import Estruturas
from apps.indicadores.eco_indicadores import EcoIndicadores
from inewave.newave import Pmo
from inewave.newave import Dger
from inewave.newave import Cvar


class InfoGeralOperNewave(Estruturas):
    def __init__(self, data):
        Estruturas.__init__(self)
        self.eco_indicadores = EcoIndicadores(data.casos)
        self.lista_text = []
        self.lista_text.append(self.Tabela_Operacao_NEWAVE)

        for caso in data.casos:
            if(caso.modelo == "NEWAVE"):
                temp = self.preenche_operacao_NEWAVE(caso)
                self.lista_text.append(temp)
        self.lista_text.append("</table>"+"\n")

        self.text_html = "\n".join(self.lista_text)

    def preenche_operacao_NEWAVE(self,caso):

        df_temp = self.eco_indicadores.retorna_df_concatenado("TEMPO")
        temp = self.template_Tabela_Operacao_NEWAVE
        temp = temp.replace("Caso", caso.nome)
        temp = temp.replace("Modelo", caso.modelo)
        data_pmo = Pmo.read(caso.caminho+"/pmo.dat")
        data_dger = Dger.read(caso.caminho+"/dger.dat")
        data_cvar = Cvar.read(caso.caminho+"/cvar.dat")


        df_caso = df_temp.loc[(df_temp["caso"] == caso.nome)]
        tempo_total = df_caso.loc[(df_caso["etapa"] == "Tempo Total")]["tempo"].iloc[0]/60
        iteracoes = data_pmo.convergencia["iteracao"].iloc[-1]
        zinf = data_pmo.convergencia["zinf"].iloc[-1]
        custo_total = data_pmo.custo_operacao_total
        desvio_custo = data_pmo.desvio_custo_operacao_total*1.96
        temp = temp.replace("tempo_total", str(tempo_total))
        temp = temp.replace("iteracoes", str(iteracoes))
        temp = temp.replace("zinf", str(zinf))
        temp = temp.replace("custo_total", str(custo_total))
        temp = temp.replace("desvio_custo", str(desvio_custo))
        return temp

