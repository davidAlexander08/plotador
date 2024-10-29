from typing import List
from os.path import join
import pandas as pd
from inewave.newave import Dger
from apps.utils.log import Log
import os.path
from apps.model.caso import Caso
from apps.indicadores.eco_indicadores import EcoIndicadores
from apps.model.unidade import UnidadeSintese
import warnings
 
class IndicadoresTemporais(EcoIndicadores):
    def __init__(
        self, casos: List[Caso] ):
        warnings.simplefilter(action='ignore')
        
        self.casos = casos
        self.__df_cref = None
        EcoIndicadores.__init__(self, casos)

    
    def retorna_df_concatenado(self, unidade, boxplot):
        return pd.concat(self.retorna_mapaDF_cenario_medio_temporal(unidade, boxplot))
    
    def __retorna_mapa_media_parquet(self, mapa):
        dict = {}
        for c in self.casos:
            df = mapa[c]
            #print(df)
            if(c.modelo == "NEWAVE" or c.modelo == "DECOMP"):
                dict[c] = df.loc[(df["cenario"] == c.tipo) & (df["patamar"] == c.patamar)].reset_index(drop = True)
            if(c.modelo == "DESSEM"):   
                dict[c] = df.reset_index(drop = True) 
        return dict

    #def __retorna_mapa_cenarios_parquet(self, mapa):
    #    dict = {}
    #    for c in self.casos: 
    #        df = mapa[c]
    #        if(c.modelo == "NEWAVE" or c.modelo == "DECOMP"): 
    #            dict[c] = df[df[["cenario"]].apply(lambda x: x[0].isdigit(), axis=1)].reset_index(drop = True)
    #        if(c.modelo == "DESSEM"):   
    #            print("Opcao Boxplot nao pode ser utilizada com modelo DESSEM")
    #            exit(1)
    #    return dict


    def retorna_mapaDF_cenario_medio_temporal(self, unidade, boxplot):
        eco_mapa = self.retornaMapaDF(unidade.sintese.sintese)
        mapa_temporal = {}
        if( (unidade.sintese.filtro is None) & (unidade.filtroArgumento is None) ):
            if(boxplot =="True"):
                return eco_mapa
            else:
                return self.__retorna_mapa_media_parquet(eco_mapa)
        else: 
            mapa_argumentos = self.retornaMapaDF(unidade.sintese.espacial)
            
            coluna_filtro = unidade.sintese.filtro.split("_")[1]
            for c in self.casos:
                cod_arg = mapa_argumentos[c].loc[(mapa_argumentos[c][coluna_filtro] == unidade.filtroArgumento)][unidade.sintese.filtro].iloc[0]
                eco_mapa[c] = eco_mapa[c].loc[eco_mapa[c][unidade.sintese.filtro] == cod_arg]
                
            if(boxplot =="True"):
                mapa_temporal = eco_mapa
            else:
                mapa_temporal = self.__retorna_mapa_media_parquet(eco_mapa)
        return mapa_temporal



    def __gera_df_mean_p10_p90_caso(self,caso, nomeSintese) -> pd.DataFrame:
        caminho_caso = caso.caminho
        arq_sintese = join(
            caminho_caso, self.DIR_SINTESE, f"{nomeSintese}.parquet.gzip"
        )
        dados = pd.read_parquet(arq_sintese)        
        media = dados.loc[dados["cenario"] == "mean", "valor"].to_numpy().flatten() 
        p10 = dados.loc[dados["cenario"] == "p10", "valor"].to_numpy().flatten() 
        p90 = dados.loc[dados["cenario"] == "p90", "valor"].to_numpy().flatten() 
        dataIni = dados.loc[dados["cenario"] == "mean"]["dataInicio"].reset_index(drop=True)
        
        df = pd.DataFrame()
        df["mean"+caso.nome] = media
        df["p10"+caso.nome] = p10
        df["p90"+caso.nome] = p90
        df["dataInicio"+caso.nome] = dataIni
    
        return df
    
    def gera_df_mean_p10_p90(self, nomeSintese) -> pd.DataFrame:
        Log.log().info("Gerando DataFrame de "+nomeSintese+"_p10_p90_mean")
        df = pd.DataFrame()
        for c in self.casos:
            df_temp = self.__gera_df_mean_p10_p90_caso(c, nomeSintese)
            df["mean"+c.nome] = df_temp["mean"+c.nome]
            df["p10"+c.nome] = df_temp["p10"+c.nome]
            df["p90"+c.nome] = df_temp["p90"+c.nome]
            df["dataInicio"+c.nome] = df_temp["dataInicio"+c.nome]
        return df

    
    @property
    def df_cref(self) -> pd.DataFrame:
        if self.__df_cref is None:
            self.__df_cref = self.__criaCref()
        return self.__df_cref


    def __criaCref(self):
        dict = {'data':[], 
        'BANDEIRA':[],
        'EARPF':[], 
        'GTER':[]        
        } 
        df = pd.DataFrame(dict)
        verde = "VERDE"
        amarelo = "AMARELO"
        vermelho = "VERMELHO"
        coluna = "EARPF"
        colunaterm = "GTER"
        categoria = "BANDEIRA"
        cores = [verde, amarelo, vermelho]
        mapaGTER2020 = {
            verde:10322,
            amarelo:10322,
            vermelho:10322
        }
        mapaGTER2021 = {
            verde:11135,
            amarelo : 15052,
            vermelho : 17684
            
        }
        mapaGTER2022 = {
            verde : 12211,
            amarelo : 16635,
            vermelho : 19199
        }
        mapaGTER2023 = {
            verde : 9385,
            amarelo : 13917,
            vermelho : 18143
        }
        mapaGTER2024 = {
            verde : 9660,
            amarelo : 14549,
            vermelho : 18657
        }
        for cor in cores:
            df.loc[len(df.index)] = [pd.Timestamp("2020-01-01"), cor, 18.2, mapaGTER2020[cor]] 
            df.loc[len(df.index)] = [pd.Timestamp("2020-02-01"), cor, 27.3, mapaGTER2020[cor]] 
            df.loc[len(df.index)] = [pd.Timestamp("2020-03-01"), cor, 35.5, mapaGTER2020[cor]] 
            df.loc[len(df.index)] = [pd.Timestamp("2020-04-01"), cor, 39.9, mapaGTER2020[cor]] 
            df.loc[len(df.index)] = [pd.Timestamp("2020-05-01"), cor, 42.0, mapaGTER2020[cor]] 
            df.loc[len(df.index)] = [pd.Timestamp("2020-06-01"), cor, 42.8, mapaGTER2020[cor]] 
            df.loc[len(df.index)] = [pd.Timestamp("2020-07-01"), cor, 40.5, mapaGTER2020[cor]] 
            df.loc[len(df.index)] = [pd.Timestamp("2020-08-01"), cor, 33.2, mapaGTER2020[cor]] 
            df.loc[len(df.index)] = [pd.Timestamp("2020-09-01"), cor, 23.6, mapaGTER2020[cor]] 
            df.loc[len(df.index)] = [pd.Timestamp("2020-10-01"), cor, 18.2, mapaGTER2020[cor]] 
            df.loc[len(df.index)] = [pd.Timestamp("2020-11-01"), cor, 14.3, mapaGTER2020[cor]] 
            df.loc[len(df.index)] = [pd.Timestamp("2020-12-01"), cor, 15.8, mapaGTER2020[cor]]  

        df.loc[len(df.index)] = [pd.Timestamp("2021-01-01"), verde, 28, mapaGTER2021[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-02-01"), verde, 31, mapaGTER2021[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-03-01"), verde, 42, mapaGTER2021[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-04-01"), verde, 49, mapaGTER2021[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-05-01"), verde, 53, mapaGTER2021[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-06-01"), verde, 53, mapaGTER2021[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-07-01"), verde, 51, mapaGTER2021[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-08-01"), verde, 45, mapaGTER2021[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-09-01"), verde, 37, mapaGTER2021[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-10-01"), verde, 29, mapaGTER2021[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-11-01"), verde, 25, mapaGTER2021[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-12-01"), verde, 22, mapaGTER2021[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-01-01"), amarelo, 27, mapaGTER2021[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-02-01"), amarelo, 27, mapaGTER2021[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-03-01"), amarelo, 35, mapaGTER2021[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-04-01"), amarelo, 42, mapaGTER2021[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-05-01"), amarelo, 45, mapaGTER2021[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-06-01"), amarelo, 46, mapaGTER2021[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-07-01"), amarelo, 45, mapaGTER2021[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-08-01"), amarelo, 40, mapaGTER2021[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-09-01"), amarelo, 33, mapaGTER2021[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-10-01"), amarelo, 26, mapaGTER2021[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-11-01"), amarelo, 24, mapaGTER2021[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-12-01"), amarelo, 22, mapaGTER2021[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-01-01"), vermelho, 25, mapaGTER2021[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-02-01"), vermelho, 25, mapaGTER2021[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-03-01"), vermelho, 32, mapaGTER2021[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-04-01"), vermelho, 39, mapaGTER2021[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-05-01"), vermelho, 42, mapaGTER2021[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-06-01"), vermelho, 43, mapaGTER2021[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-07-01"), vermelho, 42, mapaGTER2021[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-08-01"), vermelho, 37, mapaGTER2021[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-09-01"), vermelho, 31, mapaGTER2021[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-10-01"), vermelho, 25, mapaGTER2021[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-11-01"), vermelho, 23, mapaGTER2021[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2021-12-01"), vermelho, 22, mapaGTER2021[vermelho]] 

        df.loc[len(df.index)] = [pd.Timestamp("2022-01-01"), verde,    36.0, mapaGTER2022[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-02-01"), verde,    41.5, mapaGTER2022[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-03-01"), verde,    48.6, mapaGTER2022[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-04-01"), verde,    57.2, mapaGTER2022[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-05-01"), verde,    58.1, mapaGTER2022[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-06-01"), verde,    57.7, mapaGTER2022[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-07-01"), verde,    56.0, mapaGTER2022[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-08-01"), verde,    51.6, mapaGTER2022[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-09-01"), verde,    44.7, mapaGTER2022[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-10-01"), verde,    38.3, mapaGTER2022[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-11-01"), verde,    29.1, mapaGTER2022[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-12-01"), verde,    21.3, mapaGTER2022[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-01-01"), amarelo,  21.7, mapaGTER2022[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-02-01"), amarelo,  27.3, mapaGTER2022[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-03-01"), amarelo,  34.9, mapaGTER2022[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-04-01"), amarelo,  44.5, mapaGTER2022[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-05-01"), amarelo,  46.3, mapaGTER2022[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-06-01"), amarelo,  46.4, mapaGTER2022[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-07-01"), amarelo,  45.6, mapaGTER2022[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-08-01"), amarelo,  42.4, mapaGTER2022[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-09-01"), amarelo,  37.2, mapaGTER2022[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-10-01"), amarelo,  32.5, mapaGTER2022[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-11-01"), amarelo,  25.4, mapaGTER2022[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-12-01"), amarelo,  21.3, mapaGTER2022[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-01-01"), vermelho, 21.7, mapaGTER2022[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-02-01"), vermelho, 22.3, mapaGTER2022[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-03-01"), vermelho, 30.1, mapaGTER2022[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-04-01"), vermelho, 39.8, mapaGTER2022[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-05-01"), vermelho, 41.6, mapaGTER2022[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-06-01"), vermelho, 41.7, mapaGTER2022[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-07-01"), vermelho, 41.2, mapaGTER2022[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-08-01"), vermelho, 39.0, mapaGTER2022[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-09-01"), vermelho, 34.8, mapaGTER2022[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-10-01"), vermelho, 30.6, mapaGTER2022[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-11-01"), vermelho, 24.6, mapaGTER2022[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2022-12-01"), vermelho, 21.3, mapaGTER2022[vermelho]] 


        df.loc[len(df.index)] = [pd.Timestamp("2023-01-01"), verde,    39.5, mapaGTER2023[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-02-01"), verde,    45.0, mapaGTER2023[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-03-01"), verde,    51.8, mapaGTER2023[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-04-01"), verde,    58.6, mapaGTER2023[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-05-01"), verde,    58.6, mapaGTER2023[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-06-01"), verde,    56.9, mapaGTER2023[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-07-01"), verde,    54.4, mapaGTER2023[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-08-01"), verde,    50.0, mapaGTER2023[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-09-01"), verde,    43.5, mapaGTER2023[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-10-01"), verde,    37.6, mapaGTER2023[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-11-01"), verde,    28.7, mapaGTER2023[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-12-01"), verde,    21.4, mapaGTER2023[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-01-01"), amarelo,  28.1, mapaGTER2023[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-02-01"), amarelo,  34.3, mapaGTER2023[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-03-01"), amarelo,  42.0, mapaGTER2023[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-04-01"), amarelo,  49.7, mapaGTER2023[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-05-01"), amarelo,  50.2, mapaGTER2023[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-06-01"), amarelo,  48.9, mapaGTER2023[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-07-01"), amarelo,  46.6, mapaGTER2023[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-08-01"), amarelo,  43.0, mapaGTER2023[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-09-01"), amarelo,  38.2, mapaGTER2023[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-10-01"), amarelo,  33.0, mapaGTER2023[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-11-01"), amarelo,  25.9, mapaGTER2023[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-12-01"), amarelo,  21.4, mapaGTER2023[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-01-01"), vermelho, 21.9, mapaGTER2023[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-02-01"), vermelho, 24.6, mapaGTER2023[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-03-01"), vermelho, 32.9, mapaGTER2023[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-04-01"), vermelho, 41.3, mapaGTER2023[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-05-01"), vermelho, 42.7, mapaGTER2023[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-06-01"), vermelho, 42.1, mapaGTER2023[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-07-01"), vermelho, 40.5, mapaGTER2023[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-08-01"), vermelho, 37.8, mapaGTER2023[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-09-01"), vermelho, 33.9, mapaGTER2023[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-10-01"), vermelho, 29.4, mapaGTER2023[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-11-01"), vermelho, 23.8, mapaGTER2023[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2023-12-01"), vermelho, 21.4, mapaGTER2023[vermelho]] 

        df.loc[len(df.index)] = [pd.Timestamp("2024-01-01"), verde,    29, mapaGTER2024[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-02-01"), verde,    35, mapaGTER2024[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-03-01"), verde,    43, mapaGTER2024[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-04-01"), verde,    49, mapaGTER2024[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-05-01"), verde,    51, mapaGTER2024[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-06-01"), verde,    50, mapaGTER2024[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-07-01"), verde,    48, mapaGTER2024[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-08-01"), verde,    45, mapaGTER2024[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-09-01"), verde,    41, mapaGTER2024[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-10-01"), verde,    36, mapaGTER2024[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-11-01"), verde,    31, mapaGTER2024[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-12-01"), verde,    28, mapaGTER2024[verde]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-01-01"), amarelo,  26, mapaGTER2024[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-02-01"), amarelo,  30, mapaGTER2024[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-03-01"), amarelo,  38, mapaGTER2024[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-04-01"), amarelo,  44, mapaGTER2024[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-05-01"), amarelo,  46, mapaGTER2024[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-06-01"), amarelo,  46, mapaGTER2024[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-07-01"), amarelo,  44, mapaGTER2024[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-08-01"), amarelo,  40, mapaGTER2024[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-09-01"), amarelo,  36, mapaGTER2024[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-10-01"), amarelo,  31, mapaGTER2024[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-11-01"), amarelo,  27, mapaGTER2024[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-12-01"), amarelo,  25, mapaGTER2024[amarelo]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-01-01"), vermelho, 22, mapaGTER2024[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-02-01"), vermelho, 26, mapaGTER2024[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-03-01"), vermelho, 31, mapaGTER2024[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-04-01"), vermelho, 37, mapaGTER2024[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-05-01"), vermelho, 40, mapaGTER2024[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-06-01"), vermelho, 40, mapaGTER2024[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-07-01"), vermelho, 39, mapaGTER2024[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-08-01"), vermelho, 36, mapaGTER2024[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-09-01"), vermelho, 32, mapaGTER2024[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-10-01"), vermelho, 28, mapaGTER2024[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-11-01"), vermelho, 23, mapaGTER2024[vermelho]] 
        df.loc[len(df.index)] = [pd.Timestamp("2024-12-01"), vermelho, 21, mapaGTER2024[vermelho]] 
        
        return df
