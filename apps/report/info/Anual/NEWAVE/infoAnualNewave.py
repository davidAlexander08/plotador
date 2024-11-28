
from apps.report.info.Anual.NEWAVE.estruturas import Estruturas
from inewave.newave import Dger
import os
import pandas as pd

class InfoAnualNewave(Estruturas):
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

            anos = df_caso["data_inicio"].dt.year.unique().tolist()
            unique_years.update(anos)
        self.unique_years = unique_years
        for year in unique_years:
            self.Tabela_Eco_Entrada += f'<th>{year}</th>\n'
            self.template_Tabela_Eco_Entrada += f'<td>{year}</td>\n'
        self.Tabela_Eco_Entrada += f'</tr> \n'
        self.template_Tabela_Eco_Entrada += f'</tr> \n'


        self.lista_text = []
        grandeza = par_dados[2]
        argumentos = par_dados [1]
        posnw = par_dados[3]

        for arg in argumentos:
            if(arg == ""):
                arg = "SIN"
            #self.lista_text.append("<h3>Dados "+arg+"</h3>")
            #self.lista_text.append("<h3>Dados "+arg+"</h3>")
            temp = self.Tabela_Eco_Entrada
            temp = temp.replace("Caso", arg)
            self.lista_text.append(temp)
            #self.lista_text.append(self.Tabela_Eco_Entrada)

            for caso in data.conjuntoCasos[0].casos:
                if(caso.modelo == "NEWAVE"):
                    temp = self.preenche_modelo_tabela_modelo_NEWAVE(caso, arg, grandeza, posnw)
                    self.lista_text.append(temp)
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
            
            if(posnw == "True"):
                dados_dger = Dger.read(caso.caminho+"/dger.dat")
                anos_estudo = dados_dger.num_anos_estudo
                mes_inicial = dados_dger.mes_inicio_estudo
                periodos_estudo = anos_estudo*12 - mes_inicial + 1
                oper_mean = oper_mean.loc[(oper_mean["estagio"] <= periodos_estudo)]


            for year in self.unique_years:
                media_ano = oper_mean.loc[(oper_mean["data_inicio"].dt.year == year) & (oper_mean["variavel"] == tipo)]["valor"].mean()
                temp = temp.replace(str(year), str(round(media_ano,2)))

        return temp
