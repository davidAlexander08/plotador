from apps.model.sintese import Sintese
from apps.model.argumento import Argumento
from apps.interface.metaData import MetaData
 
class UnidadeSintese (MetaData):  
    def label_y(self, sintese):
        operacional = sintese.split("_")[0]
        return self.mapa_sintese[operacional][0]

    def titulo_fig(self, sintese):
        operacional = sintese.split("_")[0]
        espacial = sintese.split("_")[1]
        return self.mapa_sintese[operacional][1]+" "+espacial
        
    def __init__(self, sintese, legendaEixoX, uArg, limSup = False, limInf = False, tamanho_texto = 11, df = None ):
        MetaData.__init__(self)
        self.sts = sintese
        self.uArg = uArg
        self.sintese = sintese.sintese
        self.legendaEixoX = legendaEixoX
        self.df = df
        self.fitroColuna = sintese.filtro
        self.filtroArgumento = uArg.nome
        self.limSup = limSup
        self.limInf = limInf
        self.tamanho_texto = tamanho_texto


        self.legendaEixoY = self.label_y(sintese.sintese)     
        self.titulo = self.titulo_fig(sintese.sintese) if nomeArgumento == None else self.titulo_fig(sintese.sintese) + "_"+ nomeArgumento


