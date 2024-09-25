
from apps.report.info.SBM.DESSEM.estruturas import Estruturas
from apps.indicadores.eco_indicadores import EcoIndicadores
from idessem.dessem.des_log_relato import DesLogRelato

class InfoSBMDessem(Estruturas):
    def __init__(self, data, par_dados):
        Estruturas.__init__(self)
        argumentos = par_dados[1]
        print(argumentos)
        mapa_sbm = {"SUDESTE":"SE", "NORDESTE":"NE", "NORTE":"N", "SUL":"S"}
        mapa_sbm_inverso = {"SE":"SUDESTE", "NE":"NORDESTE", "N":"NORTE", "S":"SUL"}
        lista_sbm = list(mapa_sbm.keys())
        lista_sbm_inv = list(mapa_sbm_inverso.keys())
        lista_argumentos = []
        if(argumentos is None):
            lista_argumentos = lista_sbm
        else:
            for arg in argumentos:
                if(arg in lista_sbm):
                    lista_argumentos.append(arg)
                elif(arg in lista_sbm_inv):
                    lista_argumentos.append(mapa_sbm_inverso[arg])
                else:
                    print("SUBMERCADO: ", arg, " NAO RECONHECIDO")
                    exit(1)

        self.eco_indicadores = EcoIndicadores(data.casos)
        self.lista_text = []
        self.lista_text.append(self.Tabela_Eco_Entrada)
        for caso in data.casos:
            if(caso.modelo == "DESSEM"):
                for arg in lista_argumentos:
                    temp = self.preenche_modelo_tabela_modelo(caso, arg)
                    self.lista_text.append(temp)
        self.lista_text.append("</table>"+"\n")

        self.text_html = "\n".join(self.lista_text)

    def preenche_modelo_tabela_modelo(self,caso, arg):


        temp = self.template_Tabela_Eco_Entrada
        temp = temp.replace("Caso", caso.nome)
        temp = temp.replace("Modelo", caso.modelo)

        data_des_log = DesLogRelato.read(caso.caminho+"/DES_LOG_RELATO.DAT")
        temp = temp.replace("Versao", data_des_log.versao)
        


        df_gt = self.eco_indicadores.retorna_df_concatenado("GTER_SBM_EST")
        df_gt_caso = df_gt.loc[(df_gt["caso"] == caso.nome) & (df_gt["submercado"] == arg)]
        print(arg)
        print(df_gt_caso)

        gt_1_dia = df_gt_caso.loc[(df_gt_caso["estagio"] <= 48)]["valor"].mean()
        print(gt_1_dia)
        temp = temp.replace("1_Dia_GT", str(round(gt_1_dia,2)))

        gt_avg = df_gt_caso["valor"].mean()
        temp = temp.replace("Media_GT", str(round(gt_avg,2)))

        df_gh = self.eco_indicadores.retorna_df_concatenado("GHID_SBM_EST")
        df_gh_caso = df_gh.loc[(df_gh["caso"] == caso.nome) & (df_gh["submercado"] == arg)]

        gh_1_dia = df_gh_caso["valor"].mean()
        temp = temp.replace("1_Dia_GH", str(round(gh_1_dia,2)))

        gh_avg = df_gh_caso["valor"].mean()
        temp = temp.replace("Media_GH", str(round(gh_avg,2)))
        
        df_earmf = self.eco_indicadores.retorna_df_concatenado("EARMF_SBM_EST")
        df_earmf_caso = df_earmf.loc[(df_earmf["caso"] == caso.nome) & (df_earmf["submercado"] == arg)]

        earmf_1_dia = df_earmf_caso.loc[(df_earmf_caso["estagio"] <= 48)]["valor"].mean()
        temp = temp.replace("1_Dia_EARMF", str(round(earmf_1_dia,2)))
        
        earmf_avg = df_earmf_caso["valor"].mean()
        temp = temp.replace("Media_EARMF", str(round(earmf_avg,2)))



        return temp
