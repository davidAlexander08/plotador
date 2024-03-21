
class UnidadeSintese:    
    def __init__(self, sintese, legendaEixoX, titulo, fitroColuna = None, filtroArgumento = None, df = None):
        self.sintese = sintese
        self.legendaEixoY = self.label_y(sintese)     
        self.legendaEixoX = legendaEixoX
        self.titulo = titulo
        self.df = df
        self.fitroColuna = fitroColuna
        self.filtroArgumento = filtroArgumento
        self.__mapa_sintese_label_y =        {
            "GTER":"MWmes",
            "GHID":"MWmes",
            "EARPF":"%",
            "COP":"R$",
            "EARMF":"MWmes",
            "CMO":"R$/MWh",
            "QTUR":"m3/s",
            "QDEF":"m3/s",
            "VVMINOP":"MWmed",
        }
    def label_y(self, sintese):
        operacional = sintese.split("_")[0]
        return self.__mapa_sintese_label_y[operacional]



