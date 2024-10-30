
from apps.report.info.SIN.NEWAVE.estruturas import Estruturas
from apps.indicadores.eco_indicadores import EcoIndicadores
from inewave.newave import Pmo
from inewave.newave import Dger
from inewave.newave import Cvar
import os


class InfoSINNewave(Estruturas):
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

        tempo_total = iteracoes = zinf = custo_total = desvio_custo = 0
        versao = "0"
        temp = self.template_Tabela_Eco_Entrada
        temp = temp.replace("Caso", caso.nome)
        temp = temp.replace("Modelo", caso.modelo)


        if(os.path.isfile(caso.caminho+"/sintese/ESTATISTICAS_OPERACAO_SIN.parquet")):
            print(caso.nome)
            oper = self.eco_indicadores.retorna_df_concatenado("ESTATISTICAS_OPERACAO_SIN")
            oper_sin = oper.loc[(oper["caso"] == caso.nome) & (oper["cenario"] == "mean") & (oper["patamar"] == 0) ]
            first_month = oper_sin.loc[(oper_sin["estagio"] == 1) ]
            second_month = oper_sin.loc[(oper_sin["estagio"] == 2) ]
            print("INICIA SUBSTITUICAO")
            if(oper_sin['variavel'].str.contains("EARMI", case=False, na=False).any()):
                earmi_first_per = first_month.loc[(first_month["variavel"] == "EARMI") ]["valor"].iloc[0]
                temp = temp.replace("EarmI", str(round(earmi_first_per,2)))

            if(oper_sin['variavel'].str.contains("EARPI", case=False, na=False).any()):
                earpf_i = first_month.loc[(first_month["variavel"] == "EARPI")]["valor"].iloc[0]
                temp = temp.replace("EarpI", str(earpf_i))
            
            if(oper_sin['variavel'].str.contains("GTER", case=False, na=False).any()):
                gt_2_mes = second_month.loc[(second_month["variavel"] == "GTER") ]["valor"].iloc[0]
                temp = temp.replace("2_Mes_GT", str(round(gt_2_mes,2)))
                gt_avg = oper_sin.loc[(oper_sin["variavel"] == "GTER") ]["valor"].mean()
                temp = temp.replace("Media_GT", str(round(gt_avg,2)))

            if(oper_sin['variavel'].str.contains("EARPF", case=False, na=False).any()):
                earpf_2_mes = second_month.loc[(second_month["variavel"] == "EARPF")]["valor"].iloc[0]
                temp = temp.replace("2_Mes_EARPF", str(round(earpf_2_mes,2)))
                earpf_avg = oper_sin.loc[(oper_sin["variavel"] == "EARPF")]["valor"].mean()
                temp = temp.replace("Media_EARPF", str(round(earpf_avg,2)))
            print("FIM SUBSTITUICAO")
        return temp
