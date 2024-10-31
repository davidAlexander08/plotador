from typing import List
from os.path import join
import pandas as pd
from apps.utils.log import Log
import os.path
from apps.model.caso import Caso
from apps.indicadores.abstractIndicadores import AbstractIndicadores
import warnings

class EcoIndicadores:

    def __init__(  self, casos: List[Caso] ):
        warnings.simplefilter(action='ignore')
        self.casos = casos
        AbstractIndicadores.__init__(self)
        
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
        for c in self.casos:            
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





