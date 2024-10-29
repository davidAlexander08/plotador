
from apps.report.info.SIN.DESSEM.estruturas import Estruturas
from apps.indicadores.eco_indicadores import EcoIndicadores
from idessem.dessem.des_log_relato import DesLogRelato
import os
class InfoSINDessem(Estruturas):
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

        
        temp = self.template_Tabela_Eco_Entrada
        temp = temp.replace("Caso", caso.nome)
        temp = temp.replace("Modelo", caso.modelo)

        if(os.path.isfile(caso.caminho+"/DES_LOG_RELATO.DAT")):
            data_des_log = DesLogRelato.read(caso.caminho+"/DES_LOG_RELATO.DAT")
            temp = temp.replace("Versao", data_des_log.versao)

        if(os.path.isfile(caso.caminho+"/sintese/GTER_SBM_EST.parquet.gzip")):
            df_gt = self.eco_indicadores.retorna_df_concatenado("GTER_SIN_EST")
            df_gt_caso = df_gt.loc[(df_gt["caso"] == caso.nome)]

            gt_1_dia = df_gt_caso.loc[(df_gt_caso["estagio"] <= 48)]["valor"].mean()
            temp = temp.replace("1_Dia_GT", str(round(gt_1_dia,2)))

            gt_avg = df_gt_caso["valor"].mean()
            temp = temp.replace("Media_GT", str(round(gt_avg,2)))

        if(os.path.isfile(caso.caminho+"/sintese/GHID_SIN_EST.parquet.gzip")):
            df_gh = self.eco_indicadores.retorna_df_concatenado("GHID_SIN_EST")
            df_gh_caso = df_gh.loc[(df_gh["caso"] == caso.nome)]

            gh_1_dia = df_gh_caso["valor"].mean()
            temp = temp.replace("1_Dia_GH", str(round(gh_1_dia,2)))

            gh_avg = df_gh_caso["valor"].mean()
            temp = temp.replace("Media_GH", str(round(gh_avg,2)))
        
        if(os.path.isfile(caso.caminho+"/sintese/EARMF_SIN_EST.parquet.gzip")):
            df_earmf = self.eco_indicadores.retorna_df_concatenado("EARMF_SIN_EST")
            df_earmf_caso = df_earmf.loc[(df_earmf["caso"] == caso.nome)]

            earmf_1_dia = df_earmf_caso.loc[(df_earmf_caso["estagio"] <= 48)]["valor"].mean()
            temp = temp.replace("1_Dia_EARMF", str(round(earmf_1_dia,2)))
            
            earmf_avg = df_earmf_caso["valor"].mean()
            temp = temp.replace("Media_EARMF", str(round(earmf_avg,2)))

        return temp
