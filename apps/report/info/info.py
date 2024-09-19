from apps.report.info.geral.infoGeral import InfoGeral

class Info():
    def __init__(self, data, par_dados):
        self.text_html = None
        if(par_dados[0] == "Estudo"):
            info = InfoGeral(data, par_dados)
            self.text_html = info.text_html
        else:
            print("NOME DO ARGUMENTO INFO NAO RECONHECIDO")
            exit(1)
        