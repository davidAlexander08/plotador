
from apps.report.info.SBM.NEWAVE.estruturas import Estruturas
from apps.indicadores.eco_indicadores import EcoIndicadores
from inewave.newave import Pmo
from inewave.newave import Dger
from inewave.newave import Cvar


class InfoSBMNewave(Estruturas):
    def __init__(self, data, par_dados):
        Estruturas.__init__(self)
        argumentos = par_dados[1]
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
            if(caso.modelo == "NEWAVE"):
                for arg in lista_argumentos:
                    temp = self.preenche_modelo_tabela_modelo_NEWAVE(caso, arg)
                    self.lista_text.append(temp)
        self.lista_text.append("</table>"+"\n")

        self.text_html = "\n".join(self.lista_text)

    def preenche_modelo_tabela_modelo_NEWAVE(self,caso, arg):

        tempo_total = iteracoes = zinf = custo_total = desvio_custo = 0
        versao = "0"
        temp = self.template_Tabela_Eco_Entrada
        temp = temp.replace("Caso", caso.nome)
        temp = temp.replace("Modelo", caso.modelo)
        data_pmo = Pmo.read(caso.caminho+"/pmo.dat")
        data_dger = Dger.read(caso.caminho+"/dger.dat")
        data_cvar = Cvar.read(caso.caminho+"/cvar.dat")
        temp = temp.replace("Versao", data_pmo.versao_modelo)
        temp = temp.replace("Subm", arg)
        
        df_earpi = self.eco_indicadores.retorna_df_concatenado("EARPI_SBM_EST")
        df_earpi_caso = df_earpi.loc[(df_earpi["caso"] == caso.nome) & (df_earpi["submercado"] == arg) ]
        earpi = df_earpi_caso.loc[(df_earpi_caso["estagio"] == 1) & (df_earpi_caso["cenario"] == "mean")]["valor"].iloc[0]

        df_earmi = self.eco_indicadores.retorna_df_concatenado("EARMI_SBM_EST")
        df_earmi_caso = df_earmi.loc[(df_earmi["caso"] == caso.nome)& (df_earpi["submercado"] == arg) ]
        earmi = df_earmi_caso.loc[(df_earmi_caso["estagio"] == 1) & (df_earmi_caso["cenario"] == "mean")]["valor"].iloc[0]

        temp = temp.replace("EarmI", str(round(earmi,2)))
        temp = temp.replace("EarpI", str(round(earpi,2)))

        df_gt = self.eco_indicadores.retorna_df_concatenado("GTER_SBM_EST")
        df_gt_caso = df_gt.loc[(df_gt["caso"] == caso.nome)& (df_earpi["submercado"] == arg) ]
        df_gh = self.eco_indicadores.retorna_df_concatenado("GHID_SBM_EST")
        df_gh_caso = df_gh.loc[(df_gh["caso"] == caso.nome)& (df_earpi["submercado"] == arg) ]
        df_earpf = self.eco_indicadores.retorna_df_concatenado("EARPF_SBM_EST")
        df_earpf_caso = df_earpf.loc[(df_earpf["caso"] == caso.nome)& (df_earpi["submercado"] == arg) ]

        df_cmo = self.eco_indicadores.retorna_df_concatenado("CMO_SBM_EST")
        df_cmo_caso = df_cmo.loc[(df_cmo["caso"] == caso.nome)& (df_earpi["submercado"] == arg) ]

        print(df_gt_caso)
        print(df_gh_caso)
        print(df_earpf_caso)

        gt_2_mes = df_gt_caso.loc[(df_gt_caso["estagio"] == 2) & (df_gt_caso["cenario"] == "mean")]["valor"].iloc[0]
        gh_2_mes = df_gh_caso.loc[(df_gh_caso["estagio"] == 2) & (df_gh_caso["cenario"] == "mean")]["valor"].iloc[0]
        earpf_2_mes = df_earpf_caso.loc[(df_earpf_caso["estagio"] == 2) & (df_earpf_caso["cenario"] == "mean")]["valor"].iloc[0]
        cmo_2_mes = df_cmo_caso.loc[(df_cmo_caso["estagio"] == 2) & (df_cmo_caso["cenario"] == "mean")]["valor"].iloc[0]

        print(round(gt_2_mes,2))
        print(round(gh_2_mes,2))
        print(round(earpf_2_mes,2))
        print(round(cmo_2_mes,2))

        temp = temp.replace("2_Mes_GT", str(round(gt_2_mes,2)))
        temp = temp.replace("2_Mes_GH", str(round(gh_2_mes,2)))
        temp = temp.replace("2_Mes_EARPF", str(round(earpf_2_mes,2)))
        temp = temp.replace("2_Mes_CMO", str(round(cmo_2_mes,2)))

        gt_avg = df_gt_caso.loc[(df_gt_caso["cenario"] == "mean")]["valor"].mean()
        gh_avg = df_gh_caso.loc[(df_gh_caso["cenario"] == "mean")]["valor"].mean()
        earpf_avg = df_earpf_caso.loc[(df_earpf_caso["cenario"] == "mean")]["valor"].mean()
        cmo_avg = df_cmo_caso.loc[(df_cmo_caso["cenario"] == "mean")]["valor"].mean()

        print(round(gt_avg,2))
        print(round(gh_avg,2))
        print(round(earpf_avg,2))
        print(round(cmo_avg,2))

        temp = temp.replace("Media_GT", str(round(gt_avg,2)))
        temp = temp.replace("Media_GH", str(round(gh_avg,2)))
        temp = temp.replace("Media_EARPF", str(round(earpf_avg,2)))
        temp = temp.replace("Media_CMO", str(round(cmo_avg,2)))


        return temp
