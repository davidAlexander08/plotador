from typing import Dict
from apps.model.unidadeArgumental import UnidadeArgumental

class Argumento:
    """
    Classe base que representa um argumento do estudo
    que será utilizado para o cálculo de indicadores
    e para geração de gráficos.
    """

    def __init__(self, listaNomes, chave):
        self.listaNomes = listaNomes  
        self.chave = chave

        col = 1
        lin = 1
        pTitulo = 0
        coord_max = (1,1)
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
        listaUArg = []
        for nome in listaNomes:
            print(nome, " col: ", col, " lin: ", lin, " ", pTitulo)
            uArg = UnidadeArgumental(nome,col, lin, pTitulo)
            listaUArg.append(uArg)
            col += 1
            if(col > coord_max[0]):
                col = 1
                lin += 1
            pTitulo += 1
        self.listaUArg = listaUArg


    @classmethod
    def from_dict(cls, d: Dict[str, str]):
        key = list(d.keys())[0]
        arg = d[key]
        if isinstance(arg, list):
           return cls(arg, key)
        else:
            return cls([arg], key)
