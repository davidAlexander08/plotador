from typing import List
from os.path import join
import pandas as pd
from apps.utils.log import Log
import os
from apps.model.caso import Caso 
from apps.indicadores.abstractIndicadores import AbstractIndicadores
import warnings

class EcoIndicadores:

    def __init__(  self, casos: List[Caso] ):
        warnings.simplefilter(action='ignore')
        self.casos = casos
        AbstractIndicadores.__init__(self)
        self.mapa_arquivos = {
            "GTER_SIN":"gttotsin.out",
            "EARPF_SIN":"earmfsin.out",
            "EARMF_SIN":"earmfpsin.out"
        }
        
    def retorna_df_concatenado(self,sintese):
        return pd.concat(self.retornaMapaDF(sintese))

    def retorna_df(self, caso, sintese) -> pd.DataFrame:
        arq_sintese = join( caso.caminho, self.DIR_SINTESE, sintese+".parquet"  )
        #check_file = os.path.isfile(arq_sintese)
        try:
            df = pd.read_parquet(arq_sintese, engine = "pyarrow")
            return df
        except:
            raise FileNotFoundError(f"Arquivo {arq_sintese} não encontrado. Caminho pode estar errado.")

            
    def retornaMapaDF(self, sintese):
        result_dict  = {}
        sintese_parts = sintese.split("_")
        variavel = sintese_parts[0]
        flag_estatistica = 0
        print("SINTESE")
        for c in self.casos:
            if(os.path.isfile(c.caminho+"/sintese/"+sintese+".parquet")):
                print("ENCNTROU")
                #if( (len(sintese_parts) > 1) and (variavel != "ESTATISTICAS") and (variavel != "METADADOS") ):
                if len(sintese_parts) > 1 and variavel not in ("ESTATISTICAS", "METADADOS") :
                    if(self.checkIfNumberOnly(c.tipo)):
                        c.tipo = int(c.tipo)
                        sintese_busca = sintese
                    else:
                        sintese_busca = "ESTATISTICAS_OPERACAO_"+sintese.split("_")[1]
                        flag_estatistica = 1
                else:
                    sintese_busca = sintese
                #df = self.retorna_df(c, sintese_busca).copy()
                df = self.retorna_df(c, sintese_busca)
                #if(flag_estatistica == 1):
                if(flag_estatistica):
                    #df = df.loc[(df["variavel"] == variavel)].copy() 
                    df = df.loc[(df["variavel"] == variavel)]                   
                df["caso"] = c.nome
                df["modelo"] = c.modelo
                result_dict [c] = df
                print(df)
            else:                    
                if(sintese in self.mapa_arquivos.keys()):
                    #try:
                    arquivo = self.mapa_arquivos[sintese]
                    caminho_arquivo = c.caminho+"/"+arquivo
                    media_values = []
                    estagios = []
                    with open(caminho_arquivo, 'r') as file:
                        for line in file:
                            inicio = line[0:10].split()
                            if("MEDIA" in inicio):
                                temp = []
                                temp = [float(value) for value in line.split()[1:]]
                                temp.pop()
                                media_values = media_values + temp
                    estagios = list(range(1, len(media_values) + 1))
                    print(estagios)

                    dicionario = {
                        "valor":media_values,
                        "estagio":estagios
                    }
                    df = pd.DataFrame(dicionario)
                    df["cenario"] = "mean"
                    df["patamar"] = 0
                    df["limite_superior"] = 0
                    df["limite_inferior"] = 0
                    df["caso"] = c.nome
                    df["modelo"] = c.modelo
                    df["codigo_usina"] = None
                    df["codigo_ree"] = None
                    df["codigo_submercado"] = None
                    df["variavel"] = sintese.split("_")[0]

                    print(df)

                    start_date = "2024-08-01"
                    num_months = 72  # Change this to your desired number
                    date_range = pd.date_range(start=start_date, periods=num_months, freq='MS', tz='UTC')
                    df = pd.DataFrame({'Timestamp': date_range})
                    print(df)



                    exit(1)
                    media_values = [float(value) for value in media_values]
                    print(media_values)

                    exit(1)
                    #except Exception as e:  
                    #    print("NAO EXISTE SINTESE: ", sintese, " NO CAMINHO: ", c.caminho)


        return result_dict 



    def checkIfNumberOnly(self,s):
        try:
            float(s)  # Check if string can be converted to a float
            return True
        except ValueError:
            return False

    def exportar(self, df, diretorio_saida, nome_arquivo, imprimeIndex = False):
        Log.log().info("Gerando tabela "+nome_arquivo)
        df.to_csv( os.path.join(diretorio_saida, 
                                nome_arquivo+".csv"), 
                  index= imprimeIndex )





