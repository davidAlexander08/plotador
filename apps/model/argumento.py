from typing import Dict


class Argumento:
    """
    Classe base que representa um argumento do estudo
    que será utilizado para o cálculo de indicadores
    e para geração de gráficos.
    """

    def __init__(self, nome: str, chave:str):
        self.nome = nome  
        self.chave = chave

    @classmethod
    def from_dict(cls, d: Dict[str, str]):
        key = list(d.keys())[0]
        print(str(key))
        return cls(d[key]["nome"], key)
