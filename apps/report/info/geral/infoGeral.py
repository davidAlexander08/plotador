
from apps.report.geral.estruturas import Estruturas
from apps.report.info.geral.NEWAVE.infoGeralNewave import InfoGeralNewave
from apps.indicadores.eco_indicadores import EcoIndicadores
from inewave.newave import Pmo
from inewave.newave import Dger
from inewave.newave import Cvar
from idecomp.decomp import Relato
from idessem.dessem.des_log_relato import DesLogRelato


class InfoGeral(Estruturas):
    def __init__(self, html_file, data):
        Estruturas.__init__(self)
        self.eco_indicadores = EcoIndicadores(data.casos)
        self.lista_text = []
        self.lista_text.append("<h3>Informações Gerais do Estudo</h3>"+"\n")
        self.lista_text.append(self.Inicio_tabela)    
        for caso in data.casos:
            temp = self.template_tabela_caso
            temp = temp.replace("nome", caso.nome)
            temp = temp.replace("caminho", caso.caminho)
            temp = temp.replace("modelo", caso.modelo)
            temp = temp.replace("cor", caso.cor)
            self.lista_text.append(temp)
        self.lista_text.append("</table>"+"\n")
        
        self.lista_text.append("<h2>Eco Dados Entrada</h2>"+"\n")
        
        for caso in data.casos:
            if(caso.modelo == "NEWAVE"):
                info = InfoGeralNewave(data)
                temp = info.text_html
            #if(caso.modelo == "DECOMP"):
            #    if(flag_deco == True):
            #        self.lista_text.append(self.mapa_tabela_modelo[caso.modelo])
            #        flag_deco = False
            #    temp = self.preenche_modelo_tabela_modelo_DECOMP(caso)
            #if(caso.modelo == "DESSEM"):
            #    if(flag_dss == True):
            #        self.lista_text.append(self.mapa_tabela_modelo[caso.modelo])
            #        flag_dss = False
            #    temp = self.preenche_modelo_tabela_modelo_DESSEM(caso)
            self.lista_text.append(temp)
        


        self.text_html = "\n".join(self.lista_text)
