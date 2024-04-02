



from plotly.subplots import make_subplots
import plotly.graph_objects as go

class Figura():

    def __init__(self, conjUnity , mapaGO, titulo):
        self.titulo = titulo
        self.fig = make_subplots(rows=conjUnity.arg.max_lin, cols=conjUnity.arg.max_col, subplot_titles=(" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "))
        #Descobrindo Limites
        for unity in conjUnity.listaUnidades:
            for trace in mapaGO[unity]:
                lim_sup = max(trace.y)
                lim_inf = min(trace.y)
        limSup = lim_sup if conjUnity.limSup is True else None
        limInf_aux = lim_inf if conjUnity.limInf is True else None
        limInf = 0 if limInf_aux > 0 else limInf_aux
        print("limInf: ", limInf, " limSup: ", limSup)
        for unity in conjUnity.listaUnidades:
            for trace in mapaGO[unity]:
                self.fig.add_trace(trace, row = unity.arg.lin, col = unity.arg.col)
            self.fig.update_xaxes(title=conjUnity.legendaEixoX, row = unity.arg.lin , col = unity.arg.col) 
            self.fig.update_yaxes(title=conjUnity.legendaEixoY, row = unity.arg.lin , col = unity.arg.col, range=[limInf,limSup]) 
            if(len(conjUnity.listaUnidades) > 1):
                self.fig.layout.annotations[unity.arg.t].update(text=unity.arg.nome) 
            self.fig.update_layout(title= titulo)

        #limSup = lim_sup if conjUnity.limSup is True else None
        #limInf_aux = lim_inf if conjUnity.limInf is True else None
        #limInf = 0 if limInf_aux > 0 else limInf_aux
        
        self.fig.update_layout(font=dict(size= conjUnity.tamanho_texto)) 

    def getFig(self):
        return self.fig