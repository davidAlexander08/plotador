



from plotly.subplots import make_subplots
import plotly.graph_objects as go

class Figura():

    def __init__(self, col = 1, row = 1):
        self.fig = make_subplots(rows=row, cols=col)
    
    def add_trace(self, goObject, col = 1, lin = 1):
        self.fig.add_trace(goObject)