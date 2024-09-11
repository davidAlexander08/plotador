class Estruturas:
    def __init__(self):

        #TABELA DE INFORMACOES BASICAS
        Tabela_Eco_Entrada = """
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


        Tabela_Operacao_NEWAVE = """
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
        self.mapa_tabela_modelo["NEWAVE"] = Tabela_Eco_Entrada
        self.mapa_tabela_modelo["DECOMP"] = Inicio_tabela_Decomp

        template_Tabela_Eco_Entrada = """
        <tr>
            <th>Caso</th>
            <th>Modelo</th>
            <th>Versao</th>
            <th>Mes_I</th>
            <th>Ano_I</th>
            <th>Anos_Pos</th>
            <th>It_Max</th>
            <th>It_Min</th>
            <th>FW</th>
            <th>BK</th>
            <th>N_series_sim_final</th>
            <th>SF_Ind</th>
            <th>CVAR</th>
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
        self.mapa_template_tabela_modelo["NEWAVE"] = template_Tabela_Eco_Entrada
        self.mapa_template_tabela_modelo["DECOMP"] = Template_tabela_caso_Decomp