
class UnidadeSintese:  
    def label_y(self, sintese):
        operacional = sintese.split("_")[0]
        return self.__mapa_sintese_label_y[operacional]

    def titulo_fig(self, sintese):
        operacional = sintese.split("_")[0]
        espacial = sintese.split("_")[1]
        return self.__mapa_sintese_titulo[operacional]+" "+espacial
        
    def __init__(self, sintese, legendaEixoX, titulo, fitroColuna = None, filtroArgumento = None, df = None):
        self.sintese = sintese
        self.legendaEixoY = self.label_y(sintese)     
        self.legendaEixoX = legendaEixoX
        self.titulo = self.titulo_fig(sintese)
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

        self.__mapa_sintese_titulo =        {
            "GTER":"Geração Térmica",
            "GHID":"Geração Hidrelétrica",
            "EARPF":"Energ. Armz. Perc.",
            "COP":"Custo de Oper.",
            "EARMF":"Energ. Armz.",
            "CMO":"Custo Marg.",
            "QTUR":"Vaz. Turb.",
            "QDEF":"Vaz. Defl.",
            "VVMINOP":"Viol. VMINOP",
        }




