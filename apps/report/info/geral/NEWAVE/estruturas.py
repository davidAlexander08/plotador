class Estruturas:
    def __init__(self):



        #TABELA DE INFORMACOES BASICAS
        self.Tabela_Eco_Entrada = """
        <table>
        <tr>
            <th>Caso</th>
            <th>Modelo</th>
            <th>Versao</th>
            <th>Mes I</th>
            <th>Ano I</th>
            <th>Anos Pos</th>
            <th>It Max</th>
            <th>It Min</th>
            <th>FW</th>
            <th>BK</th>
            <th>FW SF</th>
            <th>SF Ind</th>
            <th>CVAR</th>
        </tr>
"""


        self.Tabela_Operacao_NEWAVE = """
        <tr>
            <th>Caso</th>
            <th>Modelo</th>
            <th>Temp. Tot(min)</th>
            <th>Iter</th>
            <th>Zinf</th>
            <th>Custo Total</th>
            <th>Desvio Custo</th>
        </tr>
    """      


        self.template_Tabela_Eco_Entrada = """
        <tr>
            <td>Caso</td>
            <td>Modelo</td>
            <td>Versao</td>
            <td>Mes_I</td>
            <td>Ano_I</td>
            <td>Anos_Pos</td>
            <td>It_Max</td>
            <td>It_Min</td>
            <td>FW</td>
            <td>BK</td>
            <td>N_series_sim_final</td>
            <td>SF_Ind</td>
            <td>CVAR</td>
        </tr>
"""

