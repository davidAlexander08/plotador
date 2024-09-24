
from apps.report.info.geral.DESSEM.operacao.estruturas import Estruturas
from apps.indicadores.eco_indicadores import EcoIndicadores
from idessem.dessem.des_log_relato import DesLogRelato

from inewave.newave import Pmo
from inewave.newave import Dger
from inewave.newave import Cvar


class InfoGeralOperDessem(Estruturas):
    def __init__(self, data):
        Estruturas.__init__(self)
        self.eco_indicadores = EcoIndicadores(data.casos)
        self.lista_text = []
        self.lista_text.append(self.Tabela_Operacao)
        for caso in data.casos:
            if(caso.modelo == "DESSEM"):
                temp = self.preenche_operacao(caso)
                self.lista_text.append(temp)
        self.lista_text.append("</table>"+"\n")
        self.text_html = "\n".join(self.lista_text)

    def preenche_operacao(self,caso):

        temp = self.template_Tabela_Operacao
        temp = temp.replace("Caso", caso.nome)
        temp = temp.replace("Modelo", caso.modelo)
        data_des_log = DesLogRelato.read(caso.caminho+"/DES_LOG_RELATO.DAT")
        temp = temp.replace("Tempo", str(data_des_log.tempo_processamento))
        otim = data_des_log.variaveis_otimizacao
        print(data_des_log.variaveis_otimizacao)

        colunas = otim.loc[(otim["variavel"] == "Funcao objetivo do Problema Linear (FOBJ)")]
        print(colunas)

        custo_real                  = otim.loc[(otim["variavel"] == "Funcao objetivo do Problema Linear (FOBJ)")]["valor"]
        parcela_custo_presente      = otim["Parcela de custo presente"]
        parcela_Custo_Futuro        = otim["Parcela de custo Futuro"]
        custo_viol_restr            = otim["Custo de violacao de restricoes"]
        custo_pequenas_penalidades  = otim["Custo de pequenas penalidades"]
        gap_max_otim                = otim["Gap Maximo de Otimalidade"]

        temp = temp.replace("Custo Total",          str(custo_real))
        temp = temp.replace("Custo Presente",       str(parcela_custo_presente))
        temp = temp.replace("Custo Futuro",         str(parcela_Custo_Futuro))
        temp = temp.replace("Custo Viol",           str(custo_viol_restr))
        temp = temp.replace("Custo Peq. Penalid",   str(custo_pequenas_penalidades))
        temp = temp.replace("Max Gap Otim",         str(gap_max_otim))

        
        #    <td>Caso</td>
        #    <td>Modelo</td>
        #    <td>Tempo</td>
        #    <td>Custo Total</td>
        #    <td>Custo Presente</td>
        #    <td>Custo Futuro</td>
        #    <td>Custo Viol</td>
        #    <td>Custo Peq. Penalid</td>
        #    <td>Max Gap Otim</td>



       #df_temp = self.eco_indicadores.retorna_df_concatenado("TEMPO")
       #temp = self.template_Tabela_Operacao_NEWAVE
       #temp = temp.replace("Caso", caso.nome)
       #temp = temp.replace("Modelo", caso.modelo)
       #data_pmo = Pmo.read(caso.caminho+"/pmo.dat")
       #print(caso.caminho)
       #data_dger = Dger.read(caso.caminho+"/dger.dat")
       #data_cvar = Cvar.read(caso.caminho+"/cvar.dat")

       #df_caso = df_temp.loc[(df_temp["caso"] == caso.nome)]
       #tempo_politica = df_caso.loc[(df_caso["etapa"] == "Calculo da Politica")]["tempo"].iloc[0]/60
       #tempo_sf = df_caso.loc[(df_caso["etapa"] == "Simulacao Final")]["tempo"].iloc[0]/60
       #tempo_total = df_caso.loc[(df_caso["etapa"] == "Tempo Total")]["tempo"].iloc[0]/60

       #iteracoes = data_pmo.convergencia["iteracao"].iloc[-1]
       #zinf = data_pmo.convergencia["zinf"].iloc[-1]
       #custo_total = data_pmo.custo_operacao_total
       #desvio_custo = data_pmo.desvio_custo_operacao_total*1.96

       #temp = temp.replace("tempo_politica", str(round(tempo_politica, 2)))
       #temp = temp.replace("tempo_sf", str(round(tempo_sf, 2)))
       #temp = temp.replace("tempo_total", str(round(tempo_total, 2)))
       #temp = temp.replace("iteracoes", str(iteracoes))
       #temp = temp.replace("zinf", str(zinf))
       #temp = temp.replace("custo_total", str(custo_total))
       #temp = temp.replace("desvio_custo", str(round(desvio_custo, 2)))
        return temp

