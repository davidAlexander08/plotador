from apps.report.info.Anual.NEWAVE.infoAnualNewave import InfoAnualNewave
#from apps.report.info.SIN.DESSEM.infoSINDessem import InfoSINDessem
#from apps.report.info.SIN.DECOMP.infoSINDecomp import InfoSINDecomp
class InfoAnual():
    def __init__(self, data, par_dados):
        set_modelos = set()
        for caso in data.conjuntoCasos[0].casos:
            set_modelos.add(caso.modelo)

        self.lista_text = []
        self.lista_text.append("<h2>Dados Anuais da Grandeza</h2>"+"\n")

        for modelo in set_modelos:
            if(modelo == "NEWAVE"):
                self.lista_text.append(InfoAnualNewave(data, par_dados).text_html)
            if(modelo == "DECOMP"):
                #self.lista_text.append(InfoSINDecomp(data).text_html)
                pass
            if(modelo == "DESSEM"):
                #self.lista_text.append(InfoSINDessem(data).text_html)
                pass

        self.text_html = "\n".join(self.lista_text)

