from apps.model.unidadeArgumental import UnidadeArgumental 

class UnidadeSintese ():  
    def __init__(self, sintese, uArg):
        self.arg = uArg
        self.fitroColuna = sintese.filtro
        self.sintese = sintese.sintese
        self.filtroArgumento = uArg.nome
        self.titulo = self.arg.nome
            


