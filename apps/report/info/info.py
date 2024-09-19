from apps.report.info.geral.infoGeral import InfoGeral

class Info():
    def __init__(self, data, nome_argumento_info):
        self.text_html = None
        if(nome_argumento_info == "Estudo"):
            info = InfoGeral(data, nome_argumento_info)
            self.text_html = info.text_html
        else:
            print("NOME DO ARGUMENTO INFO NAO RECONHECIDO")
            exit(1)
        