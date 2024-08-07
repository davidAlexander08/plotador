


 
from plotly.subplots import make_subplots
import plotly.graph_objects as go

class Figura(): 

    def __init__(self, conjUnity , mapaGO, titulo, yinf = None,  ysup = None, y2 = "False"):
        self.titulo = titulo
        self.fig = make_subplots(specs=[[{"secondary_y": True}]], rows=conjUnity.arg.max_lin, cols=conjUnity.arg.max_col, subplot_titles=(" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "))
        for unity in conjUnity.listaUnidades:
            contador = 1
            for trace in mapaGO[unity]:
                lim_sup = max(trace.y) if len(trace.y) is not 0 else 0
                lim_inf = min(trace.y) if len(trace.y) is not 0 else 0
                if(y2 == "True"):
                    print("contador: ", contador)
                    print("tamanho: ",len(mapaGO[unity]) )
                    if(contador == len(mapaGO[unity])):
                        self.fig.add_trace(trace, row = unity.arg.lin, col = unity.arg.col, secondary_y = True)
                        print("ENTROU AQUI")
                        print(trace.y)
                    else:
                        self.fig.add_trace(trace, row = unity.arg.lin, col = unity.arg.col)
                else:
                    self.fig.add_trace(trace, row = unity.arg.lin, col = unity.arg.col)
                self.fig.update_yaxes(range=[yinf,ysup])
                contador += 1
            if(unity.arg.lin == 1 and unity.arg.col == 1):
                self.fig.update_yaxes(title=conjUnity.legendaEixoY, row = unity.arg.lin , col = unity.arg.col) 
                self.fig.update_xaxes(title=conjUnity.legendaEixoX, row = unity.arg.lin , col = unity.arg.col) 
                self.fig.update_yaxes(title="Diff", secondary_y = True, overlaying ="y", side = "right") 
#                self.fig.update_layout(yaxis2 = dict(title ="Diff", side = "right", overlaying = "y"), row = unity.arg.lin , col = unity.arg.col)
            if(len(conjUnity.listaUnidades) > 1):
                self.fig.layout.annotations[unity.arg.t].update(text=unity.arg.nome) 
            self.fig.update_layout(title= titulo)

        limSup = lim_sup if conjUnity.limites is True else None
        if(conjUnity.limites):
            limInf = 0 if lim_inf > 0 else lim_inf
        else:
            limInf = None
        self.fig.update_layout(font=dict(size= conjUnity.tamanho_texto), boxmode="group")  
        #self.fig.update_yaxes(range=[limInf,limSup])
    def getFig(self):
        return self.fig