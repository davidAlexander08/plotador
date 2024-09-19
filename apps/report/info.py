from apps.report.infoGeral import InfoGeral

class Info():
    def __init__(self, html_file, data, nome_argumento_info):
        self.text_html = None
        if(nome_argumento_info == "Geral"):
            info = InfoGeral(self, html_file, data)
            self.text_html = info.text_html
        else:
            print("NOME DO ARGUMENTO INFO NAO RECONHECIDO")
            exit(1)
        