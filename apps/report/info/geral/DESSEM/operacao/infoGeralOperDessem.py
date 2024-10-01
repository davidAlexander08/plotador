
from apps.report.info.geral.DESSEM.operacao.estruturas import Estruturas
from apps.indicadores.eco_indicadores import EcoIndicadores
from idessem.dessem.des_log_relato import DesLogRelato
import os

class InfoGeralOperDessem(Estruturas):
    def __init__(self, data):
        Estruturas.__init__(self)
        self.eco_indicadores = EcoIndicadores(data.conjuntoCasos[0].casos)
        self.lista_text = []
        self.lista_text.append(self.Tabela_Operacao)
        for caso in data.conjuntoCasos[0].casos:
            if(caso.modelo == "DESSEM"):
                temp = self.preenche_operacao(caso)
                self.lista_text.append(temp)
        self.lista_text.append("</table>"+"\n")
        self.text_html = "\n".join(self.lista_text)

    def preenche_operacao(self,caso):

        temp = self.template_Tabela_Operacao
        temp = temp.replace("Caso", caso.nome)
        temp = temp.replace("Modelo", caso.modelo)
        if(os.path.isfile(caso.caminho+"/DES_LOG_RELATO.DAT")):
            data_des_log = DesLogRelato.read(caso.caminho+"/DES_LOG_RELATO.DAT")
            temp = temp.replace("Tempo", str(data_des_log.tempo_processamento))
            otim = data_des_log.variaveis_otimizacao
            #print(data_des_log.variaveis_otimizacao)

            colunas = otim.loc[(otim["variavel"] == "Funcao objetivo do Problema Linear (FOBJ)")]
            #print(colunas)

            custo_real                  = otim.loc[(otim["variavel"] == "Funcao objetivo do Problema Linear (FOBJ)")]["valor"].iloc[0]
            parcela_custo_presente      = otim.loc[(otim["variavel"] == "Parcela de custo presente")]["valor"].iloc[0]            
            parcela_Custo_Futuro        = otim.loc[(otim["variavel"] == "Parcela de custo Futuro")]["valor"].iloc[0]            
            custo_viol_restr            = otim.loc[(otim["variavel"] == "Custo de violacao de restricoes")]["valor"].iloc[0]            
            #custo_pequenas_penalidades  = otim.loc[(otim["variavel"] == "Custo de pequenas penalidades")]["valor"].iloc[0]            
            #gap_max_otim                = otim.loc[(otim["variavel"] == "Gap Maximo de Otimalidade")]["valor"].iloc[0]            

            temp = temp.replace("Custo Total",          str(custo_real))
            temp = temp.replace("Custo Presente",       str(parcela_custo_presente))
            temp = temp.replace("Custo Futuro",         str(parcela_Custo_Futuro))
            temp = temp.replace("Custo Viol",           str(custo_viol_restr))
            #temp = temp.replace("Custo Peq. Penalid",   str(custo_pequenas_penalidades))
            #temp = temp.replace("Max Gap Otim",         str(gap_max_otim))
        return temp

