from typing import List
from os.path import join
from datetime import datetime
from calendar import monthrange
import numpy as np
import pandas as pd
from inewave.newave import Dger
from apps.utils.log import Log
import os.path
from apps.calibracao_cvar.caso import CasoCalibracaoCVAR
from apps.calibracao_cvar.usina import UsinaAvalicao
import warnings

class IndicadoresCalibracaoCVAR_Violacao:
    """indicadores.df_custos_incrementais.to_csv
    Calcula os indicadores que são utilizados nas visualizações
    dos paretos para a escolha dos pares de CVaR candidatos
    para recalibração.
    """

    DIR_SINTESE = "sintese"

    def __init__(
        self, casos: List[CasoCalibracaoCVAR], nome_caso_referencia: str, usinas: List[UsinaAvalicao]
    ):
        warnings.simplefilter(action='ignore')
        
        self.casos = casos
        self.usinas = usinas
        self.nome_caso_referencia = nome_caso_referencia
        self.__df_viol_usinas = None
        self.__df_viol_usinas_mean = None
        self.__df_viol_usinas_mean_mean = None
        self.__df_viol_usinas_mean_anual = None
        self.__df_viol_usina_primeiro_ano_media_outros_anos = None
        self.__df_viol_incrementais_usinas_medio_medio = None
        self.__df_viol_incrementais_usinas_medios_anuais = None
        self.__df_viol_incrementais_usinas_primeiro_ano_media_outros_anos = None

        self.__df_viol_SIN = None
        self.__df_viol_SIN_mean = None
        self.__df_viol_SIN_mean_mean = None
        self.__df_viol_SIN_mean_anual = None
        self.__df_viol_SIN_primeiro_ano_media_outros_anos = None
        self.__df_viol_incrementais_SIN_medio_medio = None
        self.__df_viol_incrementais_SIN_medios_anuais = None
        self.__df_viol_incrementais_SIN_primeiro_ano_media_outros_anos = None


 
    @property
    def df_viol_usinas(self) -> pd.DataFrame:
        if(self.__df_viol_usinas is None):
            self.__gera_df_viol_usinas()
        return self.__df_viol_usinas
    @property
    def df_viol_usinas_mean (self) -> pd.DataFrame:
        if(self.__df_viol_usinas_mean is None):
            self.__gera_df_viol_usinas()
        return self.__df_viol_usinas_mean
    @property
    def df_viol_usinas_mean_mean(self) -> pd.DataFrame:
        if(self.__df_viol_usinas_mean_mean is None):
            self.__gera_df_viol_usinas()
        return self.__df_viol_usinas_mean_mean
    @property
    def df_viol_usinas_mean_anual(self) -> pd.DataFrame:
        if(self.__df_viol_usinas_mean_anual is None):
            self.__gera_df_viol_usinas()
        return self.__df_viol_usinas_mean_anual
    @property
    def df_viol_usina_primeiro_ano_media_outros_anos(self) -> pd.DataFrame:
        if(self.__df_viol_usina_primeiro_ano_media_outros_anos is None):
            self.__gera_df_viol_usinas()
        return self.__df_viol_usina_primeiro_ano_media_outros_anos


    @property
    def df_viol_SIN(self) -> pd.DataFrame:
        if(self.__df_viol_SIN is None):
            self.__gera_df_viol_SIN()
        return self.__df_viol_SIN
    @property
    def df_viol_SIN_mean (self) -> pd.DataFrame:
        if(self.__df_viol_SIN_mean is None):
            self.__gera_df_viol_SIN()
        return self.__df_viol_SIN_mean
    @property
    def df_viol_SIN_mean_mean(self) -> pd.DataFrame:
        if(self.__df_viol_SIN_mean_mean is None):
            self.__gera_df_viol_SIN()
        return self.__df_viol_SIN_mean_mean
    @property
    def df_viol_SIN_mean_anual(self) -> pd.DataFrame:
        if(self.__df_viol_SIN_mean_anual is None):
            self.__gera_df_viol_SIN()
        return self.__df_viol_SIN_mean_anual

    @property
    def df_viol_SIN_primeiro_ano_media_outros_anos(self) -> pd.DataFrame:
        if(self.__df_viol_SIN_primeiro_ano_media_outros_anos is None):
            self.__gera_df_viol_SIN()
        return self.__df_viol_SIN_primeiro_ano_media_outros_anos


    def __retorna_df(self, caso, sintese) -> pd.DataFrame:
        caminho_caso = caso.caminho
        arq_sintese = join(
            caminho_caso, self.DIR_SINTESE, sintese+".parquet.gzip"
        )
        check_file = os.path.isfile(arq_sintese)
        if(check_file) :
            df = pd.read_parquet(arq_sintese)
            return df
        else:
            #print("CASO: ", caso.nome, " NAO POSSUI A SINTESE: ", sintese)
            df_vazio = pd.DataFrame()
            return df_vazio

    def __gera_df_viol_SIN(self) -> pd.DataFrame:
        Log.log().info("Gerando DataFrame de custos de violação de Usinas")
        listaDF = []
        lista_caso_sintese_SIN = []
        lista_caso_sintese_SIN_mean_mean = []
        lista_caso_sintese_SIN_mean_anual = []
        
        for caso in self.casos:
            df_VDEFMIN_SIN_EST = self.__retorna_df(caso, "VDEFMIN_SIN_EST")
            df_VDEFMIN_SIN_EST["valor"] = df_VDEFMIN_SIN_EST["valor"]*0
            df_VDEFMIN_SIN_mean = df_VDEFMIN_SIN_EST.loc[(df_VDEFMIN_SIN_EST["cenario"] == "mean")].reset_index(drop=True)
            df_VDEFMIN_SIN_mean["valor"] = df_VDEFMIN_SIN_mean["valor"]*0
            df_VDEFMIN_PAT = self.__retorna_df(caso,"VDEFMIN_UHE_PAT")
            df_VDEFMIN_PAT["valor"] = df_VDEFMIN_PAT["valor"]*2.63
            usinas = df_VDEFMIN_PAT["usina"].unique()

            df_VDEFMIN_SIN_PAT = pd.DataFrame()
            df_VDEFMIN_SIN_PAT = df_VDEFMIN_PAT.loc[(df_VDEFMIN_PAT["usina"] == "JUPIA")].drop(['usina'], axis=1).reset_index(drop=True)
            df_VDEFMIN_SIN_PAT["valor"] = df_VDEFMIN_SIN_PAT["valor"]*0
            for usi in usinas:
                df_teste = df_VDEFMIN_PAT.loc[(df_VDEFMIN_PAT["usina"] == usi)].reset_index(drop=True)
                df_VDEFMIN_SIN_PAT["valor"] += df_teste["valor"]

            df_VDEFMIN_SIN_PAT.to_csv("df_VDEFMIN_SIN_PAT.csv")
                    
            patamares = df_VDEFMIN_SIN_PAT["patamar"].unique()           
            for pat in patamares:
                df_temp = df_VDEFMIN_SIN_PAT.loc[(df_VDEFMIN_SIN_PAT["patamar"] == pat)].reset_index(drop = True)
                df_VDEFMIN_SIN_EST["valor"] += df_temp["valor"]
            df_VDEFMIN_SIN_EST = df_VDEFMIN_SIN_EST[df_VDEFMIN_SIN_EST[['cenario']].apply(lambda x: x[0].isdigit(), axis=1)]

            for index, row in df_VDEFMIN_SIN_mean.iterrows():
                df_temp = df_VDEFMIN_SIN_EST.loc[(df_VDEFMIN_SIN_EST["estagio"] == row["estagio"])].reset_index(drop = True)
                df_VDEFMIN_SIN_mean.at[index,"valor"] = df_temp["valor"].mean()

            
            df_VDEFMIN_SIN_mean["valor"]  = df_VDEFMIN_SIN_mean["valor"].round(2)
            df_VDEFMIN_SIN_mean["caso"] = caso.nome
            lista_caso_sintese_SIN.append(df_VDEFMIN_SIN_mean)   
            
            caso_sintese_SIN_mean_mean = pd.DataFrame()
            caso_sintese_SIN_media_anual = pd.DataFrame()
            #df_VDEFMIN = df_VDEFMIN[df_VDEFMIN[['cenario']].apply(lambda x: x[0].isdigit(), axis=1)]
            
            caso_sintese_SIN_mean_mean.at[caso.nome,"Viol Def Min"] =  df_VDEFMIN_SIN_mean["valor"].mean()
            caso_sintese_SIN_mean_mean["caso"] = caso.nome
            lista_caso_sintese_SIN_mean_mean.append(caso_sintese_SIN_mean_mean)
            
            caso_sintese_SIN_media_anual["Viol Def Min"] = df_VDEFMIN_SIN_mean.groupby(df_VDEFMIN_SIN_mean["dataInicio"].dt.year)["valor"].agg(["mean"])
            caso_sintese_SIN_media_anual["caso"] = caso.nome
            lista_caso_sintese_SIN_mean_anual.append(caso_sintese_SIN_media_anual)

 
        self.__df_viol_SIN = pd.concat(lista_caso_sintese_SIN).reset_index(drop=True)
        self.__df_viol_SIN_mean_mean = pd.concat(lista_caso_sintese_SIN_mean_mean).reset_index(drop=True)
        self.__df_viol_SIN_mean_anual = pd.concat(lista_caso_sintese_SIN_mean_anual).reset_index(drop=False)
        self.__df_viol_SIN_mean_anual.columns = self.__df_viol_SIN_mean_anual.columns.str.replace('dataInicio', 'anos')   

        anos = set(self.__df_viol_SIN_mean_anual["anos"].tolist())
        listaDF = []
        df_primeiro = self.__df_viol_SIN_mean_anual.loc[self.__df_viol_SIN_mean_anual["anos"] == min(anos)]
        df_outros = self.__df_viol_SIN_mean_anual.loc[self.__df_viol_SIN_mean_anual["anos"] != min(anos)]
        casos = set(df_outros["caso"].tolist())
        df_temp = pd.DataFrame()
        for caso in casos:
            df_outros_caso = df_outros.loc[ df_outros["caso"] == caso ]
            df_outros_caso = df_outros_caso.reset_index(drop = True)
            df_temp.at[caso, "Viol Def Min"] = df_outros_caso["Viol Def Min"].mean()
            anoInicial = df_outros_caso["anos"].iloc[0]
            anoFinal = df_outros_caso["anos"].iloc[-1]
            df_temp.at[caso, "anos"] = str(anoInicial)+"-"+str(anoFinal)
        df_temp.index.name = "caso"    
        df_temp = df_temp.reset_index(drop = False)
        listaDF.append(df_temp)
        df_primeiro["anos"] = df_primeiro["anos"].astype(str)
        listaDF.append(df_primeiro)
        self.__df_viol_SIN_primeiro_ano_media_outros_anos = pd.concat(listaDF)
        self.__df_viol_SIN_primeiro_ano_media_outros_anos = self.__df_viol_SIN_primeiro_ano_media_outros_anos.reset_index(drop = True)
            
        #print(self.__df_viol_SIN_mean_mean)
        #print(self.__df_viol_SIN_mean_anual)
        #print(self.__df_viol_SIN_primeiro_ano_media_outros_anos)

        return 0
    

    
    def __gera_df_viol_usinas(self) -> pd.DataFrame:
        Log.log().info("Gerando DataFrame de custos de violação de Usinas")
        listaDF = []
        lista_caso_sintese_usina = []
        lista_caso_sintese_usina_mean_mean = []
        lista_caso_sintese_usina_mean_anual = []
        
        for caso in self.casos:
            df_VDEFMIN_PAT = self.__retorna_df(caso,"VDEFMIN_UHE_PAT")
            df_GHMIN = self.__retorna_df(caso,"VGHMIN_UHE_EST")
            df_VDEFMIN = self.__retorna_df(caso,"VDEFMIN_UHE_EST")
            
            for u in self.usinas:
                df_VDEFMIN_usi_pat = df_VDEFMIN_PAT.loc[(df_VDEFMIN_PAT["usina"] == u.nome)].reset_index(drop=True)
                df_VDEFMIN_usi_pat["valor"] = df_VDEFMIN_usi_pat["valor"]*2.63


            
                patamares = df_VDEFMIN_usi_pat["patamar"].unique()
                df_VDEFMIN_usi_est = df_VDEFMIN.loc[(df_VDEFMIN["usina"] == u.nome)].reset_index(drop=True)
                df_VDEFMIN_usi_mean = df_VDEFMIN_usi_est.loc[(df_VDEFMIN_usi_est["cenario"] == "mean")].reset_index(drop=True)
                df_VDEFMIN_usi_mean["valor"] = df_VDEFMIN_usi_mean["valor"]*0
                df_VDEFMIN_usi_est["valor"] = df_VDEFMIN_usi_est["valor"]*0
                
                
                for pat in patamares:
                    df_temp = df_VDEFMIN_usi_pat.loc[(df_VDEFMIN_usi_pat["patamar"] == pat)].reset_index(drop = True)
                    df_VDEFMIN_usi_est["valor"] += df_temp["valor"]
                df_VDEFMIN_usi_est = df_VDEFMIN_usi_est[df_VDEFMIN_usi_est[['cenario']].apply(lambda x: x[0].isdigit(), axis=1)]


                
                for index, row in df_VDEFMIN_usi_mean.iterrows():
                    df_temp = df_VDEFMIN_usi_est.loc[(df_VDEFMIN_usi_est["estagio"] == row["estagio"])].reset_index(drop = True)
                    df_VDEFMIN_usi_mean.at[index,"valor"] = df_temp["valor"].mean()

                df_VGHMIN_usi_mean = df_GHMIN.loc[(df_GHMIN["usina"] == u.nome) & (df_GHMIN["cenario"] == "mean")].reset_index(drop=True)
 
                caso_sintese_usina = pd.DataFrame()
                caso_sintese_usina_mean_mean = pd.DataFrame()
                caso_sintese_usina_media_anual = pd.DataFrame()
                
                caso_sintese_usina["dataInicio"] = df_VDEFMIN_usi_mean["dataInicio"] 
                caso_sintese_usina["estagio"] = df_VDEFMIN_usi_mean["estagio"]
                caso_sintese_usina["cenario"] = df_VDEFMIN_usi_mean["cenario"]
                caso_sintese_usina["caso"] = caso.nome
                caso_sintese_usina["usina"] = u.nome
                caso_sintese_usina["Viol Def Min"] = df_VDEFMIN_usi_mean["valor"]
                caso_sintese_usina["Viol GH Min"] = df_VGHMIN_usi_mean["valor"]
                lista_caso_sintese_usina.append(caso_sintese_usina)

                caso_sintese_usina_mean_mean.at[caso.nome,"Viol Def Min"] =  df_VDEFMIN_usi_mean["valor"].mean()
                caso_sintese_usina_mean_mean.at[caso.nome,"Viol GH Min"] =  df_VGHMIN_usi_mean["valor"].mean()
                caso_sintese_usina_mean_mean["usina"] = u.nome
                caso_sintese_usina_mean_mean["caso"] = caso.nome
                lista_caso_sintese_usina_mean_mean.append(caso_sintese_usina_mean_mean)
                #print(lista_caso_sintese_usina_mean_mean)
                caso_sintese_usina_media_anual["Viol Def Min"] = df_VDEFMIN_usi_mean.groupby(df_VDEFMIN_usi_mean["dataInicio"].dt.year)["valor"].agg(['mean'])
                caso_sintese_usina_media_anual["Viol GH Min"] = df_VGHMIN_usi_mean.groupby(df_VGHMIN_usi_mean["dataInicio"].dt.year)["valor"].agg(['mean'])
                caso_sintese_usina_media_anual["usina"] = u.nome
                caso_sintese_usina_media_anual["caso"] = caso.nome
                lista_caso_sintese_usina_mean_anual.append(caso_sintese_usina_media_anual)
                #print(lista_caso_sintese_usina_mean_anual)
        self.__df_viol_usinas = pd.concat(lista_caso_sintese_usina).reset_index(drop=True)
        self.__df_viol_usinas_mean_mean = pd.concat(lista_caso_sintese_usina_mean_mean).reset_index(drop=True)
        self.__df_viol_usinas_mean_anual = pd.concat(lista_caso_sintese_usina_mean_anual).reset_index(drop=False)
        self.__df_viol_usinas_mean_anual.columns = self.__df_viol_usinas_mean_anual.columns.str.replace('dataInicio', 'anos') 

        #print(self.__df_viol_usinas_mean_anual)
        
        anos = set(self.__df_viol_usinas_mean_anual["anos"].tolist())
        #print(anos)
        listaDF = []
        for u in self.usinas:
            df_usina = self.__df_viol_usinas_mean_anual.loc[(self.__df_viol_usinas_mean_anual["usina"] == u.nome)]                
            df_primeiro = df_usina.loc[df_usina["anos"] == min(anos)]
            df_outros = df_usina.loc[df_usina["anos"] != min(anos)]
            casos = set(df_outros["caso"].tolist())
            
            df_temp = pd.DataFrame()
            for caso in casos:
                df_outros_caso = df_outros.loc[ df_outros["caso"] == caso ]
                df_outros_caso = df_outros_caso.reset_index(drop = True)
                df_temp.at[caso, "Viol Def Min"] = df_outros_caso["Viol Def Min"].mean()
                df_temp.at[caso, "Viol GH Min"] = df_outros_caso["Viol GH Min"].mean()
                anoInicial = df_outros_caso["anos"].iloc[0]
                anoFinal = df_outros_caso["anos"].iloc[-1]
                df_temp.at[caso, "anos"] = str(anoInicial)+"-"+str(anoFinal)
                df_temp.at[caso, "usina"] = u.nome
            df_temp.index.name = "caso"    
            df_temp = df_temp.reset_index(drop = False)
            listaDF.append(df_temp)
            df_primeiro["anos"] = df_primeiro["anos"].astype(str)
            listaDF.append(df_primeiro)
        self.__df_viol_usina_primeiro_ano_media_outros_anos = pd.concat(listaDF)
        self.__df_viol_usina_primeiro_ano_media_outros_anos = self.__df_viol_usina_primeiro_ano_media_outros_anos.reset_index(drop = True)
            
        #print(self.__df_viol_usinas)
        #print(self.__df_viol_usinas_mean_mean)
        #print(self.__df_viol_usinas_mean_anual)
        #print(self.__df_viol_usina_primeiro_ano_media_outros_anos)

        #exit(1)
        return 0
    
    @property
    def df_custos_viol_incrementais_usinas_valores_medios_medios(self)->pd.DataFrame:
        if(self.__df_viol_incrementais_usinas_medio_medio is None):
            self.__retorna_custo_incremental_no_df_custos_USI()
        return self.__df_viol_incrementais_usinas_medio_medio
        
    @property
    def df_custos_viol_incrementais_usinas_valores_medios_anuais(self)->pd.DataFrame:
        if(self.__df_viol_incrementais_usinas_medios_anuais is None):
            self.__retorna_custo_incremental_no_df_custos_USI()
        return self.__df_viol_incrementais_usinas_medios_anuais


    @property
    def df_custos_viol_incrementais_usinas_valores_medios_primeiro_ano_media_outros_anos(self)->pd.DataFrame:
        if(self.__df_viol_incrementais_usinas_primeiro_ano_media_outros_anos is None):
            self.__retorna_custo_incremental_no_df_custos_USI()
        return self.__df_viol_incrementais_usinas_primeiro_ano_media_outros_anos

    @property
    def df_custos_viol_incrementais_SIN_valores_medios_medios(self)->pd.DataFrame:
        if(self.__df_viol_incrementais_SIN_medio_medio is None):
            self.__retorna_custo_incremental_viol_SIN()
        return self.__df_viol_incrementais_SIN_medio_medio
    @property
    def df_custos_viol_incrementais_SIN_valores_medios_anuais(self)->pd.DataFrame:
        if(self.__df_viol_incrementais_SIN_medios_anuais is None):
            self.__retorna_custo_incremental_viol_SIN()

        return self.__df_viol_incrementais_SIN_medios_anuais


    @property
    def df_custos_viol_incrementais_SIN_valores_medios_primeiro_ano_media_outros_anos(self)->pd.DataFrame:
        if(self.__df_viol_incrementais_SIN_primeiro_ano_media_outros_anos is None):
            self.__retorna_custo_incremental_viol_SIN()
        return self.__df_viol_incrementais_SIN_primeiro_ano_media_outros_anos


    
    def __retorna_custo_incremental_viol_SIN(self)->pd.DataFrame:
        df_retorna = pd.DataFrame()
        df_temp =  self.__df_viol_SIN_mean_mean
        df_temp["Viol Def Min"] = ((self.__df_viol_SIN_mean_mean["Viol Def Min"].round(2)/self.__df_viol_SIN_mean_mean.loc[(self.__df_viol_SIN_mean_mean["caso"] == self.nome_caso_referencia)]["Viol Def Min"].round(2).iloc[0]) - 1)*100
        df_temp = df_temp.drop(df_temp[df_temp['caso'] == self.nome_caso_referencia].index)
        self.__df_viol_incrementais_SIN_medio_medio = df_temp.reset_index(drop = True)

        anos = set(self.__df_viol_SIN_mean_anual["anos"].tolist())
        #print(anos)
        listaDF = []
        for ano in anos:
            df_temp = self.__df_viol_SIN_mean_anual.loc[(self.__df_viol_SIN_mean_anual["anos"] == ano)]
            df_temp["Viol Def Min"] = ((df_temp["Viol Def Min"].round(2)/df_temp.loc[(df_temp["caso"] == self.nome_caso_referencia)]["Viol Def Min"].round(2).iloc[0]) - 1)*100
            df_temp = df_temp.drop(df_temp[df_temp['caso'] == self.nome_caso_referencia].index)
            listaDF.append(df_temp)

        df_completo = pd.concat(listaDF)
        df_completo = df_completo.reset_index(drop=True)
        self.__df_viol_incrementais_SIN_medios_anuais = df_completo
        
        #print(df_completo)

        #print("OUTROS")
        anos = set(self.__df_viol_SIN_primeiro_ano_media_outros_anos["anos"].tolist())
        #print(anos)
        listaDF = []
        for ano in anos:
            df_temp = self.__df_viol_SIN_primeiro_ano_media_outros_anos.loc[(self.__df_viol_SIN_primeiro_ano_media_outros_anos["anos"] == ano)]
            df_temp["Viol Def Min"] = ((df_temp["Viol Def Min"].round(2)/df_temp.loc[(df_temp["caso"] == self.nome_caso_referencia)]["Viol Def Min"].round(2).iloc[0]) - 1)*100
            df_temp = df_temp.drop(df_temp[df_temp['caso'] == self.nome_caso_referencia].index)
            listaDF.append(df_temp)
        df_completo = pd.concat(listaDF)
        df_completo = df_completo.reset_index(drop=True)
        self.__df_viol_incrementais_SIN_primeiro_ano_media_outros_anos = df_completo
        #print(df_completo)
            
            #for col in df_mean.columns:
        #print(self.__df_viol_incrementais_SIN_medio_medio)
        #print(self.__df_viol_incrementais_SIN_medios_anuais)
        #print(self.__df_viol_incrementais_SIN_primeiro_ano_media_outros_anos)

        
        return 0

    
    def __retorna_custo_incremental_no_df_custos_USI(self)->pd.DataFrame:
        df_retorna = pd.DataFrame()
        self.__df_viol_incrementais_usinas_medio_medio = pd.DataFrame()
        listDF = []
        for u in self.usinas:
            df_temp = self.df_viol_usinas_mean_mean.loc[(self.df_viol_usinas_mean_mean["usina"] == u.nome)]
            df_temp["Viol Def Min"] = ((df_temp["Viol Def Min"].round(2)/df_temp.loc[(df_temp["caso"] == self.nome_caso_referencia)]["Viol Def Min"].round(2).iloc[0]) - 1)*100
            df_temp["Viol GH Min"] = ((df_temp["Viol GH Min"].round(2)/df_temp.loc[(df_temp["caso"] == self.nome_caso_referencia)]["Viol GH Min"].round(2).iloc[0]) - 1)*100
            df_temp = df_temp.drop(df_temp[df_temp['caso'] == self.nome_caso_referencia].index)
            listDF.append(df_temp)
        
        self.__df_viol_incrementais_usinas_medio_medio = pd.concat(listDF).reset_index(drop = True)

        #print(self.__df_viol_incrementais_usinas_medio_medio)

        anos = set(self.__df_viol_usinas_mean_anual["anos"].tolist())
        #print(anos)
        listaDF = []
        for u in self.usinas:
            df_usina = self.__df_viol_usinas_mean_anual.loc[(self.__df_viol_usinas_mean_anual["usina"] == u.nome)]
            #print(df_usina)
            for ano in anos:
                df_temp = df_usina.loc[(df_usina["anos"] == ano)]
                df_temp["Viol Def Min"] = ((df_temp["Viol Def Min"].round(2)/df_temp.loc[(df_temp["caso"] == self.nome_caso_referencia)]["Viol Def Min"].round(2).iloc[0]) - 1)*100
                df_temp["Viol GH Min"] = ((df_temp["Viol GH Min"].round(2)/df_temp.loc[(df_temp["caso"] == self.nome_caso_referencia)]["Viol GH Min"].round(2).iloc[0]) - 1)*100
                df_temp = df_temp.drop(df_temp[df_temp['caso'] == self.nome_caso_referencia].index)
                listaDF.append(df_temp)

        df_completo = pd.concat(listaDF)
        df_completo = df_completo.reset_index(drop=True)
        self.__df_viol_incrementais_usinas_medios_anuais = df_completo
        
        print(df_completo)

        #print("OUTROS")
        anos = set(self.__df_viol_usina_primeiro_ano_media_outros_anos["anos"].tolist())
        #print(anos)
        listaDF = []
        for u in self.usinas:
            df_usina = self.__df_viol_usina_primeiro_ano_media_outros_anos.loc[(self.__df_viol_usina_primeiro_ano_media_outros_anos["usina"] == u.nome)]
            print(df_usina)
            for ano in anos:
                df_temp = df_usina.loc[(df_usina["anos"] == ano)]
                df_temp["Viol Def Min"] = ((df_temp["Viol Def Min"].round(2)/df_temp.loc[(df_temp["caso"] == self.nome_caso_referencia)]["Viol Def Min"].round(2).iloc[0]) - 1)*100
                df_temp["Viol GH Min"] = ((df_temp["Viol GH Min"].round(2)/df_temp.loc[(df_temp["caso"] == self.nome_caso_referencia)]["Viol GH Min"].round(2).iloc[0]) - 1)*100
                df_temp = df_temp.drop(df_temp[df_temp['caso'] == self.nome_caso_referencia].index)
                listaDF.append(df_temp)
        df_completo = pd.concat(listaDF)
        df_completo = df_completo.reset_index(drop=True)
        self.__df_viol_incrementais_usinas_primeiro_ano_media_outros_anos = df_completo
        print(df_completo)
        return 0

