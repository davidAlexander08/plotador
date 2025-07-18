from apps.report.info.SBM.NEWAVE.infoSBMNewave import InfoSBMNewave
from apps.report.info.SBM.DESSEM.infoSBMDessem import InfoSBMDessem
from apps.report.info.SBM.DECOMP.infoSBMDecomp import InfoSBMDecomp

class InfoSBM():
    def __init__(self, data, par_dados):
        set_modelos = set()
        for caso in data.conjuntoCasos[0].casos:
            set_modelos.add(caso.modelo)

        self.lista_text = []
        self.lista_text.append("<h3>Dados Submercado</h3>"+"\n")

        for modelo in set_modelos:
            if(modelo == "NEWAVE"):
                self.lista_text.append(InfoSBMNewave(data, par_dados).text_html)
            if(modelo == "DECOMP"):
                self.lista_text.append(InfoSBMDecomp(data, par_dados).text_html)
                pass
            if(modelo == "DESSEM"):
                self.lista_text.append(InfoSBMDessem(data, par_dados).text_html)
                pass

        self.text_html = "\n".join(self.lista_text)

