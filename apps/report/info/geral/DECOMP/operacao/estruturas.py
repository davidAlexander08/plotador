class Estruturas:
    def __init__(self):


        self.Tabela_Operacao = """
        <table class="exportTable">
        <tr>
            <th>Caso</th> 
            <th>Modelo</th>
            <th>Versao</th>
            <th>Zinf</th>
            <th>Zsup</th>
            <th>Gap</th>
            <th>Iter</th>
            <th>Tempo</th>
            <th>Custo_P. (avg)</th>
            <th>Custo_Fut. (avg)</th>
            <th>CMO_SE (1 est)</th>
            <th>CMO_SE (1 est)</th>
        </tr>
    """      

        self.template_Tabela_Operacao = """
        <tr>
            <td>Caso</td> 
            <td>Modelo</td>
            <td>Versao</td>
            <td>Zinf</td>
            <td>Zsup</td>
            <td>Gap</td>
            <td>Iter</td>
            <td>Tempo</td>
            <td>Custo_P. (avg)</td>
            <td>Custo_Fut. (avg)</td>
            <td>CMO_SE (1 est)</td>
            <td>CMO_SE (1 est)</td>
        </tr>
    """     