
class UnidadeArgumental (): 
    def __init__(self, nome, col = 1, lin = 1, posTitulo = 0):
        self.col = col
        self.lin = lin 
        self.t = posTitulo
        self.nome = nome
        self.titulo = nome if self.nome is None else "SIN"
        self.show = True if posTitulo == 0 else False