
from apps.report.info.SBM.NEWAVE.estruturas import Estruturas
from apps.indicadores.eco_indicadores import EcoIndicadores
import os

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

        self.eco_indicadores = EcoIndicadores(data.conjuntoCasos[0].casos)
        self.lista_text = []

        for arg in ["SUDESTE"]:#lista_argumentos:
            self.lista_text.append("<h3>Dados "+arg+"</h3>")
            self.lista_text.append(self.Tabela_Eco_Entrada)
            for caso in data.conjuntoCasos[0].casos:
                if(caso.modelo == "NEWAVE"):
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
        temp = temp.replace("Subm", arg)
            

        if(os.path.isfile(caso.caminho+"/sintese/ESTATISTICAS_OPERACAO_SBM.parquet")):
            print(caso.nome, arg)
            
            oper = self.eco_indicadores.retorna_df_concatenado("ESTATISTICAS_OPERACAO_SBM")
            codigos_sbm = self.eco_indicadores.retorna_df_concatenado("SBM")
            cod_sbm = codigos_sbm.loc[(codigos_sbm["submercado"] == arg)]["codigo_submercado"].iloc[0]
            oper_sbm = oper.loc[(oper["caso"] == caso.nome) & (oper["codigo_submercado"] == cod_sbm) & (oper["cenario"] == "mean") & (oper["patamar"] == 0)]
            first_month = oper_sbm.loc[(oper_sbm["estagio"] == 1)]
            second_month = oper_sbm.loc[(oper_sbm["estagio"] == 2)]
            
            if(oper_sbm['variavel'].str.contains("EARPI", case=False, na=False).any()):
                earpi = first_month.loc[(first_month["variavel"] == "EARPI") ]["valor"].iloc[0]
                temp = temp.replace("EarpI", str(round(earpi,2)))

            if(oper_sbm['variavel'].str.contains("EARMI", case=False, na=False).any()):
                earmi = first_month.loc[(first_month["variavel"] == "EARMI") ]["valor"].iloc[0]
                temp = temp.replace("EarmI", str(round(earmi,2)))
            
            if(oper_sbm['variavel'].str.contains("GTER", case=False, na=False).any()):
                gt_2_mes = second_month.loc[(second_month["variavel"] == "GTER") ]["valor"].iloc[0]
                gt_avg = oper_sbm.loc[(oper_sbm["variavel"] == "GTER") ]["valor"].mean()
                temp = temp.replace("2_Mes_GT", str(round(gt_2_mes,2)))
                temp = temp.replace("Media_GT", str(round(gt_avg,2)))

            if(oper_sbm['variavel'].str.contains("EARPF", case=False, na=False).any()):      
                earpf_2_mes = second_month.loc[(second_month["variavel"] == "EARPF") ]["valor"].iloc[0]
                earpf_avg = oper_sbm.loc[(oper_sbm["variavel"] == "EARPF") ]["valor"].mean()
                temp = temp.replace("2_Mes_EARPF", str(round(earpf_2_mes,2)))
                temp = temp.replace("Media_EARPF", str(round(earpf_avg,2)))

            if(oper_sbm['variavel'].str.contains("CMO", case=False, na=False).any()):        
                cmo_2_mes = second_month.loc[(second_month["variavel"] == "CMO") ]["valor"].iloc[0]
                cmo_avg = oper_sbm.loc[(oper_sbm["variavel"] == "CMO") ]["valor"].mean()
                temp = temp.replace("2_Mes_CMO", str(round(cmo_2_mes,2)))
                temp = temp.replace("Media_CMO", str(round(cmo_avg,2)))
        return temp
