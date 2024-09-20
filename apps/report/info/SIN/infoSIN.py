from apps.report.info.SIN.NEWAVE.infoSINNewave import InfoSINNewave


class InfoSIN(Estruturas):
    def __init__(self, data, par_dados):
        Estruturas.__init__(self)
        self.lista_text = []
        self.lista_text.append("<h3>Dados SIN</h3>"+"\n")
        if(caso.modelo == "NEWAVE"):
            self.lista_text.append(InfoSINNewave(data).text_html)
        if(caso.modelo == "DECOMP"):
            #self.lista_text.append(InfoGeralEcoDecomp(data).text_html)
            pass
        if(caso.modelo == "DESSEM"):
            #self.lista_text.append(InfoGeralEcoDessem(data).text_html)
            pass

        self.text_html = "\n".join(self.lista_text)

