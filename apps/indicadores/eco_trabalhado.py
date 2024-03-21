import pandas as pd

class EcoTrabalhado:    
    def __init__(self, df_cru):
        self.__df_cru = df_cru

    @property
    def df_cru(self):
        return self.__df_cru

    @property
    def df_medias(self):
        df_medias = self.__df_cru.loc[(self.__df_cru["cenario"] == "mean")].reset_index(drop=True)
        return df_medias

    @property
    def df_valor_medio(self):
        df_valor = self.df_medias["valor"].mean()
        return df_valor

    @property
    def df_medias_anuais_discretizadas(self):
        df_temp = self.__df_cru[self.__df_cru[['cenario']].apply(lambda x: x[0].isdigit(), axis=1)]
        df_anual = self.__df_cru.groupby(self.__df_cru["dataInicio"].dt.year)["valor"].agg(['mean'])
        df_anual = df_anual.reset_index(drop = False)
        df_anual.columns = df_anual.columns.str.replace('dataInicio', 'anos') 
        df_anual.columns = df_anual.columns.str.replace('mean', 'valor') 
        
        return df_anual

    @property
    def df_medias_primeiro_ano_outros_anos(self):
        anos = set(self.df_medias_anuais_discretizadas["anos"].tolist())
        print(anos)
        listaDF = []
        df_primeiro = self.df_medias_anuais_discretizadas.loc[self.df_medias_anuais_discretizadas["anos"] == min(anos)]
        df_outros = self.df_medias_anuais_discretizadas.loc[self.df_medias_anuais_discretizadas["anos"] != min(anos)]
        df_temp = pd.DataFrame()
        df_temp.at[0, "valor"] = df_outros["valor"].mean()
        anoInicial = df_outros["anos"].iloc[0]
        anoFinal = df_outros["anos"].iloc[-1]
        df_temp.at[0, "anos"] = str(anoInicial)+"-"+str(anoFinal)
        df_primeiro["anos"] = df_primeiro["anos"].astype(str)
        listaDF.append(df_primeiro)
        listaDF.append(df_temp)
        df_anual_primeiro_ano_outros_anos = pd.concat(listaDF)
        df_anual_primeiro_ano_outros_anos = df_anual_primeiro_ano_outros_anos.reset_index(drop = True)
        return df_anual_primeiro_ano_outros_anos
