# graficador-newave
A filosofia deste repositório é de gerar gráficos e análises estatísticas automáticas para diferens tipos de casos de Newave, a fim de facilitar e replicar estudos feitos com o modelo. A configuração da análise é definida em um arquivo ".json" na nuvem, o qual é chamado por linha de comando, como, por exemplo:

graficador-newave temporal teste.json

No comando acima, o "graficador-newave" é invocado para realizar a análise "temporal" com base na configuração definida no "teste.json". Dentre as análises atualmente implementadas, encontram-se:

Eco
Temporal
Media
Anual
Cenarios
Conjunto


Eco
A análise Eco tem como objetivo retornar em csv os dataFrames definidos no campo "sinteses" sem nenhuma modificação ou filtro aplicado.

Temporal
A análise Temporal gera tabelas e gráficos com base temporal média, ou seja, para todo o horizonte, apenas para o primeiro ou segundo mês por exemplo. 

Média
A análise média gera tabelas e gráficos médios gerais, usualmente gráficos de barra, também realizando cálculos incrementais com base no caso de referência. 

Anual
A análise anual gera tabelas e gráficos com base anual, por exemplo, considerando apenas o primeiro ano ou a média de outros anos, ou cada ano discretizado.

Cenários
A análise de cenários é focada para analisar os parquets relacionados a ENA e QINC gerados para cada iteração do Newave. Para esse tipo de análise, apenas os parquets "ENAA" ou "QINC" com terminação "FOR" ou "SF" são válidos.

Conjunto
A análise de conjuntos de casos é um diferente das anteriores, um exemplo seria analisar 12 meses de PMO em comparação a outros 12 meses de PMO. A configuração também é diferente, uma vez que todos os casos fazem parte de um conjunto, em que um estudo possui mais de um conjunto. 


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Arquivos json:

O arquivo json possui diferentes campos, podendo alguns serem alterados de acordo com a análise.

Campos principais:
Estudo - Define o nome do estudo realizado
nome_caso_referencia - Define o nome do caso de referência, o qual deve ser igual a algum dos casos indicados. É utilizado para cálculos incrementais. 
casos - É uma lista de casos, em que cada caso tem suas próprias característica como:
    nome: Nome do caso que aparecerá no gráfico,
    caminho: caminho relativo da pasta do arquivo json até o caso,
    cor: cor da linha do gráfico para o caso,
    marcador: marcador para os gráficos de pareto do caso. 
configuração: Caso o usuário deseje escolher alguma configuração de análise dentre as configurações padrões, deverá preencher este campo, caso contrário deixe-o vazio. Algumas das configurações padrões são:
    - sintese: 
    - argumentos:

argumentos: Caso o campo configuração esteja vazio, são lidos os argumentos do campo argumentos, os quais podem ser:
    - UHE: usinas hidrelétricas
    - SBM: Submercado (SUDESTE, NORDESTE, SUL, NORTE)
    - REE: REE (PARANA, PARANAPANEMA...)
    - BCA: Bacias (....)

sintese: Caso o campo configuração esteja vazio, são lidos os argumentos do campo sintese, os quais podem ser:
    - sintese: Nome da síntese a ser avaliada. Caso seja do SIN, ela será executada sem nenhum argumento necessário. 


Exemplo Configuração padrão - Válida para análises ECO, TEMPORAL, MEDIA, ANUAL e CENARIOS

{
    "estudo": "TESTE_GRAFICADOR",
    "nome_caso_referencia": "REE",
    "casos": [
        {
            "nome": "REE",
            "caminho": "FEV21/ree_25x35",
            "cor": "rgba(0, 0, 0, 1.00)",
            "marcador": "square"
        },
        {
            "nome": "25x35",
            "caminho": "FEV21/hib12_25x35",
            "cor": "rgba(66, 179, 245, 0.25)",
            "marcador": "diamond"
        }
    ],
    "configuracao":"Personalizado",
    "argumentos":[
		{"UHE":"JUPIA"},
		{"UHE":"FURNAS"},
		{"REE":"PARANA"},
		{"SBM":"SUDESTE"},
		{"SBM":"NORDESTE"}
    ],
    "sinteses":[
	{"sintese":"GTER_SIN_EST"},
    {"sintese":"GTER_SBM_EST"},
	{"sintese":"GHID_SBM_EST"}

    ]
}


Exemplo Configuração padrão - Válida para análises CONJUNTOS


