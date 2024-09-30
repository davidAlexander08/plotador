class Estruturas:
    def __init__(self):


        self.Tabela_Operacao = """
        <table>
        <tr>
            <th>Caso</th>
            <th>Modelo</th>
            <th>Versao</th>
            <th>Politica (min)</th>
            <th>SF (min)</th>
            <th>Total (min)</th>
            <th>Iter</th>
            <th>Zinf</th>
            <th>Custo Total</th>
            <th>Desvio Custo</th>
        </tr>
    """      

        self.template_Tabela_Operacao = """
        <tr>
            <td>Caso</td>
            <td>Modelo</td>
            <td>Versao</td>
            <td>tempo_politica</td>
            <td>tempo_sf</td>
            <td>tempo_total</td>
            <td>iteracoes</td>
            <td>zinf</td>
            <td>custo_total</td>
            <td>desvio_custo</td>
        </tr>
    """     