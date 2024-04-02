from apps.model.unidadeArgumental import UnidadeArgumental 

class UnidadeSintese ():  
    def __init__(self, filtroColuna, uArg):
        self.arg = uArg
        self.fitroColuna = filtroColuna
        self.filtroArgumento = uArg.nome
        self.titulo = "SIN" if uArg.nome == None else uArg.nome 
            


