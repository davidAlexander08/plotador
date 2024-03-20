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

class IndicadoresCalibracaoCVAR:
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
        self.__criaCref()
        self.casos = casos
        self.usinas = usinas
        self.nome_caso_referencia = nome_caso_referencia
        self.__df_custos_incrementais = None
        self.__df_valores_medios_caso = None
        self.__df_custos = None
        self.__df_custos_viol_incrementais = None
        self.__df_valores_anuais_medios = None
        self.__df_cref = None
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
    
    def __le_arquivo_sintese_caso_SIN_geral(
        self, caso: CasoCalibracaoCVAR, nome_sintese: str, coluna :str, cenario:str
    ) -> np.ndarray:
        caminho_caso = caso.caminho
        arq_sintese = join(
            caminho_caso, self.DIR_SINTESE, f"{nome_sintese}.parquet.gzip"
        )
        df = pd.read_parquet(arq_sintese)
        dados = df.loc[df[coluna] == cenario, "valor"].to_numpy().flatten()
        return dados
    
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
        
        
    def __gera_df_custos_incrementais(self) -> pd.DataFrame:
        """
        Gera o DataFrame que contém as informações para serem visualizadas
        nos gráficos de fronteiras de pareto. Para algumas das colunas é
        necessário o estabelecimento de um caso de "referência", em relação
        ao qual são calculados incrementos / decrementos de custo e energia
        armazenada.

        Colunas:

        - earm_mwh: energia armazenada média (MWh)
        - earm_mwmes: energia armazenada média (MWmes)
        - gt_mwh: geração térmica total (MWh)
        - gt_mwmes: geração térmica total (MWmes)
        - ct_com_vpl: custo de térmica com valor presente líquido (R$)
        - ct_sem_vpl: custo de térmica sem valor presente líquido (R$)
        - carga: carga média do SIN (MWh)
        - delta_earm: variação de energia armazenada (MWh) em relação
            ao caso referência
        - delta_ct: variação de custo de térmica sem VPL (R$) em relação
            ao caso referência
        - delta_gt_mwh: variação de geração térmica em relação
            ao caso referência (MWh)
        - delta_gt_mwmes: variação de geração térmica em relação
            ao caso referência (MWmes)
        - ct_por_earm: delta_ct / delta_earm
        - ct_por_carga: delta_ct / carga
        - gt_por_earm: delta_gt_mwh / delta_earm
        - gt_por_carga: delta_gt_mwh / carga
        """
        Log.log().info("Gerando DataFrame de custos incrementais")
        dfs_casos = [
            self.__gera_df_custos_incrementais_caso(c) for c in self.casos
        ]
        df_completo = pd.concat(dfs_casos)
        df_completo = self.__calcula_colunas_deltas_incrementais(df_completo)
        return df_completo

    def __calcula_colunas_deltas_incrementais(
        self, df: pd.DataFrame
    ) -> pd.DataFrame:
        df_i = df.copy()
        df_i["delta_earm_mwh"] = (
            df_i["earm_mwh"] - df_i.at[self.nome_caso_referencia, "earm_mwh"]
        )
        
        df_i["delta_earm_mwmes"] = (
            df_i["earm_mwmes"]
            - df_i.at[self.nome_caso_referencia, "earm_mwmes"]
        )

        df_i["delta_ct"] = (
            df_i["ct_sem_vpl"]
            - df_i.at[self.nome_caso_referencia, "ct_sem_vpl"]
        )




        

        df_i["delta_gt_mwh"] = (
            df_i["gt_mwh"] - df_i.at[self.nome_caso_referencia, "gt_mwh"]
        )
        df_i["delta_gt_mwmes"] = (
            df_i["gt_mwmes"] - df_i.at[self.nome_caso_referencia, "gt_mwmes"]
        )
        df_i["ct_por_earm"] = df_i["delta_ct"] / df_i["delta_earm_mwh"]
        df_i["ct_por_carga"] = df_i["delta_ct"] / df_i["carga"]
        df_i["gt_por_earm"] = df_i["delta_gt_mwh"] / df_i["delta_earm_mwh"]
        df_i["gt_por_carga"] = df_i["delta_gt_mwh"] / df_i["carga"]

        return df_i

    def calculaIntervaloConfianca(self, std):
        IC = 1.96*std/(np.sqrt(2000))
        return IC

    def __gera_df_valores_medios_caso(
        self, caso: CasoCalibracaoCVAR
    ) -> pd.DataFrame:
        nome_caso = caso.nome
        caminho_caso = caso.caminho
        cmo_se_2o_mes = self.__le_arquivo_sintese_caso_SBM(
            caso, "CMO_SBM_EST", "SUDESTE"
        )[1]
        cmo_ne_2o_mes = self.__le_arquivo_sintese_caso_SBM(
            caso, "CMO_SBM_EST", "NORDESTE"
        )[1]
        gter_2o_mes = self.__le_arquivo_sintese_caso_SIN(
            caso, "GTER_SIN_EST"
        )[1]
        cmo_se_med = np.mean(self.__le_arquivo_sintese_caso_SBM(
            caso, "CMO_SBM_EST", "SUDESTE"
        ))
        cmo_ne_med = np.mean(self.__le_arquivo_sintese_caso_SBM(
            caso, "CMO_SBM_EST", "NORDESTE"
        ))
        earm_mwmes = self.__le_arquivo_sintese_caso_SIN(caso, "EARMF_SIN_EST")
        earm_perc = self.__le_arquivo_sintese_caso_SIN(caso, "EARPF_SIN_EST")
        earm_med_mwh = self.__calcula_earm_medio_mwh(caso)
        earm_med_mwmes = np.mean(earm_mwmes)
        earm_med_perc = np.mean(earm_perc)
        earm_1mes_perc = earm_perc[0]

        
        
        vert_tot_med = np.mean(
            self.__le_arquivo_sintese_caso_SIN(caso, "EVER_SIN_EST")
        )
        vert_turb_med = np.mean(
            self.__le_arquivo_sintese_caso_SIN(caso, "EVERFT_SIN_EST")
        )
        gter_list  = self.__le_arquivo_sintese_caso_SIN(caso, "GTER_SIN_EST")
        gter_med = np.mean(gter_list)
        gter_1mes = gter_list[0]

        ghid_med = np.mean(
            self.__le_arquivo_sintese_caso_SIN(caso, "GHID_SIN_EST")
        )
        cter_med = np.sum(
            self.__le_arquivo_sintese_caso_SIN(caso, "CTER_SIN_EST")
        )

        cter_med_cenarios = self.__retorna_df_2000_cenarios_acumulado_no_periodo(
            caso, "CTER_SIN_EST"
        )
        cter_med_cenarios = cter_med_cenarios.groupby(["cenario"]).sum()
        cter_med_cenarios = cter_med_cenarios.iloc[cter_med_cenarios.index.astype(int).argsort()]
        earm_med_mwmes_cenarios = self.__retorna_df_2000_cenarios_acumulado_no_periodo(
            caso, "EARMF_SIN_EST"
        )
        earm_med_mwmes_cenarios = earm_med_mwmes_cenarios.groupby(["cenario"]).mean()
        earm_med_mwmes_cenarios = earm_med_mwmes_cenarios.iloc[earm_med_mwmes_cenarios.index.astype(int).argsort()]
        def_med = np.mean(
            self.__le_arquivo_sintese_caso_SIN(caso, "DEF_SIN_EST")
        )
        cdef_med = np.sum(
            self.__le_arquivo_sintese_caso_SIN(caso, "CDEF_SIN_EST")
        )

        cdef_med_cenarios = self.__retorna_df_2000_cenarios_acumulado_no_periodo(
            caso, "CDEF_SIN_EST"
        )
        cdef_med_cenarios = cdef_med_cenarios.groupby(["cenario"]).sum()
        cdef_med_cenarios = cdef_med_cenarios.iloc[cdef_med_cenarios.index.astype(int).argsort()]
        coper_med = np.mean(
            self.__le_arquivo_sintese_caso_SIN(caso, "COP_SIN_EST")
        )
        # EARM dos primeiros meses de ABR e NOV
        arq_earm = join(
            caminho_caso, self.DIR_SINTESE, "EARMF_SIN_EST.parquet.gzip"
        )
        df_earm = pd.read_parquet(arq_earm)

        earm_abr_mwmes = (
            df_earm.loc[
                (df_earm["cenario"] == "mean")
                & (df_earm["dataInicio"].dt.month == 4),
                "valor",
            ]
            .to_numpy()
            .flatten()[0]
        )
        earm_nov_mwmes = (
            df_earm.loc[
                (df_earm["cenario"] == "mean")
                & (df_earm["dataInicio"].dt.month == 11),
                "valor",
            ]
            .to_numpy()
            .flatten()[0]
        )

        df = pd.DataFrame()
        df.loc[nome_caso, "cmo_2mes_se"] = cmo_se_2o_mes
        df.loc[nome_caso, "cmo_2mes_ne"] = cmo_ne_2o_mes
        df.loc[nome_caso, "earm_1mes_perc"] = earm_1mes_perc
        df.loc[nome_caso, "gter_1mes"] = gter_1mes
        df.loc[nome_caso, "gter_2o_mes"] = gter_2o_mes
        df.loc[nome_caso, "cmo_se_med"] = cmo_se_med
        df.loc[nome_caso, "cmo_ne_med"] = cmo_ne_med
        df.loc[nome_caso, "earm_med_mwh"] = earm_med_mwh
        df.loc[nome_caso, "earm_med_mwmes"] = earm_med_mwmes
        df.loc[nome_caso, "earm_med_mwmes_std_r$"] = self.calculaIntervaloConfianca(np.std(earm_med_mwmes_cenarios["valor"]) ) 
        df.loc[nome_caso, "earm_med_perc"] = earm_med_perc
        df.loc[nome_caso, "earm_nov_mwmes"] = earm_nov_mwmes
        df.loc[nome_caso, "earm_abr_mwmes"] = earm_abr_mwmes
        df.loc[nome_caso, "vert_tot_med_mwmes"] = vert_tot_med
        df.loc[nome_caso, "vert_turb_med_mwmes"] = vert_turb_med
        df.loc[nome_caso, "coper_med_r$"] = coper_med * (10**6)
        df.loc[nome_caso, "cdef_med_r$"] = cdef_med * (10**6)
        df.loc[nome_caso, "cdef_med_std_r$"] = self.calculaIntervaloConfianca(np.std(cdef_med_cenarios["valor"]* (10**6)) )  
        df.loc[nome_caso, "def_med_mwmes"] = def_med* (10**6)
        df.loc[nome_caso, "gterm_med_mwmes"] = gter_med
        df.loc[nome_caso, "ghid_med_mwmes"] = ghid_med
        df.loc[nome_caso, "cterm_med_r$"] = cter_med * (10**6)
        df.loc[nome_caso, "cter_std_r$"] = self.calculaIntervaloConfianca(np.std(cter_med_cenarios["valor"]* (10**6)) )
        df.index.name = "caso"
        return df
        
    def __retorna_df_2000_cenarios_acumulado_no_periodo(
        self, caso: CasoCalibracaoCVAR, nome_sintese: str
    ) -> np.ndarray:
        caminho_caso = caso.caminho
        arq_sintese = join(
            caminho_caso, self.DIR_SINTESE, f"{nome_sintese}.parquet.gzip"
        )
        df = pd.read_parquet(arq_sintese)
        df = df.loc[:, df.columns!='dataInicio']
        df = df.loc[:, df.columns!='dataFim']
        df =  df[df[['cenario']].apply(lambda x: x[0].isdigit(), axis=1)]
        return df

    def __retorna_df_2000_cenarios_acumulado_no_periodo_Referencia(
        self, nome_sintese: str
    ) -> np.ndarray:
        caminho_caso = ""
        for caso in self.casos:
            if(caso.nome == self.nome_caso_referencia):
                caminho_caso = caso.caminho
       
        arq_sintese = join(
            caminho_caso, self.DIR_SINTESE, f"{nome_sintese}.parquet.gzip"
        )
        df = pd.read_parquet(arq_sintese)
        df = df.loc[:, df.columns!='dataInicio']
        df = df.loc[:, df.columns!='dataFim']
        df =  df[df[['cenario']].apply(lambda x: x[0].isdigit(), axis=1)]
        return df
        
    def __gera_df_custos_incrementais_caso(
        self, caso: CasoCalibracaoCVAR
    ) -> pd.DataFrame:
        taxa_desconto_anual = (
            Dger.read(join(caso.caminho, "dger.dat")).taxa_de_desconto / 100.0
        )
        earm_medio_mwmes = self.__le_arquivo_sintese_caso_SIN(
            caso, "EARMF_SIN_EST"
        )
        earm_medio_final_perc = self.__le_arquivo_sintese_caso_SIN(
            caso, "EARPF_SIN_EST"
        )
        
        earm_medio_final_perc_cenarios = self.__retorna_df_2000_cenarios_acumulado_no_periodo(
            caso, "EARPF_SIN_EST"
        )

        earm_medio_final_perc_cenarios = earm_medio_final_perc_cenarios.groupby(["cenario"]).mean()
        earm_medio_final_perc_cenarios = earm_medio_final_perc_cenarios.iloc[earm_medio_final_perc_cenarios.index.astype(int).argsort()]
        
        
        gt_medio_mwmes = self.__le_arquivo_sintese_caso_SIN(
            caso, "GTER_SIN_EST"
        )

        gt_medio_mwmes_cenarios = self.__retorna_df_2000_cenarios_acumulado_no_periodo(
            caso, "GTER_SIN_EST"
        )
        gt_medio_mwmes_cenarios = gt_medio_mwmes_cenarios.groupby(["cenario"]).sum()
        gt_medio_mwmes_cenarios = gt_medio_mwmes_cenarios.iloc[gt_medio_mwmes_cenarios.index.astype(int).argsort()]

        cter_valor_futuro = self.__le_arquivo_sintese_caso_SIN(
            caso, "CTER_SIN_EST"
        )
        earm_medio_mwmes_cenarios = self.__retorna_df_2000_cenarios_acumulado_no_periodo(
            caso, "EARMF_SIN_EST"
        )
        earm_medio_mwmes_cenarios = earm_medio_mwmes_cenarios.groupby(["cenario"]).mean()
        earm_medio_mwmes_cenarios = earm_medio_mwmes_cenarios.iloc[earm_medio_mwmes_cenarios.index.astype(int).argsort()]

        cter_med = np.mean(
            self.__le_arquivo_sintese_caso_SIN(caso, "CTER_SIN_EST")
        )
        cter_med_cenarios = self.__retorna_df_2000_cenarios_acumulado_no_periodo(
            caso, "CTER_SIN_EST"
        )
        cter_med_cenarios = cter_med_cenarios.groupby(["cenario"]).sum()
        cter_med_cenarios = cter_med_cenarios.iloc[cter_med_cenarios.index.astype(int).argsort()]

        
        gt_medio_mwmes_cenarios_ref = self.__retorna_df_2000_cenarios_acumulado_no_periodo_Referencia(
            "GTER_SIN_EST"
        )
        gt_medio_mwmes_cenarios_ref = gt_medio_mwmes_cenarios_ref.groupby(["cenario"]).sum()
        gt_medio_mwmes_cenarios_ref = gt_medio_mwmes_cenarios_ref.iloc[gt_medio_mwmes_cenarios_ref.index.astype(int).argsort()]
        
        earm_medio_mwmes_cenarios_ref = self.__retorna_df_2000_cenarios_acumulado_no_periodo_Referencia(
            "EARMF_SIN_EST"
        )
        earm_medio_mwmes_cenarios_ref = earm_medio_mwmes_cenarios_ref.groupby(["cenario"]).mean()
        earm_medio_mwmes_cenarios_ref = earm_medio_mwmes_cenarios_ref.iloc[earm_medio_mwmes_cenarios_ref.index.astype(int).argsort()]
        
        cter_med_cenarios_ref = self.__retorna_df_2000_cenarios_acumulado_no_periodo_Referencia(
            "CTER_SIN_EST"
        )
        cter_med_cenarios_ref = cter_med_cenarios_ref.groupby(["cenario"]).sum()
        cter_med_cenarios_ref = cter_med_cenarios_ref.iloc[cter_med_cenarios_ref.index.astype(int).argsort()]

        ganho_gt = gt_medio_mwmes_cenarios["valor"] - gt_medio_mwmes_cenarios_ref["valor"]
        ganho_earm = earm_medio_mwmes_cenarios["valor"] - earm_medio_mwmes_cenarios_ref["valor"]
        ganho_cter = cter_med_cenarios["valor"] - cter_med_cenarios_ref["valor"]
        
        
        cter_valor_presente = self.__traz_custo_a_valor_presente(
            taxa_desconto_anual, cter_valor_futuro
        )
        earm_medio_mwh = self.__calcula_earm_medio_mwh(caso)
        gt_medio_mwh = self.__calcula_gt_medio_mwh(caso)
        mercado_liquido_mwh = self.__calcula_mercado_liquido_mwh(caso)
        df = pd.DataFrame()
        df.loc[caso.nome, "earm_mwh"] = earm_medio_mwh
        df.loc[caso.nome, "earm_mwmes"] = np.mean(earm_medio_mwmes)
        df.loc[caso.nome, "earm_medio_final_perc"] = np.mean(earm_medio_final_perc)
        df.loc[caso.nome, "earm_medio_final_perc_std"] = self.calculaIntervaloConfianca(np.std(earm_medio_final_perc_cenarios["valor"]))
        df.loc[caso.nome, "gt_mwh"] = gt_medio_mwh
        df.loc[caso.nome, "gt_mwmes"] = sum(gt_medio_mwmes)
        df.loc[caso.nome, "gt_mwmes_std"] = self.calculaIntervaloConfianca(np.std(gt_medio_mwmes_cenarios["valor"]))
        df.loc[caso.nome, "ct_com_vpl"] = cter_valor_presente * 10**6
        df.loc[caso.nome, "ct_sem_vpl"] = sum(cter_valor_futuro) * 10**6
        df.loc[caso.nome, "carga"] = mercado_liquido_mwh
        df.loc[caso.nome, "cterm_med_r$"] = cter_med * (10**6)
        #df.loc[caso.nome, "cter_std_r$"] = self.calculaIntervaloConfianca(np.std(cter_med_cenarios["valor"]* (10**6)) )
        df.loc[caso.nome, "ganho_gt_std"] = self.calculaIntervaloConfianca(np.std(ganho_gt.values)) 
        df.loc[caso.nome, "ganho_earm_std"] = self.calculaIntervaloConfianca(np.std(ganho_earm.values)) 
        df.loc[caso.nome, "ganho_cter_std"] = self.calculaIntervaloConfianca(np.std(ganho_cter.values) * (10**6))
        df.index.name = "caso"
        return df

    
    def __le_arquivo_sintese_caso_periodo(
        self, caso: CasoCalibracaoCVAR, nome_sintese: str, segundoArgumento
        ) -> pd.DataFrame:
        
        caminho_caso = caso.caminho
        arq_sintese = join(
            caminho_caso, self.DIR_SINTESE, f"{nome_sintese}.parquet.gzip"
        )
        if(os.path.isfile(arq_sintese)):
            df = pd.read_parquet(arq_sintese)
            if(segundoArgumento is None):
                dados = df.loc[df["cenario"] == "mean"].reset_index(drop=True)
            else:
                dados = (
                    df.loc[
                        (df["cenario"] == "mean") & (df["submercado"] == segundoArgumento)].reset_index(drop=True)
                )
            return dados
        else:
            dados = pd.DataFrame({"valor":[0]})
            return dados
        


    def __gera_df_valores_medios_periodo(
        self, caso: CasoCalibracaoCVAR, nome_sintese:str, segundoArgumento
    ) -> pd.DataFrame:
        nome_caso = caso.nome
        df_med = self.__le_arquivo_sintese_caso_periodo(caso, nome_sintese, segundoArgumento)
        return df_med

    def __gera_df_acumulado_valores_medios_periodo(self,nome_sintese, segundoArgumento, coluna) -> pd.DataFrame:
        Log.log().info("Gerando DataFrame de valores médios por periodo")
        mapaCasos  = {}
        df = pd.DataFrame()
        for c in self.casos:
            df[c.nome] = self.__gera_df_valores_medios_periodo(c,nome_sintese, segundoArgumento)[coluna]
        df.index.name = "estagio"
        return df

    def calcula_df_valores_medios_periodo(self, nome_sintese, segundoArgumento, coluna) -> pd.DataFrame:
        dfvalores_medios_periodo = self.__gera_df_acumulado_valores_medios_periodo(nome_sintese, segundoArgumento, coluna)
        return dfvalores_medios_periodo


    
    def __traz_custo_a_valor_presente(
        self, taxa_desconto_anual: float, custos: np.ndarray
    ) -> float:
        taxa_desconto_mensal = (1 + taxa_desconto_anual) ** (1 / 12.0) - 1
        indices_estagios = np.arange(custos.shape[0])
        descontos_mensais = np.power(
            1 - taxa_desconto_mensal, indices_estagios
        )
        print(indices_estagios)
        print(descontos_mensais)
        return np.sum(np.multiply(custos, descontos_mensais))

    
    def __le_arquivo_sintese_caso_SIN(
        self, caso: CasoCalibracaoCVAR, nome_sintese: str
    ) -> np.ndarray:
        caminho_caso = caso.caminho
        arq_sintese = join(
            caminho_caso, self.DIR_SINTESE, f"{nome_sintese}.parquet.gzip"
        )
        df = pd.read_parquet(arq_sintese)
        dados = df.loc[df["cenario"] == "mean", "valor"].to_numpy().flatten()
        return dados

    def __le_arquivo_sintese_caso_SBM(
        self, caso: CasoCalibracaoCVAR, nome_sintese: str, submercado: str
    ) -> np.ndarray:
        caminho_caso = caso.caminho
        arq_sintese = join(
            caminho_caso, self.DIR_SINTESE, f"{nome_sintese}.parquet.gzip"
        )
        df = pd.read_parquet(arq_sintese)
        dados = (
            df.loc[
                (df["cenario"] == "mean") & (df["submercado"] == submercado),
                "valor",
            ]
            .to_numpy()
            .flatten()
        )
        return dados





    
    @staticmethod
    def __converte_timestamp_em_datetime(
        dado_timestamp: pd.Timestamp,
    ) -> datetime:
        timestamp = (
            dado_timestamp - np.datetime64("1970-01-01T00:00:00")
        ) / np.timedelta64(1, "s")
        return datetime.utcfromtimestamp(timestamp)

    def __calcula_earm_medio_mwh(self, caso: CasoCalibracaoCVAR) -> float:
        caminho_caso = caso.caminho
        df = pd.read_parquet(
            join(caminho_caso, self.DIR_SINTESE, "EARMF_SIN_EST.parquet.gzip")
        )
        meses = df["dataInicio"].unique()
        meses_dt = [self.__converte_timestamp_em_datetime(m) for m in meses]
        dias_meses = [monthrange(m.year, m.month)[1] for m in meses_dt]
        earm_mwmes = (
            df.loc[df["cenario"] == "mean", "valor"].to_numpy().flatten()
        )
        earm_mwh = sum(np.multiply(earm_mwmes, dias_meses)) * 24
        return earm_mwh

    def __calcula_gt_medio_mwh(self, caso: CasoCalibracaoCVAR) -> float:
        caminho_caso = caso.caminho
        df = pd.read_parquet(
            join(caminho_caso, self.DIR_SINTESE, "GTER_SIN_EST.parquet.gzip")
        )
        meses = df["dataInicio"].unique()
        meses_dt = [self.__converte_timestamp_em_datetime(m) for m in meses]
        dias_meses = [monthrange(m.year, m.month)[1] for m in meses_dt]
        gt_mwmes = (
            df.loc[df["cenario"] == "mean", "valor"].to_numpy().flatten()
        )
        gt_mwh = sum(np.multiply(gt_mwmes, dias_meses)) * 24
        return gt_mwh

    def __calcula_mercado_liquido_mwh(self, caso: CasoCalibracaoCVAR) -> float:
        mercado_mwh = self.__le_arquivo_sintese_caso_SIN(caso, "MERL_SIN_EST")
        return np.sum(mercado_mwh) * 740

    
    





    @property
    def df_custos_incrementais(self) -> pd.DataFrame:
        """
        Colunas:

        - earm_mwh: energia armazenada média (MWh)
        - earm_mwmes: energia armazenada média (MWmes)
        - gt_mwh: geração térmica total (MWh)
        - gt_mwmes: geração térmica total (MWmes)
        - ct_com_vpl: custo de térmica com valor presente líquido (R$)
        - ct_sem_vpl: custo de térmica sem valor presente líquido (R$)
        - carga: carga média do SIN (MWh)
        - delta_earm_mwh: variação de energia armazenada (MWh) em relação
            ao caso referência
        - delta_earm_mwmes: variação de energia armazenada (MWmes) em relação
            ao caso referência
        - delta_ct: variação de custo de térmica sem VPL (R$) em relação
            ao caso referência
        - delta_gt_mwh: variação de geração térmica em relação
            ao caso referência (MWh)
        - delta_gt_mwmes: variação de geração térmica em relação
            ao caso referência (MWmes)
        - ct_por_earm: delta_ct / delta_earm
        - ct_por_carga: delta_ct / carga
        - gt_por_earm: delta_gt_mwh / delta_earm
        - gt_por_carga: delta_gt_mwh / carga
        """
        if self.__df_custos_incrementais is None:
            self.__df_custos_incrementais = (
                self.__gera_df_custos_incrementais()
            )
        return self.__df_custos_incrementais


    def __gera_df_valores_medios(self) -> pd.DataFrame:
        """
        Gera o DataFrame que contém as informações para serem visualizadas
        nos gráficos de fronteiras de pareto.

        Colunas:

        - cmo_2mes_se: CMO do submercado SE (R$ / MWh)
        - cmo_2mes_ne: CMO do submercado NE (R$ / MWh)
        - gter_2o_mes: GTER do SIN (MWmes)
        - earm_med_mwh: energia armazenada média (MWh)
        - earm_med_mwmes: energia armazenada média (MWmes)
        - earm_med_perc: energia armazenada média (% earmax)
        - earm_abr_mwmes: energia armazenada do primeiro abril
            do horizonte de estudo (MWmes)
        - earm_nov_mwmes: energia armazenada do primeiro novembro
            do horizonte de estudo (MWmes)
        - vert_tot_med_mwmes: vertimento total médio (MWmes)
        - vert_turb_med_mwmes: vertimento turbinável médio (MWmes)
        - coper_med_r$: custo de operação médio do período de estudo (R$)
        - cdef_med_r$: custo de déficit médio do período de estudo (R$)
        - cterm_med_r$: custo de geração térmica média do período de estudo (R$)
        - def_med_mwmes: déficit médio do período de estudo (MWmes)
        - gter_med_mwmes: geração térmica média do período de estudo (MWmes)
        """
        Log.log().info("Gerando DataFrame de valores médios")
        dfs_casos = [self.__gera_df_valores_medios_caso(c) for c in self.casos]
        df_completo = pd.concat(dfs_casos)
        return df_completo

    @property
    def df_valores_medios_caso(self) -> pd.DataFrame:
        """
        Colunas:

        - cmo_2mes_se: CMO do submercado SE (R$ / MWh)
        - cmo_2mes_ne: CMO do submercado NE (R$ / MWh)
        - gter_2o_mes: GTER do SIN (MWmes)
        - earm_med_mwh: energia armazenada média (MWh)
        - earm_med_mwmes: energia armazenada média (MWmes)
        - earm_med_perc: energia armazenada média (% earmax)
        - earm_abr_mwmes: energia armazenada do primeiro abril
            do horizonte de estudo (MWmes)
        - earm_nov_mwmes: energia armazenada do primeiro novembro
            do horizonte de estudo (MWmes)
        - vert_tot_med_mwmes: vertimento total médio (MWmes)
        - vert_turb_med_mwmes: vertimento turbinável médio (MWmes)
        - coper_med_r$: custo de operação médio do período de estudo (R$)
        - cdef_med_r$: custo de déficit médio do período de estudo (R$)
        - cterm_med_r$: custo de geração térmica média do período de estudo (R$)
        - def_med_mwmes: déficit médio do período de estudo (MWmes)
        - gter_med_mwmes: geração térmica média do período de estudo (MWmes)
        """
        if self.__df_valores_medios_caso is None:
            self.__df_valores_medios_caso = self.__gera_df_valores_medios()
        return self.__df_valores_medios_caso

    @property
    def tabela_valores_medios(self) -> pd.DataFrame:
        df = self.df_valores_medios_caso.copy()
        mapa_colunas = {
            "caso": "Caso",
            "gterm_med_mwmes": "GT SIN Med (MWmes)",
            "ghid_med_mwmes": "GH SIN Med (MWmes)",
            "earm_med_perc": "EARM SIN Med (%)",
            "vert_tot_med_mwmes": "VERT SIN Med (MWmes)",
            "cmo_2mes_se": "CMO SE 2 Mes (R$/MWh)",
            "cmo_2mes_ne": "CMO NE 2 Mes (R$/MWh)",
            "earm_1mes_perc": "EARM SIN 1 Mes (%)",
            "gter_1mes": "GT SIN 1 Mes (MWmes)",
            "gter_2o_mes": "GT SIN 2 Mes (MWmes)",
            "cmo_se_med": "CMO SE Med (R$/MWh)",
            "cmo_ne_med": "CMO NE Med (R$/MWh)",
            "coper_med_r$": "COPER Med (Mi R$)",
        }
        df.index.name = "caso"
        df = df.reset_index()
        df = df.rename(columns=mapa_colunas)
        df = df[list(mapa_colunas.values())]
        df["COPER Med (Mi R$)"] /= 1e6
        return df

    @property
    def tabela_cmo_vert_earm_novembro(self) -> pd.DataFrame:
        df = self.df_valores_medios_caso.copy()
        mapa_colunas = {
            "caso": "Caso",
            "gterm_med_mwmes": "GT SIN Med (MWmes)",
            "earm_nov_mwmes": "EARM SIN - Nov 1 Ano (MWmes)",
            "vert_tot_med_mwmes": "VERT SIN Med (MWmes)",
            "cmo_2mes_se": "CMO SE 2 Mes (R$/MWh)",
            "cmo_2mes_ne": "CMO NE 2 Mes (R$/MWh)",
            "gter_2o_mes": "GT SIN 2 Mes (MWmes)",
        }
        df.index.name = "caso"
        df = df.reset_index()
        df = df.rename(columns=mapa_colunas)
        df = df[list(mapa_colunas.values())]
        return df

    @property
    def tabela_ganho_incremental(self) -> pd.DataFrame:
        df = self.df_custos_incrementais.copy()
        mapa_colunas = {
            "caso": "Caso",
            "delta_ct": "Custo GT em VPL (Mi R$)",
            "delta_earm_mwmes": "Ganho EARM (MWmes)",
            "delta_earm_mwh": "Ganho EARM (MWh)",
            "delta_gt_mwmes": "Ganho GT (MWmes)",
            "delta_gt_mwh": "Ganho GT (MWh)",
            "ct_por_earm": "Custo GT / Ganho EARM (R$/MWh)",
            "ct_por_carga": "Custo GT / Carga (R$/MWh)",
            "gt_por_earm": "Ganho GT / Ganho EARM",
            "gt_por_carga": "Ganho GT / Carga",
        }
        df.index.name = "caso"
        df = df.reset_index()
        df = df.rename(columns=mapa_colunas)
        df = df[list(mapa_colunas.values())]
        df["Custo GT em VPL (Mi R$)"] /= 1e6
        return df



    def gera_df_custos(self) -> pd.DataFrame:
        Log.log().info("Gerando DataFrame de custos de violação")
        
        mapaDataFrameCustos = {}
        nome_sintese = "CUSTOS"
        for caso in self.casos:

            caminho_caso = caso.caminho
            arq_sintese = join(
                caminho_caso, self.DIR_SINTESE, f"{nome_sintese}.parquet.gzip"
            )
            df = pd.read_parquet(arq_sintese)
            
            mapaDataFrameCustos[caso.nome] = df
        df_custos = pd.DataFrame()
        for nome_caso in mapaDataFrameCustos:
            for parcela in mapaDataFrameCustos[nome_caso]["parcela"]:
                df = mapaDataFrameCustos[nome_caso]
                df_custos.loc[nome_caso, parcela] = df.loc[df["parcela"]== parcela]["mean"].tolist()[0]
        df_custos.index.name = "caso"
        df_custos = df_custos.loc[:, (df_custos != 0).any(axis=0)] #Remove colunas com 0
        df_custos = df_custos.sort_values(by=df_custos.index.tolist()[0], ascending=False, axis = 1)
        df_custos = df_custos.round(1)
        return df_custos
    

    @property
    def df_custos(self) -> pd.DataFrame:
        if self.__df_custos is None:
            self.__df_custos = self.gera_df_custos()
        return self.__df_custos

            
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
    
    
    @property
    def df_custos_viol_incrementais(self)->pd.DataFrame:
        if(self.__df_custos_viol_incrementais is None):
            self.__df_custos_viol_incrementais = self.__retorna_custo_incremental_no_df_custos_SIN()
        return self.__df_custos_viol_incrementais
        
    def __retorna_custo_incremental_no_df_custos_SIN(self)->pd.DataFrame:
        df_retorna = pd.DataFrame()
        df_retorna["diff_VIOL_VAZMIN"] = (self.__df_custos["VIOLACAO VZMIN"]/self.__df_custos.at[self.nome_caso_referencia, "VIOLACAO VZMIN"] - 1)*100
        df_retorna["diff_VIOL_GHMIN"] = (self.__df_custos["VIOLACAO GHMINU"]/self.__df_custos.at[self.nome_caso_referencia, "VIOLACAO GHMINU"] - 1)*100
        df_retorna["diff_VIOL_VAZMIN_GHMIN"] = ((self.__df_custos["VIOLACAO VZMIN"]+ self.__df_custos["VIOLACAO GHMINU"])/(self.__df_custos.at[self.nome_caso_referencia, "VIOLACAO GHMINU"]+self.__df_custos.at[self.nome_caso_referencia, "VIOLACAO VZMIN"]) - 1)*100
        return df_retorna 



    

    def __le_arquivo_sintese_anual_caso_SIN(
        self, caso: CasoCalibracaoCVAR, nome_sintese: str
    ) -> np.ndarray:
        caminho_caso = caso.caminho
        arq_sintese = join(
            caminho_caso, self.DIR_SINTESE, f"{nome_sintese}.parquet.gzip"
        )
        check_file = os.path.isfile(arq_sintese)
        if(check_file) :
            df = pd.read_parquet(arq_sintese)
            df_teste = df.loc[df["cenario"] == "mean"]
            df_teste = df_teste.groupby(df_teste["dataInicio"].dt.year)["valor"].agg(['mean'])
            df_teste = df_teste.round(1)
            return df_teste
        else:
            arq_sintese = join(
                caminho_caso, self.DIR_SINTESE, "GHID_SIN_EST.parquet.gzip"
            )
            df = pd.read_parquet(arq_sintese)
            df_teste = df.loc[df["cenario"] == "mean"]
            df_teste = df_teste.groupby(df_teste["dataInicio"].dt.year)["valor"].agg(['mean'])
            df_teste = df_teste*0
            return df_teste


    def __le_arquivo_sintese_anual_caso_SBM(
        self, caso: CasoCalibracaoCVAR, nome_sintese: str, submercado: str
    ) -> np.ndarray:
        caminho_caso = caso.caminho
        arq_sintese = join(
            caminho_caso, self.DIR_SINTESE, f"{nome_sintese}.parquet.gzip"
        )
        df = pd.read_parquet(arq_sintese)

        df_teste = df.loc[(df["cenario"] == "mean") & (df["submercado"] == submercado)]
        df_teste = df_teste.groupby(df_teste["dataInicio"].dt.year)["valor"].agg(['mean'])
        df_teste = df_teste.round(1)
        return df_teste
    
    def __gera_df_valores_anuais_medios_caso(self, caso: CasoCalibracaoCVAR) -> pd.DataFrame:
        cmo_se_med = self.__le_arquivo_sintese_anual_caso_SBM(
            caso, "CMO_SBM_EST", "SUDESTE"
            )
        
        cmo_ne_med = self.__le_arquivo_sintese_anual_caso_SBM(
            caso, "CMO_SBM_EST", "NORDESTE"
            )
        

        earm_perc = self.__le_arquivo_sintese_anual_caso_SIN(
            caso, "EARPF_SIN_EST"
        )
        evert_tot_med = self.__le_arquivo_sintese_anual_caso_SIN(caso, "EVER_SIN_EST")
        
        gter_med = self.__le_arquivo_sintese_anual_caso_SIN(caso, "GTER_SIN_EST")
        
        ghid_med =  self.__le_arquivo_sintese_anual_caso_SIN(caso, "GHID_SIN_EST")
        
        vdefmin_med =  self.__le_arquivo_sintese_anual_caso_SIN(caso, "VDEFMIN_SIN_EST")
        
        coper_med =  self.__le_arquivo_sintese_anual_caso_SIN(caso, "COP_SIN_EST")
        
        df = pd.DataFrame()
        df["gter_med"] = gter_med["mean"]
        df["ghid_med"] = ghid_med["mean"]
        df["vdefmin_med"] = vdefmin_med["mean"]
        df["coper_med"] = coper_med["mean"]
        df["evert_tot_med"] = evert_tot_med["mean"]
        df["earm_perc"] = earm_perc["mean"]
        df["cmo_ne_med"] = cmo_ne_med["mean"]
        df["cmo_se_med"] = cmo_se_med["mean"]
        df.index.name = "data"
        return df


    def gera_df_valores_anuais_medios(self) -> pd.DataFrame:
        Log.log().info("Gerando DataFrame de valores anuais medios")
        """
        Gera o DataFrame que contém as informações para serem visualizadas
        nos gráficos de linha.
        """
        dfs_casos = {}
        for c in self.casos:
            dfs_casos[c.nome] = self.__gera_df_valores_anuais_medios_caso(c)
        
        dfs_inverso = {}
        chaves = []
        for caso in dfs_casos:
            df_orig = dfs_casos[caso]
            chaves = df_orig.columns.tolist()
            for column in df_orig:
                dfs_inverso[(caso,column)] = df_orig[column]
            
        dfs_anual = {}
        for chave in chaves:
            df_novo = pd.DataFrame()
            df_novo.index.name = "data"
            for caso in dfs_casos:
                df_novo.index =  dfs_inverso[(caso,chave )].index
                df_novo["tipo"] = chave
                df_novo = pd.concat([df_novo, dfs_inverso[(caso, chave)].rename(caso)],axis = 1) 
            
            dfs_anual[chave] = df_novo
        
        df_completo = pd.concat(dfs_anual)
        return df_completo
        
    @property
    def df_valores_anuais_medios(self) -> pd.DataFrame:
        if self.__df_valores_anuais_medios is None:
            self.__df_valores_anuais_medios = self.gera_df_valores_anuais_medios()
        return self.__df_valores_anuais_medios


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
