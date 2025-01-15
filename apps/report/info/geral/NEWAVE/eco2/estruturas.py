class Estruturas:
    def __init__(self):



        #TABELA DE INFORMACOES BASICAS
        self.Tabela_Eco_Entrada = """
        <table>
        <tr>
            <th>Caso</th>
            <th>Modelo</th>
            <th>Flag_CVAR</th>
            <th>Flag_PARP</th>
            <th>Anos Pos</th>
            <th>FPH</th>
            <th>FCF_POS</th>
            <th>Restr_Elet</th>
            <th>RHQ</th>
            <th>RHV</th>
            <th>XXX</th>
            <th>XXX</th>
        </tr>
"""


        self.template_Tabela_Eco_Entrada = """
        <tr>
            <td>Caso</td>
            <td>Modelo</td>
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

