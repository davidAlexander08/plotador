from typing import Dict
from apps.model.unidadeArgumental import UnidadeArgumental
 
class Argumento:
    """
    Classe base que representa um argumento do estudo
    que será utilizado para o cálculo de indicadores
    e para geração de gráficos.
    """

    def __init__(self, listaNomes, chave, nome):
        self.listaNomes = listaNomes  
        self.chave = chave
        self.nome = nome

        col = 1
        lin = 1
        pTitulo = 0
        coord_max = (1,1)
        if(listaNomes is not None): 
            if(len(listaNomes) ==  2): coord_max = (2,1)
            if(len(listaNomes) ==  3): coord_max = (2,2)
            if(len(listaNomes) ==  4): coord_max = (2,2)
            if(len(listaNomes) ==  5): coord_max = (3,2)
            if(len(listaNomes) ==  6): coord_max = (3,2)
            if(len(listaNomes) ==  7): coord_max = (3,3)
            if(len(listaNomes) ==  8): coord_max = (3,3)
            if(len(listaNomes) ==  9): coord_max = (3,3)
            if(len(listaNomes) == 10): coord_max = (4,3)
            if(len(listaNomes) == 11): coord_max = (4,3)
            if(len(listaNomes) == 12): coord_max = (4,3)
            if(len(listaNomes) == 13): coord_max = (4,4)
            if(len(listaNomes) == 14): coord_max = (4,4)
            if(len(listaNomes) == 15): coord_max = (4,4)
            if(len(listaNomes) == 16): coord_max = (4,4)
            if(len(listaNomes) == 17): coord_max = (4,5)
            if(len(listaNomes) == 18): coord_max = (4,5)
            if(len(listaNomes) == 19): coord_max = (4,5)
            if(len(listaNomes) == 20): coord_max = (4,5)
            if(len(listaNomes) == 21): coord_max = (4,6)
            if(len(listaNomes) == 22): coord_max = (4,6)
            if(len(listaNomes) == 23): coord_max = (4,6)
            if(len(listaNomes) == 24): coord_max = (4,6)
            if(len(listaNomes) == 25): coord_max = (4,6)
            listaUArg = []
            for nome in listaNomes:
                #print(nome, " col: ", col, " lin: ", lin, " ", pTitulo)
                uArg = UnidadeArgumental(nome,col, lin, pTitulo)
                listaUArg.append(uArg)
                col += 1
                if(col > coord_max[0]):
                    col = 1
                    lin += 1
                pTitulo += 1
            self.listaUArg = listaUArg
            self.max_col = coord_max[0]
            self.max_lin = coord_max[1]
        else:
            self.listaUArg = None
            self.max_col = 1
            self.max_lin = 1

    @classmethod
    def from_dict(cls, d: Dict[str, str]):
        arg = d["args"]
        if isinstance(arg, list):
           return cls(arg, d["chave"], d["nome"])
        else:
            return cls([arg], d["chave"], d["nome"])
