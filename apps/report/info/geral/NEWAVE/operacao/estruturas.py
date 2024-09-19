class Estruturas:
    def __init__(self):


        self.Tabela_Operacao_NEWAVE = """
        <table>
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

        self.template_Tabela_Operacao_NEWAVE = """
        <tr>
            <tr>Caso</tr>
            <tr>Modelo</tr>
            <tr>tempo_total</tr>
            <tr>iteracoes</tr>
            <tr>zinf</tr>
            <tr>custo_total</tr>
            <tr>desvio_custo</tr>
        </tr>
    """     