from apps.report.info.UHE.NEWAVE.infoUHENewave import InfoUHENewave


class InfoUHE():
    def __init__(self, data, par_dados):
        set_modelos = set()
        for caso in data.casos:
            set_modelos.add(caso.modelo)

        self.lista_text = []
        self.lista_text.append("<h3>Dados Usinas</h3>"+"\n")

        for modelo in set_modelos:
            if(modelo == "NEWAVE"):
                self.lista_text.append(InfoUHENewave(data, par_dados).text_html)
            if(modelo == "DECOMP"):
                #self.lista_text.append(InfoGeralEcoDecomp(data).text_html)
                pass
            if(modelo == "DESSEM"):
                #self.lista_text.append(InfoGeralEcoDessem(data).text_html)
                pass

        self.text_html = "\n".join(self.lista_text)

