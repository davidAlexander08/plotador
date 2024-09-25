
from apps.report.info.Execucao.DESSEM.estruturas import Estruturas
from apps.indicadores.eco_indicadores import EcoIndicadores
from idessem.dessem.des_log_relato import DesLogRelato

class InfoExecucaoDessem(Estruturas):
    def __init__(self, data):
        Estruturas.__init__(self)
        self.eco_indicadores = EcoIndicadores(data.casos)
        self.lista_text = []
        self.lista_text.append(self.Tabela_Eco_Entrada)
        for caso in data.casos:
            if(caso.modelo == "DESSEM"):
                temp = self.preenche_modelo_tabela_modelo(caso)
                self.lista_text.append(temp)
        self.lista_text.append("</table>"+"\n")

        self.text_html = "\n".join(self.lista_text)

    def preenche_modelo_tabela_modelo(self,caso):




        temp = self.template_Tabela_Eco_Entrada
        temp = temp.replace("Caso", caso.nome)
        temp = temp.replace("Modelo", caso.modelo)
        data_des_log = DesLogRelato.read(caso.caminho+"/DES_LOG_RELATO.DAT")
        temp = temp.replace("Versao", data_des_log.versao)


        df_temp = self.eco_indicadores.retorna_df_concatenado("TEMPO")
        
        df_caso = df_temp.loc[(df_temp["caso"] == caso.nome)]
        print(df_caso)
        print(df_caso.loc[(df_caso["etapa"] == "      MILP")])
        tempo_MILP =        df_caso.loc[(df_caso["etapa"] == "MILP")]["tempo"].iloc[0]
        tempo_PL_INT_FIX =  df_caso.loc[(df_caso["etapa"] == "PL.Int.Fix")]["tempo"].iloc[0]
        tempo_Calc_CMO =    df_caso.loc[(df_caso["etapa"] == "PL.CalcCMO")]["tempo"].iloc[0]
        tempo_total =       df_caso["tempo"].sum()

        temp = temp.replace("MILP (min)", str(round(tempo_MILP,2)))
        temp = temp.replace("PL_INT_FIX (min)", str(round(tempo_PL_INT_FIX,2)))
        temp = temp.replace("Calc_CMO (Min)", str(round(tempo_Calc_CMO,2)))
        temp = temp.replace("Total (min)", str(round(tempo_total,2)))


        return temp
