
from apps.report.info.geral.estruturas import Estruturas
from apps.report.info.geral.NEWAVE.eco.infoGeralEcoNewave import InfoGeralEcoNewave
from apps.report.info.geral.NEWAVE.operacao.infoGeralOperNewave import InfoGeralOperNewave
class InfoGeral(Estruturas):
    def __init__(self, data, par_dados):
        Estruturas.__init__(self)
        self.lista_text = []
        set_modelos = {}

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
            set_modelos.add(caso.modelo)
        self.lista_text.append("</table>"+"\n")
        
        for modelo in set_modelos:
            if(par_dados[1] == "ECO" or par_dados[1] == None):
                ## TABELA ECO
                self.lista_text.append("<h3>Eco Dados Entrada</h3>"+"\n")
                if(modelo == "NEWAVE"):
                    self.lista_text.append(InfoGeralEcoNewave(data).text_html)
                if(modelo == "DECOMP"):
                    #self.lista_text.append(InfoGeralEcoDecomp(data).text_html)
                    pass
                if(modelo == "DESSEM"):
                    #self.lista_text.append(InfoGeralEcoDessem(data).text_html)
                    pass

            if(par_dados[1] == "OPER" or par_dados[1] == None):
                ##TABELA OPER
                self.lista_text.append("<h3>Oper Dados</h3>"+"\n")
                if(modelo == "NEWAVE"):
                    self.lista_text.append(InfoGeralOperNewave(data).text_html)
                if(modelo == "DECOMP"):
                    #self.lista_text.append(InfoGeralOperDecomp(data).text_html)
                    pass
                if(modelo == "DESSEM"):
                    #self.lista_text.append(InfoGeralOperDessem(data).text_html)
                    pass

        self.text_html = "\n".join(self.lista_text)

