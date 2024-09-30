
from apps.report.info.SIN.NEWAVE.estruturas import Estruturas
from apps.indicadores.eco_indicadores import EcoIndicadores
from inewave.newave import Dger
from inewave.newave import Cvar
import os


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

        temp = self.template_Tabela_Eco_Entrada
        temp = temp.replace("Caso", caso.nome)
        temp = temp.replace("Modelo", caso.modelo)

        if(os.path.isfile(caso.caminho+"/sintese/EARMI_SIN_EST.parquet.gzip")):
            df = self.eco_indicadores.retorna_df_concatenado("EARMI_SIN_EST")
            df_caso = df.loc[(df["caso"] == caso.nome) & (df["cenario"] == "mean")]
            valor = df_caso.loc[(df_caso["estagio"] == 1) ]["valor"].iloc[0]
            temp = temp.replace("EarmI", str(round(valor,2)))
        
        if(os.path.isfile(caso.caminho+"/sintese/EARPI_SIN_EST.parquet.gzip")):
            df = self.eco_indicadores.retorna_df_concatenado("EARPI_SIN_EST")
            df_caso = df.loc[(df["caso"] == caso.nome) & (df["cenario"] == "mean")]
            valor = df_caso.loc[(df_caso["estagio"] == 1) ]["valor"].iloc[0]
            temp = temp.replace("EarpI", str(round(valor,2)))

        if(os.path.isfile(caso.caminho+"/sintese/GTER_SIN_EST.parquet.gzip")):
            df_gt = self.eco_indicadores.retorna_df_concatenado("GTER_SIN_EST")
            df_gt_caso = df_gt.loc[(df_gt["caso"] == caso.nome) & (df_gt["cenario"] == "mean")]
            gt_2_mes = df_gt_caso.loc[(df_gt_caso["estagio"] == 2) ]["valor"].iloc[0]
            temp = temp.replace("2_Mes_GT", str(round(gt_2_mes,2)))

            gt_avg = df_gt_caso["valor"].mean()
            temp = temp.replace("Media_GT", str(round(gt_avg,2)))

        if(os.path.isfile(caso.caminho+"/sintese/GHID_SIN_EST.parquet.gzip")):
            df_gh = self.eco_indicadores.retorna_df_concatenado("GHID_SIN_EST")
            df_gh_caso = df_gh.loc[(df_gh["caso"] == caso.nome) & (df_gh["cenario"] == "mean")]
            gh_2_mes = df_gh_caso.loc[(df_gh_caso["estagio"] == 2) ]["valor"].iloc[0]
            temp = temp.replace("2_Mes_GH", str(round(gh_2_mes,2)))

            gh_avg = df_gh_caso["valor"].mean()
            temp = temp.replace("Media_GH", str(round(gh_avg,2)))

        if(os.path.isfile(caso.caminho+"/sintese/GHID_SIN_EST.parquet.gzip")):
            df_earpf = self.eco_indicadores.retorna_df_concatenado("EARPF_SIN_EST")
            df_earpf_caso = df_earpf.loc[(df_earpf["caso"] == caso.nome) & (df_earpf["cenario"] == "mean")]
            earpf_2_mes = df_earpf_caso.loc[(df_earpf_caso["estagio"] == 2) ]["valor"].iloc[0]
            temp = temp.replace("2_Mes_EARPF", str(round(earpf_2_mes,2)))

            earpf_avg = df_earpf_caso["valor"].mean()
            temp = temp.replace("Media_EARPF", str(round(earpf_avg,2)))


        return temp
