from apps.report.info.geral.infoGeral import InfoGeral
from apps.report.info.SIN.infoSIN import InfoSIN
from apps.report.info.SBM.infoSBM import InfoSBM
from apps.report.info.UHE.infoUHE import InfoUHE
from apps.report.info.Execucao.infoExecucao import InfoExecucao
from apps.report.info.valoresUnicos.infoValoresUnicos import InfoValoresUnicos
from apps.report.info.Anual.infoAnual import InfoAnual
from apps.report.info.Cortes.infoCORTES import InfoCORTES
class Info():
    def __init__(self, data, par_dados):
        self.text_html = None
        if(par_dados[0] == "Estudo"):
            info = InfoGeral(data, par_dados)
            self.text_html = info.text_html
        elif(par_dados[0] == "SIN"):
            info = InfoSIN(data, par_dados)
            self.text_html = info.text_html
        elif(par_dados[0] == "SBM"):
            info = InfoSBM(data, par_dados)
            self.text_html = info.text_html
        elif(par_dados[0] == "UHE"):
            info = InfoUHE(data, par_dados)
            self.text_html = info.text_html
        elif(par_dados[0] == "Execucao"):
            info = InfoExecucao(data, par_dados)
            self.text_html = info.text_html
        elif(par_dados[0] == "ValoresUnicos"):
            info = InfoValoresUnicos(data, par_dados)
            self.text_html = info.text_html
        elif(par_dados[0] == "ValoresAnuais"):
            info = InfoAnual(data, par_dados)
            self.text_html = info.text_html
        elif(par_dados[0] == "CORTES"):
            info = InfoCORTES(data, par_dados)
            self.text_html = info.text_html
        else:
            print("NOME DO ARGUMENTO INFO NAO RECONHECIDO")
            exit(1)
        