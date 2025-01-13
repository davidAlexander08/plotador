from apps.model.unidadeArgumental import UnidadeArgumental 

class UnidadeSintese ():   
    def __init__(self, sintese, uArg):
        self.arg = uArg 
        self.sintese = sintese
        self.titulo = " " if self.arg.nome is None else self.arg.nome 
            


