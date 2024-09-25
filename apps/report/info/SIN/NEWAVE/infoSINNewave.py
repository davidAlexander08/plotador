
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

        earpf_i = round(earmi_first_per/earm_max_first_per,2)
        #varm_i = round(varmi_first_per,2)

        temp = temp.replace("EarmI", str(round(earmi_first_per,2)))
        temp = temp.replace("EarpI", str(earpf_i))
        #temp = temp.replace("VarmI", str(varm_i))

        
        oper = self.eco_indicadores.retorna_df_concatenado("ESTATISTICAS_OPERACAO_SIN")
        oper_sin = oper.loc[(oper["caso"] == caso.nome)]

        gt_2_mes = oper_sin.loc[(oper_sin["variavel"] == "GTER") & (oper_sin["estagio"] == 2) & (oper_sin["cenario"] == "mean") & (oper_sin["patamar"] == 0)]["valor"].iloc[0]
        gh_2_mes = oper_sin.loc[(oper_sin["variavel"] == "GHID") & (oper_sin["estagio"] == 2) & (oper_sin["cenario"] == "mean") & (oper_sin["patamar"] == 0)]["valor"].iloc[0]
        earpf_2_mes = oper_sin.loc[(oper_sin["variavel"] == "EARPF") & (oper_sin["estagio"] == 2) & (oper_sin["cenario"] == "mean") & (oper_sin["patamar"] == 0)]["valor"].iloc[0]

        temp = temp.replace("2_Mes_GT", str(round(gt_2_mes,2)))
        temp = temp.replace("2_Mes_GH", str(round(gh_2_mes,2)))
        temp = temp.replace("2_Mes_EARPF", str(round(earpf_2_mes,2)))

        gt_avg = oper_sin.loc[(oper_sin["variavel"] == "GTER") & (oper_sin["estagio"] == 2) & (oper_sin["cenario"] == "mean") & (oper_sin["patamar"] == 0)]["valor"].mean()
        gh_avg = oper_sin.loc[(oper_sin["variavel"] == "GHID") & (oper_sin["estagio"] == 2) & (oper_sin["cenario"] == "mean") & (oper_sin["patamar"] == 0)]["valor"].mean()
        earpf_avg = oper_sin.loc[(oper_sin["variavel"] == "EARPF") & (oper_sin["estagio"] == 2) & (oper_sin["cenario"] == "mean") & (oper_sin["patamar"] == 0)]["valor"].mean()

        temp = temp.replace("Media_GT", str(round(gt_avg,2)))
        temp = temp.replace("Media_GH", str(round(gh_avg,2)))
        temp = temp.replace("Media_EARPF", str(round(earpf_avg,2)))



        return temp
