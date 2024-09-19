class Estruturas:
    def __init__(self):

        self.Inicio_tabela = """
<table>
<tr>
<th>Nome do Caso</th>
<th>Caminho</th>
<th>Modelo</th>
<th>Cor</th>
</tr>
"""                         
        self.template_tabela_caso = """
<tr>
<td>nome</td>
<td>caminho</td>
<td>modelo</td>
<td style="background-color: cor;"></td>
</tr>
""" 