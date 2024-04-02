from apps.model.sintese import Sintese
from apps.model.argumento import Argumento
from apps.interface.metaData import MetaData
from apps.model.unidade import UnidadeSintese
from apps.model.unidadeArgumental import UnidadeArgumental
class ConjuntoUnidadeSintese (MetaData):  

    def __init__(self, sintese, arg, legendaEixoX, limSup = False, limInf = False, tamanho_texto = 11):
        MetaData.__init__(self)
        self.arg = arg
        self.sintese = sintese
        self.legendaEixoX = legendaEixoX
        self.limSup = limSup
        self.limInf = limInf
        self.tamanho_texto = tamanho_texto
        self.titulo = self.titulo_fig(sintese.sintese)+" SIN" if arg.listaNomes is None else self.titulo_fig(sintese.sintese) + "_"+ arg.nome
        self.legendaEixoY = self.label_y(sintese.sintese) 

        if(arg.listaUArg is not None):
            self.listaUnidades = []
            for uarg in arg.listaUArg:
                self.listaUnidades.append(UnidadeSintese(sintese, uarg) )
        else:
            self.listaUnidades = [UnidadeSintese(sintese, UnidadeArgumental(None)) ]

    def label_y(self, sintese):
        operacional = sintese.split("_")[0]
        return self.mapa_sintese[operacional][0]

    def titulo_fig(self, sintese):
        operacional = sintese.split("_")[0]
        espacial = sintese.split("_")[1]
        return self.mapa_sintese[operacional][1]+" "+espacial 