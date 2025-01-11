
from apps.report.info.MaioresValores.NEWAVE.estruturas import Estruturas
from inewave.newave import Dger
import os
import pandas as pd
import pyarrow.parquet as pq

class InfoMaioresValoresNewave(Estruturas):
    def __init__(self, data, par_dados):
        Estruturas.__init__(self)
        #AJUSTE DOS ANOS
        unique_years = set()
        for caso in data.conjuntoCasos[0].casos:
            oper = pd.read_parquet(caso.caminho+"/sintese/ESTATISTICAS_OPERACAO_SIN.parquet",engine = "pyarrow")
            if(par_dados[3] == "True"):
                dados_dger = Dger.read(caso.caminho+"/dger.dat")
                anos_estudo = dados_dger.num_anos_estudo
                mes_inicial = dados_dger.mes_inicio_estudo
                periodos_estudo = anos_estudo*12 - mes_inicial + 1
                df_caso = oper.loc[(oper["estagio"] <= periodos_estudo)]
            else:
                df_caso = oper

        self.lista_text = []
        grandeza = par_dados[2]
        argumentos = par_dados [1]
        posnw = par_dados[3]

        for arg in argumentos:
            if(arg == ""):
                arg = "SIN"
            temp = self.Tabela_Eco_Entrada
            temp = temp.replace("Caso", arg)
            self.lista_text.append(temp)

            for caso in data.conjuntoCasos[0].casos:
                if(caso.modelo == "NEWAVE"):
                    self.preenche_modelo_tabela_modelo_NEWAVE(caso, arg, grandeza, posnw)
            self.lista_text.append("</table>"+"\n")

        self.text_html = "\n".join(self.lista_text)

    def preenche_modelo_tabela_modelo_NEWAVE(self,caso, arg, grandeza, posnw):

        temp = self.template_Tabela_Eco_Entrada
        temp = temp.replace("Caso", caso.nome)
        temp = temp.replace("Modelo", caso.modelo)
        temp = temp.replace("Argumento", arg)
        temp = temp.replace("Grandeza", grandeza)
        

        tipo = grandeza.split("_")[0]
        espacial = grandeza.split("_")[1].strip()
        if(os.path.isfile(caso.caminho+"/sintese/"+grandeza+ ".parquet")):           
            parquet_file = pq.ParquetFile(caso.caminho+"/sintese/"+grandeza+ ".parquet")
            if(arg != "SIN"):
                if(espacial == "SBM"):
                    #codigos_sbm = pd.read_parquet(caso.caminho+"/sintese/SBM.parquet",engine = "pyarrow")
                    #cod_sbm = codigos_sbm.loc[(codigos_sbm["submercado"] == arg)]["codigo_submercado"].iloc[0]
                    #oper = oper.loc[(oper["codigo_submercado"] == cod_sbm) ]
                    None
                if(espacial == "UHE"):
                    codigos_usi = pd.read_parquet(caso.caminho+"/sintese/UHE.parquet",engine = "pyarrow")
                    cod_usi = codigos_usi.loc[(codigos_usi["usina"] == arg)]["codigo_usina"].iloc[0]
                    #oper = oper.loc[(oper["codigo_usina"] == cod_usi) ]
                    subset_df = parquet_file.read(columns=["usina", "valor"]).to_pandas()
                    print(subset_df)
                    filtered_subset = subset_df[subset_df["usina"] == cod_usi]
                    largest_values = filtered_subset["valor"].nlargest(5)
                    filters = [
                        ("usina", "==", cod_usi),
                        ("valor", "in", largest_values.tolist())
                    ]
                    filtered_data = pq.read_table(file_path, filters=filters).to_pandas()
                    print(filtered_data)
            else:
                None
            
            if(posnw == "False"):
                dados_dger = Dger.read(caso.caminho+"/dger.dat")
                anos_estudo = dados_dger.num_anos_estudo
                mes_inicial = dados_dger.mes_inicio_estudo
                periodos_estudo = anos_estudo*12 - mes_inicial + 1
                oper = oper.loc[(oper["estagio"] <= periodos_estudo)]
            #SELECIONA 5 MAIORES VALORES 
            largest_values = oper['valor'].nlargest(5)
            print(largest_values)
            for valor in largest_values:
                print("valor: ", valor)
                df_valor = oper.loc[(oper["valor"] == valor)]
                for index, row in df_valor.iterrows():
                    temp = temp.replace("Periodo", str(round(row["estagio"],2)))
                    temp = temp.replace("Cenario", str(round(row["cenario"],2)))
                    if "patamar" in row:
                        temp = temp.replace("Patamar", str(round(row["patamar"], 2)))
                    else:
                        temp = temp.replace("Patamar", "-")
                    temp = temp.replace("Valor", str(round(valor,2)))
                    self.lista_text.append(temp)
