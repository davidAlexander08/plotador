
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
        varm_i = round(varmi_first_per,2)

        temp = temp.replace("EarmI", str(round(earmi_first_per,2)))
        temp = temp.replace("EarpI", str(earpf_i))
        temp = temp.replace("VarmI", str(varm_i))

        df_gt = self.eco_indicadores.retorna_df_concatenado("GTER_SIN_EST")
        df_gt_caso = df_gt.loc[(df_gt["caso"] == caso.nome)]
        df_gh = self.eco_indicadores.retorna_df_concatenado("GHID_SIN_EST")
        df_gh_caso = df_gh.loc[(df_gh["caso"] == caso.nome)]
        df_earpf = self.eco_indicadores.retorna_df_concatenado("EARPF_SIN_EST")
        df_earpf_caso = df_earpf.loc[(df_earpf["caso"] == caso.nome)]

        print(df_gt_caso)
        print(df_gh_caso)
        print(df_earpf_caso)

        gt_2_mes = df_gt_caso.loc[(df_gt_caso["estagio"] == 2) & (df_gt_caso["cenario"] == "mean")]["valor"].iloc[0]
        gh_2_mes = df_gh_caso.loc[(df_gh_caso["estagio"] == 2) & (df_gh_caso["cenario"] == "mean")]["valor"].iloc[0]
        earpf_2_mes = df_earpf_caso.loc[(df_earpf_caso["estagio"] == 2) & (df_earpf_caso["cenario"] == "mean")]["valor"].iloc[0]

        print(round(gt_2_mes,2))
        print(round(gh_2_mes,2))
        print(round(earpf_2_mes,2))

        temp = temp.replace("2_Mes_GT", str(round(gt_2_mes,2)))
        temp = temp.replace("2_Mes_GH", str(round(gh_2_mes,2)))
        temp = temp.replace("2_Mes_EARPF", str(round(earpf_2_mes,2)))

        gt_avg = df_gt_caso.loc[(df_gt_caso["cenario"] == "mean")]["valor"].mean()
        gh_avg = df_gh_caso.loc[(df_gh_caso["cenario"] == "mean")]["valor"].mean()
        earpf_avg = df_earpf_caso.loc[(df_earpf_caso["cenario"] == "mean")]["valor"].mean()

        print(round(gt_avg,2))
        print(round(gh_avg,2))
        print(round(earpf_avg,2))

        temp = temp.replace("Media_GT", str(round(gt_avg,2)))
        temp = temp.replace("Media_GH", str(round(gh_avg,2)))
        temp = temp.replace("Media_EARPF", str(round(earpf_avg,2)))


        #    <td>2_Mes_GT</td>
        #    <td>2_Mes_GH</td>
        #    <td>2_Mes_EARPF</td>
        #    <td>Media_GT</td>
        #    <td>Media_GH</td>
        #    <td>Media_EARPF</td>


        return temp
