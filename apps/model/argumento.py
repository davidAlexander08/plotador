from typing import Dict


class Argumento:
    """
    Classe base que representa um argumento do estudo
    que será utilizado para o cálculo de indicadores
    e para geração de gráficos.
    """

    def __init__(self, listaNomes, chave):
        self.listaNomes = listaNomes  
        self.chave = chave

    @classmethod
    def from_dict(cls, d: Dict[str, str]):
        key = list(d.keys())[0]
        arg = d[key]
        if isinstance(arg, list):
           return cls(arg, key)
        else:
            return cls([arg], key)
