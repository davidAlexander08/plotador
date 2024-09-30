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
        
    #def stub(self,df,caso, sintese):  ## REGRAS ADICIONAIS QUE VARIAM POR MODELO
    #    if (caso.modelo == "NEWAVE" and sintese == "VAGUA_UHE_EST"):
    #        df["valor"] = df["valor"]/1000
    #    return df

    def retorna_df(self, caso, sintese) -> pd.DataFrame:
        arq_sintese = join( caso.caminho, self.DIR_SINTESE, sintese+".parquet"  )
        check_file = os.path.isfile(arq_sintese)
        if(check_file) :
            df = pd.read_parquet(arq_sintese)
    #        df = self.stub(df, caso, sintese)
            return df
        else:
            raise FileNotFoundError(f"Arquivo {arq_sintese} não encontrado. Caminho pode estar errado") 
            print(check_file)
            df_vazio = pd.DataFrame()
            return df_vazio
            
    def retornaMapaDF(self, sintese):
        dict = {}
        variavel = sintese.split("_")[0]
        print("variavel: ", variavel)
        for c in self.casos:            
            if( (len(sintese.split("_")) > 1) and (variavel != "ESTATISTICAS") and (variavel != "METADADOS") ):
                if(self.checkIfNumberOnly(c.tipo)):
                    c.tipo = int(c.tipo)
                    sintese_busca = sintese
                else:
                    sintese_busca = "ESTATISTICAS_OPERACAO_"+sintese.split("_")[1]
            else:
                sintese_busca = sintese
            print("SINTESE BUSCA: ", sintese_busca)
            df = self.retorna_df(c, sintese_busca)

            if( (len(sintese.split("_")) > 1) and (variavel != "ESTATISTICAS") and (variavel != "METADADOS") ):
                if(self.checkIfNumberOnly(c.tipo)):
                    pass
                else:
                    df = df.loc[(df["variavel"] == variavel)]

            print(df)
            df["caso"] = c.nome
            df["modelo"] = c.modelo
            dict[c] = df
        return dict

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





