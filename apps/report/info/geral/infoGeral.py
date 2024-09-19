
from apps.report.info.geral.estruturas import Estruturas
from apps.report.info.geral.NEWAVE.eco.infoGeralEcoNewave import InfoGeralEcoNewave
from apps.report.info.geral.NEWAVE.operacao.infoGeralOperNewave import InfoGeralOperNewave
class InfoGeral(Estruturas):
    def __init__(self, html_file, data):
        Estruturas.__init__(self)
        self.lista_text = []

        ## TABELA JSON
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
        
        ## TABELA ECO
        self.lista_text.append("<h3>Eco Dados Entrada</h3>"+"\n")
        if(caso.modelo == "NEWAVE"):
            self.lista_text.append(InfoGeralEcoNewave(data).text_html)
        if(caso.modelo == "DECOMP"):
            #self.lista_text.append(InfoGeralEcoDecomp(data).text_html)
            pass
        if(caso.modelo == "DESSEM"):
            #self.lista_text.append(InfoGeralEcoDessem(data).text_html)
            pass


        ##TABELA OPER
        self.lista_text.append("<h3>Oper Dados</h3>"+"\n")
        if(caso.modelo == "NEWAVE"):
            self.lista_text.append(InfoGeralOperNewave(data).text_html)
        if(caso.modelo == "DECOMP"):
            #self.lista_text.append(InfoGeralOperDecomp(data).text_html)
            pass
        if(caso.modelo == "DESSEM"):
            #self.lista_text.append(InfoGeralOperDessem(data).text_html)
            pass

        self.text_html = "\n".join(self.lista_text)

