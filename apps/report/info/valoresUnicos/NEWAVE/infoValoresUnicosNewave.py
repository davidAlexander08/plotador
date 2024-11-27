
from apps.report.info.valoresUnicos.NEWAVE.estruturas import Estruturas
from apps.indicadores.eco_indicadores import EcoIndicadores
import os
import pandas as pd

class InfoValoresUnicosNewave(Estruturas):
    def __init__(self, data, par_dados):
        Estruturas.__init__(self)
        self.eco_indicadores = EcoIndicadores(data.conjuntoCasos[0].casos)
        self.lista_text = []
        print(par_dados)
        if(par_dados[1] == [""]):
            par_dados[1] = ["SIN"]
            print("ENTROU AQUI")
            exit(1)
        grandeza = par_dados[2]
        argumentos = par_dados [1]
        for arg in argumentos:
            self.lista_text.append("<h3>Dados "+arg+"</h3>")
            self.lista_text.append(self.Tabela_Eco_Entrada)
            for caso in data.conjuntoCasos[0].casos:
                if(caso.modelo == "NEWAVE"):
                    temp = self.preenche_modelo_tabela_modelo_NEWAVE(caso, arg, grandeza)
                    self.lista_text.append(temp)
            self.lista_text.append("</table>"+"\n")

        self.text_html = "\n".join(self.lista_text)

    def preenche_modelo_tabela_modelo_NEWAVE(self,caso, arg, grandeza):

        temp = self.template_Tabela_Eco_Entrada
        temp = temp.replace("Caso", caso.nome)
        temp = temp.replace("Modelo", caso.modelo)
        temp = temp.replace("Argumento", arg)
        temp = temp.replace("Grandeza", grandeza)
        
        print(grandeza)
        print(arg)

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
            if(arg != "SIN"):
                if(espacial == "SBM"):
                    codigos_sbm = pd.read_parquet(caso.caminho+"/sintese/SBM.parquet",engine = "pyarrow")
                    cod_sbm = codigos_sbm.loc[(codigos_sbm["submercado"] == arg)]["codigo_submercado"].iloc[0]
                    oper_mean = oper_mean.loc[(oper_mean["codigo_submercado"] == cod_sbm) ]
                if(espacial == "UHE"):
                    codigos_usi = pd.read_parquet(caso.caminho+"/sintese/UHE.parquet",engine = "pyarrow")
                    cod_usi = codigos_usi.loc[(codigos_usi["usina"] == arg)]["codigo_usina"].iloc[0]
                    oper_mean = oper_mean.loc[(oper_mean["codigo_usina"] == cod_usi) ]
            
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
