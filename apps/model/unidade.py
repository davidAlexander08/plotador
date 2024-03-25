from apps.model.sintese import Sintese

class UnidadeSintese:  
    def label_y(self, sintese):
        operacional = sintese.split("_")[0]
        return self.__mapa_sintese[operacional][0]

    def titulo_fig(self, sintese):
        operacional = sintese.split("_")[0]
        espacial = sintese.split("_")[1]
        return self.__mapa_sintese[operacional][1]+" "+espacial
        
    def __init__(self, sintese, legendaEixoX, argumento, df = None):
        self.sintese = sintese.sintese
        self.legendaEixoX = legendaEixoX
        self.df = df
        self.fitroColuna = sintese.filtro
        self.filtroArgumento = argumento.nome
        self.__mapa_sintese =        {
            "GTER":    ("MWmes","Geração Térmica"),
            "GHID":    ("MWmes","Geração Térmica"),
            "EARPF":    ("%","Energ. Armz. Perc."),
            "COP":    ("R$","Custo de Oper."),
            "EARMF":    ("MWmes","Energ. Armz. Final"),
            "CMO":    ("R$/MWh","Custo Marg."),
            "QTUR":    ("m3/s", "Vaz. Turb."),
            "QDEF":    ("m3/s", "Vaz. Defl."),
            "VVMINOP":    ("MWmed", "Viol. VMINOP"),
            "CDEF":    ("10^6 R$", "Custo de Deficit"),
            "CONVERGENCIA":    ("10^3 R$", "Convergencia"),
            "CTER":    ("10^6 R$", "Custo Térmica"),
            "DEF":    ("MWmes", "Deficit"),
            "EARPI":    ("%", "Energ. Armz. Perc Ini."),
            "EARMI":    ("MWmes", "Energ. Armz. Ini."),
            "EEVAP":    ("MWmes", "Energ. Evap."),
            "ENAA":    ("MWmes", "Energ. Natu. Afl."),
            "ENAAF":    ("MWmes", "Energ. Natu. Afl. Final"),
            "EVER":    ("MWmes", "Energ. Vertida"),
            "EVERF":    ("MWmes", "Energ. Vertida Final"),
            "EXC":    ("MWmes", "Excesso"),
        }

        self.legendaEixoY = self.label_y(sintese.sintese)     
        self.titulo = self.titulo_fig(sintese.sintese) if argumento.nome == None else self.titulo_fig(sintese.sintese) + " " + argumento.nome


