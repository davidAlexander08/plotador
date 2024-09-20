
from apps.report.info.UHE.NEWAVE.estruturas import Estruturas
from apps.indicadores.eco_indicadores import EcoIndicadores
from inewave.newave import Pmo
from inewave.newave import Dger
from inewave.newave import Cvar


class InfoUHENewave(Estruturas):
    def __init__(self, data, par_dados):
        Estruturas.__init__(self)
        argumentos = par_dados[1]
        if(argumentos is None):
            lista_argumentos = ["ITAIPU", "FURNAS"]

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
        temp = temp.replace("UHE", arg)
        
        df_varmi = self.eco_indicadores.retorna_df_concatenado("VARMI_UHE_EST")
        df_varmi_caso = df_varmi.loc[(df_varmi["caso"] == caso.nome) & (df_varmi["usina"] == arg) ]
        varmi = df_varmi_caso.loc[(df_varmi_caso["estagio"] == 1) & (df_varmi_caso["cenario"] == "mean")]["valor"].iloc[0]

        temp = temp.replace("VarmI", str(round(varmi,2)))

        return temp
