
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

        oper = self.eco_indicadores.retorna_df_concatenado("ESTATISTICAS_OPERACAO_SBM")
        codigos_sbm = self.eco_indicadores.retorna_df_concatenado("SBM")
        cod_sbm = codigos_sbm.loc[(codigos_sbm["submercado"] == arg)]["codigo_submercado"].iloc[0]
        oper_sbm = oper.loc[(oper["caso"] == caso.nome) & (oper["codigo_submercado"] == cod_sbm) ]

        earpi = oper_sbm.loc[(oper_sbm["variavel"] == "EARPI") & (oper_sbm["estagio"] == 1) & (oper_sbm["cenario"] == "mean") & (oper_sbm["patamar"] == 0)]["valor"].iloc[0]
        earmi = oper_sbm.loc[(oper_sbm["variavel"] == "EARMI") & (oper_sbm["estagio"] == 1) & (oper_sbm["cenario"] == "mean") & (oper_sbm["patamar"] == 0)]["valor"].iloc[0]

        temp = temp.replace("EarmI", str(round(earmi,2)))
        temp = temp.replace("EarpI", str(round(earpi,2)))


        gt_2_mes = oper_sbm.loc[(oper_sbm["variavel"] == "GTER") & (oper_sbm["estagio"] == 2) & (oper_sbm["cenario"] == "mean") & (oper_sbm["patamar"] == 0)]["valor"].iloc[0]
        gh_2_mes = oper_sbm.loc[(oper_sbm["variavel"] == "GHID") & (oper_sbm["estagio"] == 2) & (oper_sbm["cenario"] == "mean") & (oper_sbm["patamar"] == 0)]["valor"].iloc[0]
        earpf_2_mes = oper_sbm.loc[(oper_sbm["variavel"] == "EARPF") & (oper_sbm["estagio"] == 2) & (oper_sbm["cenario"] == "mean") & (oper_sbm["patamar"] == 0)]["valor"].iloc[0]
        cmo_2_mes = oper_sbm.loc[(oper_sbm["variavel"] == "CMO") & (oper_sbm["estagio"] == 2) & (oper_sbm["cenario"] == "mean") & (oper_sbm["patamar"] == 0)]["valor"].iloc[0]

        print(round(gt_2_mes,2))
        print(round(gh_2_mes,2))
        print(round(earpf_2_mes,2))
        print(round(cmo_2_mes,2))

        temp = temp.replace("2_Mes_GT", str(round(gt_2_mes,2)))
        temp = temp.replace("2_Mes_GH", str(round(gh_2_mes,2)))
        temp = temp.replace("2_Mes_EARPF", str(round(earpf_2_mes,2)))
        temp = temp.replace("2_Mes_CMO", str(round(cmo_2_mes,2)))

        gt_avg = oper_sbm.loc[(oper_sbm["variavel"] == "GTER") & (oper_sbm["cenario"] == "mean") & (oper_sbm["patamar"] == 0)]["valor"].mean()
        gh_avg = oper_sbm.loc[(oper_sbm["variavel"] == "GHID") & (oper_sbm["cenario"] == "mean") & (oper_sbm["patamar"] == 0)]["valor"].mean()
        earpf_avg = oper_sbm.loc[(oper_sbm["variavel"] == "EARPF") & (oper_sbm["cenario"] == "mean") & (oper_sbm["patamar"] == 0)]["valor"].mean()
        cmo_avg = oper_sbm.loc[(oper_sbm["variavel"] == "CMO") & (oper_sbm["cenario"] == "mean") & (oper_sbm["patamar"] == 0)]["valor"].mean()

        print(round(gt_avg,2))
        print(round(gh_avg,2))
        print(round(earpf_avg,2))
        print(round(cmo_avg,2))

        temp = temp.replace("Media_GT", str(round(gt_avg,2)))
        temp = temp.replace("Media_GH", str(round(gh_avg,2)))
        temp = temp.replace("Media_EARPF", str(round(earpf_avg,2)))
        temp = temp.replace("Media_CMO", str(round(cmo_avg,2)))


        return temp
