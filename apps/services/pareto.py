from typing import Dict
from apps.model.unidade import UnidadeSintese
from apps.graficos.graficos import Graficos
from apps.model.caso import Caso
from apps.model.sintese import Sintese
from apps.model.argumento import Argumento
import os
import json
from apps.indicadores.indicadores_medios import IndicadoresMedios

class Pareto:
    
    def __init__(self, arquivo_json):
        with open(arquivo_json, "r") as f:
            dados = json.load(f)
        # Lê dados de entrada
        self.estudo = dados["estudo"]
        self.nome_caso_referencia = dados["nome_caso_referencia"]
        # Cria objetos do estudo
        casos = [Caso.from_dict(d) for d in dados["casos"]]        
        indicadores_medios = IndicadoresMedios(casos, self.nome_caso_referencia)
        self.graficos = Graficos(casos)
        # Gera saídas do estudo
        diretorio_saida = f"resultados/{self.estudo}/pareto"
        os.makedirs(diretorio_saida, exist_ok=True)
        self.executa(diretorio_saida)



    def executa(self, diretorio_saida_arg):
        self.graficos.gera_pareto_fast(
            self.indicadores_medios.retorna_df_concatenado("CTER_SIN_EST"),
            self.indicadores_medios.retorna_df_concatenado("EARPF_SIN_EST"), 
            self.indicadores_medios.retorna_df_std_concatenado("CTER_SIN_EST"),
            self.indicadores_medios.retorna_df_std_concatenado("EARPF_SIN_EST"), 
            "CGT SIN Med (MiR$)",
            "EARPF SIN Med (%)",          
            #100,
            #0,
            #self.indicadores_medios.retorna_df_concatenado("CTER_SIN_EST")["valor"].max() * 1.5,
            #0,
            None,
            None,
            None,
            None,
            "Fronteira de Pareto: EARP x CGT - "+self.estudo
        ).write_image(
            os.path.join(diretorio_saida, "Newave_pareto_EARPF_CGT"+self.estudo+".png"),
            width=800,
            height=600,
        )

        self.graficos.gera_pareto_fast(
            self.indicadores_medios.retorna_df_concatenado("GTER_SIN_EST"),
            self.indicadores_medios.retorna_df_concatenado("EARPF_SIN_EST"), 
            self.indicadores_medios.retorna_df_std_concatenado("GTER_SIN_EST"),
            self.indicadores_medios.retorna_df_std_concatenado("EARPF_SIN_EST"), 
            "GT SIN Med (MWmes)",
            "EARPF SIN Med (%)",          
            #100,
            #0,
            #self.indicadores_medios.retorna_df_concatenado("CTER_SIN_EST")["valor"].max() * 1.5,
            #0,
            None,
            None,
            None,
            None,
            "Fronteira de Pareto: EARP x GT - "+self.estudo
        ).write_image(
            os.path.join(diretorio_saida, "Newave_pareto_EARPF_GT"+self.estudo+".png"),
            width=800,
            height=600,
        )

        self.graficos.gera_pareto_fast(
            self.indicadores_medios.retorna_df_concatenado("GTER_SIN_EST"),
            self.indicadores_medios.retorna_df_concatenado("EARMF_SIN_EST"), 
            self.indicadores_medios.retorna_df_std_concatenado("GTER_SIN_EST"),
            self.indicadores_medios.retorna_df_std_concatenado("EARMF_SIN_EST"), 
            "GT SIN Med (MWmes)",
            "EARM SIN Med (MWmes)",          
            #100,
            #0,
            #self.indicadores_medios.retorna_df_concatenado("CTER_SIN_EST")["valor"].max() * 1.5,
            #0,
            None,
            None,
            None,
            None,
            "Fronteira de Pareto: EARM x GT - "+self.estudo
        ).write_image(
            os.path.join(diretorio_saida, "Newave_pareto_EARM_GT"+self.estudo+".png"),
            width=800,
            height=600,
        )

        self.graficos.gera_pareto_fast(
            self.indicadores_medios.retorna_df_concatenado("CTER_SIN_EST"),
            self.indicadores_medios.retorna_df_concatenado("EARMF_SIN_EST"), 
            self.indicadores_medios.retorna_df_std_concatenado("CTER_SIN_EST"),
            self.indicadores_medios.retorna_df_std_concatenado("EARMF_SIN_EST"), 
            "CGT SIN Med (Mi R$)",
            "EARM SIN Med (MWmes)",          
            #100,
            #0,
            #self.indicadores_medios.retorna_df_concatenado("CTER_SIN_EST")["valor"].max() * 1.5,
            #0,
            None,
            None,
            None,
            None,
            "Fronteira de Pareto: EARM x CGT - "+self.estudo
        ).write_image(
            os.path.join(diretorio_saida, "Newave_pareto_EARM_CGT"+self.estudo+".png"),
            width=800,
            height=600,
        )


        eixoY_temp = self.indicadores_medios.retorna_df_concatenado("CDEF_SIN_EST")["valor"].max()*1.5
        eixoY_sup =  eixoY_temp if eixoY_temp > 500 else 500
        self.graficos.gera_pareto_fast(
            self.indicadores_medios.retorna_df_concatenado("CTER_SIN_EST"), 
            self.indicadores_medios.retorna_df_concatenado("CDEF_SIN_EST"),
            self.indicadores_medios.retorna_df_std_concatenado("CTER_SIN_EST"),
            self.indicadores_medios.retorna_df_std_concatenado("CDEF_SIN_EST"), 
            "Custo GT (MiR$)",
            "Custo DEF (MiR$)",
            #eixoY_sup,
            #-20,
            None,
            None,
            #self.indicadores_medios.retorna_df_concatenado("CTER_SIN_EST")["valor"].max()*2,
            #0,
            None,
            None,
            "Fronteira de Pareto: Custo GT x Custo DEF - "+self.estudo
        ).write_image(
            os.path.join(diretorio_saida, "Newave_pareto_CGT_CDEF"+self.estudo+".png"),
            width=800,
            height=600,
        )




        #self.graficos.gera_pareto_fast(
        #    self.indicadores_medios.retorna_DF_cenario_medio_incremental_percentual("EARPF_SIN_EST", dropar = False),
        #    self.indicadores_medios.retorna_df_concatenado("CTER_SIN_EST"), 
        #    self.indicadores_medios.retorna_DF_std_incremental_percentual("EARPF_SIN_EST", dropar = False),
        #    self.indicadores_medios.retorna_df_std_concatenado("CTER_SIN_EST"), 
        #    "Ganho EARPF SIN Med (%)",
        #    "Custo GT (R$)",
        #    self.indicadores_medios.retorna_df_concatenado("CTER_SIN_EST")["valor"].max()*1.5,
        #    0,
        #    None,
        #    None,
        #    "Fronteira de Pareto: Ganho EARPF x Custo GT - "+self.estudo
        #).write_image(
        #    os.path.join(diretorio_saida, "Newave_pareto_ganhoEarm_CGT"+self.estudo+".png"),
        #    width=800,
        #    height=600,
        #)



        


        #self.graficos.gera_pareto_fast(
        #    self.indicadores_medios.retorna_DF_cenario_medio_incremental_percentual("EARPF_SIN_EST", dropar = False),
        #    self.indicadores_medios.retorna_DF_cenario_medio_incremental_percentual("CTER_SIN_EST", dropar = False),
        #    self.indicadores_medios.retorna_DF_std_incremental_percentual("EARPF_SIN_EST", dropar = False),
        #    self.indicadores_medios.retorna_DF_std_incremental_percentual("CTER_SIN_EST", dropar = False), 
        #    "Ganho EARPF (MWmes)",
        #    "Ganho CT (R$)",
        #    None,
        #    None,
        #    None,
        #    None,
        #    "Fronteira de Pareto: Ganho EARPF x ganho CT - "+self.estudo
        #).write_image(
        #    os.path.join(diretorio_saida, "Newave_pareto_ganhoEarpf_ganhoct"+self.estudo+".png"),
        #    width=800,
        #    height=600,
        #)
      
