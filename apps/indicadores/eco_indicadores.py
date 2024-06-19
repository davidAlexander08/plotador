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
        
    def stub(self,df,caso):  ## REGRAS ADICIONAIS QUE VARIAM POR MODELO
        return df

    def __retorna_df(self, caso, sintese) -> pd.DataFrame:
        arq_sintese = join( caso.caminho, self.DIR_SINTESE, sintese+".parquet.gzip"  )
        check_file = os.path.isfile(arq_sintese)
        if(check_file) :
            df = pd.read_parquet(arq_sintese)
            df = stub(df, caso)
            return df
        else:
            raise FileNotFoundError(f"Arquivo {arq_sintese} não encontrado. Caminho pode estar errado") 
            print(check_file)
            df_vazio = pd.DataFrame()
            return df_vazio
            
    def retornaMapaDF(self, sintese):
        dict = {}
        for c in self.casos:
            df = self.__retorna_df(c, sintese)
            df["caso"] = c.nome
            df["modelo"] = c.modelo
            dict[c] = df
        return dict



    def exportar(self, df, diretorio_saida, nome_arquivo, imprimeIndex = False):
        Log.log().info("Gerando tabela "+nome_arquivo)
        df.to_csv( os.path.join(diretorio_saida, 
                                nome_arquivo+".csv"), 
                  index= imprimeIndex )





