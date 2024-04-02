



from plotly.subplots import make_subplots
import plotly.graph_objects as go

class Figura():

    def __init__(self, conjUnity , mapaGO, titulo):
        self.titulo = titulo
        self.fig = make_subplots(rows=conjUnity.arg.max_lin, cols=conjUnity.arg.max_col, subplot_titles=(" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "))
        for unity in conjUnity.listaUnidades:
            for trace in mapaGO[unity]:
                self.fig.add_trace(trace, row = unity.arg.lin, col = unity.arg.col)
            self.fig.update_xaxes(title=conjUnity.legendaEixoX, row = unity.arg.lin , col = unity.arg.col) 
            self.fig.update_yaxes(title=conjUnity.legendaEixoY, row = unity.arg.lin , col = unity.arg.col) 
            if(len(conjUnity.listaUnidades) > 1):
                self.fig.layout.annotations[unity.arg.t].update(text=unity.arg.nome) 
            self.fig.update_layout(title= titulo)
            self.fig.update_layout(font=dict(size= unidade.tamanho_texto), 
                                yaxis=dict(range=[limInf,limSup])
                            ) 

    def getFig(self):
        return self.fig