class Estruturas:
    def __init__(self):

        Inicio_tabela_Newave = """
        <table>
        <tr>
            <th>Caso</th>
            <th>Modelo</th>
            <th>Versao</th>
            <th>Tempo Total (min)</th>
            <th>Iter</th>
            <th>Zinf</th>
            <th>Custo Total</th>
            <th>Desvio Custo</th>
        </tr>
    """      

        Inicio_tabela_Decomp = """
    <table>
    <tr>
        <th>Caso</th>
        <th>Modelo</th>
        <th>Versao</th>
        <th>Tempo Total (min)</th>
        <th>Iter</th>
        <th>Zinf</th>
        <th>Custo Total</th>
    </tr>
"""   
        self.mapa_tabela_modelo = {}
        self.mapa_tabela_modelo["NEWAVE"] == Inicio_tabela_Newave
        self.mapa_tabela_modelo["DECOMP"] == Inicio_tabela_Decomp

        Template_tabela_caso_Newave = """
  <tr>
    <td>nome</td>
	<td>modelo</td>
    <td>versao</td>
	<td>tempo_total</td>
    <td>iteracoes</td>
    <td>zinf</td>
    <td>custo_total</td>
    <td>desvio_custo</td>
  </tr>
"""

                      
        Template_tabela_caso_Decomp = """
  <tr>
    <td>nome</td>
	<td>modelo</td>
    <td>versao</td>
	<td>tempo_total</td>
    <td>iteracoes</td>
    <td>zinf</td>
    <td>custo_total</td>
  </tr>
"""
        self.mapa_template_tabela_modelo = {}
        self.mapa_tabela_modelo["NEWAVE"] == Template_tabela_caso_Newave
        self.mapa_tabela_modelo["DECOMP"] == Template_tabela_caso_Decomp