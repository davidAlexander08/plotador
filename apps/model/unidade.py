from apps.model.sintese import Sintese
from apps.model.argumento import Argumento
from apps.model.metaData import MetaData

class UnidadeSintese (MetaData):  
    def label_y(self, sintese):
        operacional = sintese.split("_")[0]
        return self.__mapa_sintese[operacional][0]

    def titulo_fig(self, sintese):
        operacional = sintese.split("_")[0]
        espacial = sintese.split("_")[1]
        return self.__mapa_sintese[operacional][1]+" "+espacial
        
    def __init__(self, sintese, legendaEixoX, argumento, df = None):
        MetaData.__init__(self)
        self.sts = sintese
        self.arg = argumento
        self.sintese = sintese.sintese
        self.legendaEixoX = legendaEixoX
        self.df = df
        self.fitroColuna = sintese.filtro
        self.filtroArgumento = argumento.nome


        self.legendaEixoY = self.label_y(sintese.sintese)     
        self.titulo = self.titulo_fig(sintese.sintese) if argumento.nome == None else self.titulo_fig(sintese.sintese) + " " + argumento.nome


