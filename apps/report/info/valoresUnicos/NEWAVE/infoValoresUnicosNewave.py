
from apps.report.info.valoresUnicos.NEWAVE.estruturas import Estruturas
from apps.indicadores.eco_indicadores import EcoIndicadores
import os
import pandas as pd

class InfoValoresUnicosNewave(Estruturas):
    def __init__(self, data, par_dados):
        Estruturas.__init__(self)
        self.eco_indicadores = EcoIndicadores(data.conjuntoCasos[0].casos)
        self.lista_text = []
        self.lista_text.append(self.Tabela_Eco_Entrada)
        
        for caso in data.conjuntoCasos[0].casos:
            if(caso.modelo == "NEWAVE"):
                temp = self.preenche_modelo_tabela_modelo_NEWAVE(caso, par_dados)
                self.lista_text.append(temp)
        self.lista_text.append("</table>"+"\n")

        self.text_html = "\n".join(self.lista_text)

    def preenche_modelo_tabela_modelo_NEWAVE(self,caso, par_dados):
        grandeza = par_dados[2]

        argumentos = par_dados[1]
        

        temp = self.template_Tabela_Eco_Entrada
        temp = temp.replace("Caso", caso.nome)
        temp = temp.replace("Modelo", caso.modelo)
        print(grandeza)
        print(argumentos)
        tipo = grandeza.split("_")[0]
        espacial = grandeza.split("_")[1].strip()
        print("tipo: ", tipo, " espacial: ", espacial)
        estatistica = ""
        if(espacial == "SIN"):
            estatistica = "ESTATISTICAS_OPERACAO_SIN"
        elif(espacial == "SBM"):
            estatistica = "ESTATISTICAS_OPERACAO_SBM"
        elif(espacial == "UHE"):
            estatistica = "ESTATISTICAS_OPERACAO_UHE"
        else:
            print("GRANDEZA ESPACIAL DA ESTATISTICA NAO ENCOTRADA NA ROTINA infoValoresUnicosNewave.py")
            exit(1)

        if(os.path.isfile(caso.caminho+"/sintese/"+estatistica+ ".parquet")):            
            oper = pd.read_parquet(caso.caminho+"/sintese/"+estatistica+".parquet",engine = "pyarrow")
            oper_mean = oper.loc[(oper["cenario"] == "mean") & (oper["patamar"] == 0) ]
            first_stage = oper_mean.loc[(oper_mean["estagio"] == 1) ]
            second_month = oper_mean.loc[(oper_mean["estagio"] == 2) ]
            last_stage_value = oper_mean["estagio"].unique()[-1]
            last_stage = oper_mean.loc[(oper_mean["estagio"] == last_stage_value) ]
            
            if(oper_mean['variavel'].str.contains(tipo, case=False, na=False).any()):
                primeiro_valor_grandeza = first_stage.loc[(first_stage["variavel"] == tipo)]["valor"].iloc[0]
                ultimo_valor_grandeza =   last_stage.loc[(last_stage["variavel"] == tipo)]["valor"].iloc[-1]
                segundo_mes_valor = second_month.loc[(second_month["variavel"] == tipo)]["valor"].iloc[0]
                media = oper_mean.loc[(oper_mean["variavel"] == tipo)]["valor"].mean()

                temp = temp.replace("Inicial", str(round(primeiro_valor_grandeza,2)))
                temp = temp.replace("2 Mes", str(round(ultimo_valor_grandeza,2)))
                temp = temp.replace("Média Horiz", str(round(segundo_mes_valor,2)))
                temp = temp.replace("Último", str(round(media,2)))

                print(temp)

        return temp
