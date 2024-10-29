class Estruturas:
    def __init__(self):

        #TABELA DE INFORMACOES BASICAS
        self.Tabela_Eco_Entrada = """
        <table>
        <tr>
            <th>Caso</th>
            <th>Modelo</th>
            <th>Versao</th>
            <th>MILP (min)</th>
            <th>PL_INT_FIX (min)</th>
            <th>Calc_CMO (Min)</th>
            <th>Total (min)</th>
            <th>Status MILP</th>
            <th>Status CalcCMO</th>
        </tr>
"""


        self.template_Tabela_Eco_Entrada = """
        <tr>
            <td>Caso</td>
            <td>Modelo</td>
            <td>Versao</td>
            <td>MILP (min)</td>
            <td>PL_INT_FIX (min)</td>
            <td>Calc_CMO (Min)</td>
            <td>Total (min)</td>
            <td>Status MILP</td>
            <td>Status CalcCMO</td>
        </tr>
"""