{
    "estudo": "FCF_Externa_TESTE_GRAFICADOR",
	"conjuntos": [
		{
			"nome_conj":"REE", 
			"cor_conj": "rgba(0, 0, 0, 1.00)",
			"casos": [
				{
					"nome": "JAN",
					"caminho": "2021_Backtest/2021_01_rv0/newave",
					"cor": "rgba(0, 0, 0, 1.00)",
					"marcador": "square"
				},
				{
					"nome": "FEV",
					"caminho": "2021_Backtest/2021_02_rv0/newave",
					"cor": "rgba(255, 255, 0, 1)",
					"marcador": "circle"
				},
				{
					"nome": "MAR",
					"caminho": "2021_Backtest/2021_03_rv0/newave",
					"cor": "rgba(255, 255, 0, 1)",
					"marcador": "circle"
				},
				{
					"nome": "ABR",
					"caminho": "2021_Backtest/2021_04_rv0/newave",
					"cor": "rgba(255, 255, 0, 1)",
					"marcador": "circle"
				},
				{
					"nome": "MAI",
					"caminho": "2021_Backtest/2021_05_rv0/newave",
					"cor": "rgba(255, 255, 0, 1)",
					"marcador": "circle"
				},
				{
					"nome": "JUN",
					"caminho": "2021_Backtest/2021_06_rv0/newave",
					"cor": "rgba(255, 255, 0, 1)",
					"marcador": "circle"
				},
				{
					"nome": "JUL",
					"caminho": "2021_Backtest/2021_07_rv0/newave",
					"cor": "rgba(255, 255, 0, 1)",
					"marcador": "circle"
				},
				{
					"nome": "AGO",
					"caminho": "2021_Backtest/2021_08_rv0/newave",
					"cor": "rgba(255, 255, 0, 1)",
					"marcador": "circle"
				},
				{
					"nome": "SET",
					"caminho": "2021_Backtest/2021_09_rv0/newave",
					"cor": "rgba(255, 255, 0, 1)",
					"marcador": "circle"
				},
				{
					"nome": "OUT",
					"caminho": "2021_Backtest/2021_10_rv0/newave",
					"cor": "rgba(255, 255, 0, 1)",
					"marcador": "circle"
				},
				{
					"nome": "NOV",
					"caminho": "2021_Backtest/2021_11_rv0/newave",
					"cor": "rgba(255, 255, 0, 1)",
					"marcador": "circle"
				},
				{
					"nome": "DEZ",
					"caminho": "2021_Backtest/2021_12_rv0/newave",
					"cor": "rgba(255, 255, 0, 1)",
					"marcador": "circle"
				}
		 
			]
		},
		{
			"nome_conj":"REE_FCFExt", 
			"cor_conj": "rgba(255, 0, 0, 1)",
			"casos": [
				{
					"nome": "JAN",
					"caminho": "2021_Backtest_FCF_Ext/c_2021_01_rv0",
					"cor": "rgba(0, 0, 0, 1.00)",
					"marcador": "square"
				},
				{
					"nome": "FEV",
					"caminho": "2021_Backtest_FCF_Ext/c_2021_02_rv0",
					"cor": "rgba(255, 255, 0, 1)",
					"marcador": "circle"
				},
				{
					"nome": "MAR",
					"caminho": "2021_Backtest_FCF_Ext/c_2021_03_rv0",
					"cor": "rgba(255, 255, 0, 1)",
					"marcador": "circle"
				},
				{
					"nome": "ABR",
					"caminho": "2021_Backtest_FCF_Ext/c_2021_04_rv0",
					"cor": "rgba(255, 255, 0, 1)",
					"marcador": "circle"
				},
				{
					"nome": "MAI",
					"caminho": "2021_Backtest_FCF_Ext/c_2021_05_rv0",
					"cor": "rgba(255, 255, 0, 1)",
					"marcador": "circle"
				},
				{
					"nome": "JUN",
					"caminho": "2021_Backtest_FCF_Ext/c_2021_06_rv0",
					"cor": "rgba(255, 255, 0, 1)",
					"marcador": "circle"
				},
				{
					"nome": "JUL",
					"caminho": "2021_Backtest_FCF_Ext/c_2021_07_rv0",
					"cor": "rgba(255, 255, 0, 1)",
					"marcador": "circle"
				},
				{
					"nome": "AGO",
					"caminho": "2021_Backtest_FCF_Ext/c_2021_08_rv0",
					"cor": "rgba(255, 255, 0, 1)",
					"marcador": "circle"
				},
				{
					"nome": "SET",
					"caminho": "2021_Backtest_FCF_Ext/c_2021_09_rv0",
					"cor": "rgba(255, 255, 0, 1)",
					"marcador": "circle"
				},
				{
					"nome": "OUT",
					"caminho": "2021_Backtest_FCF_Ext/c_2021_10_rv0",
					"cor": "rgba(255, 255, 0, 1)",
					"marcador": "circle"
				},
				{
					"nome": "NOV",
					"caminho": "2021_Backtest_FCF_Ext/c_2021_11_rv0",
					"cor": "rgba(255, 255, 0, 1)",
					"marcador": "circle"
				},
				{
					"nome": "DEZ",
					"caminho": "2021_Backtest_FCF_Ext/c_2021_12_rv0",
					"cor": "rgba(255, 255, 0, 1)",
					"marcador": "circle"
				}
		 
			]
		}
	],
    "argumentos":[
		{"UHE":"JUPIA"},
		{"UHE":"FURNAS"},
		{"REE":"PARANA"},
		{"SBM":"SUDESTE"}
    ],
    "sinteses":[
	{"sintese":"GTER_SIN_EST"},
	{"sintese":"GTER_SBM_EST"},
	{"sintese":"CMO_SBM_EST"},
	{"sintese":"GHID_SIN_EST"},
	{"sintese":"GHID_REE_EST"},
	{"sintese":"QTUR_UHE_EST"}
    ]
}

