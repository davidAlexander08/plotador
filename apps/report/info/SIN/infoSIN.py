from apps.report.info.SIN.NEWAVE.infoSINNewave import InfoSINNewave
from apps.report.info.SIN.DESSEM.infoSINDessem import InfoSINDessem

class InfoSIN():
    def __init__(self, data, par_dados):
        set_modelos = set()
        for caso in data.conjuntoCasos[0].casos:
            set_modelos.add(caso.modelo)

        self.lista_text = []
        self.lista_text.append("<h3>Dados SIN</h3>"+"\n")

        for modelo in set_modelos:
            if(modelo == "NEWAVE"):
                self.lista_text.append(InfoSINNewave(data).text_html)
            if(modelo == "DECOMP"):
                #self.lista_text.append(InfoGeralEcoDecomp(data).text_html)
                pass
            if(modelo == "DESSEM"):
                self.lista_text.append(InfoSINDessem(data).text_html)
                pass

        self.text_html = "\n".join(self.lista_text)

