from apps.model.unidadeArgumental import UnidadeArgumental 

class UnidadeSintese ():  
    def __init__(self, sintese, uArg):
        self.arg = uArg
        self.fitroColuna = sintese.filtro
        self.sintese = sintese.sintese
        self.filtroArgumento = uArg.nome
        self.titulo = " " if self.arg.nome is None else self.arg.nome 
            


