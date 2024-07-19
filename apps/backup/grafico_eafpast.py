import pandas as pd
import plotly.express as px
import os
import plotly.graph_objects as go
import plotly.io as pio
from inewave.newave import Pmo
from inewave.newave import Ree


titulo = "JANEIRO"
casos =[ ("c_2023_01_OFICIAL_29_4", "HIB12","blue"), ("c_2023_01_OFICIAL_29_4_VAZPAST","HIB12 Vazpast","red")]
mes_anterior = 12
nome_mes_anterior = "DEZEMBRO"

titulo = "AGOSTO"
casos =[ ("c_2023_08_OFICIAL_29_4", "HIB12","blue"), ("c_2023_08_OFICIAL_29_4_VAZPAST","HIB12 Vazpast","red")]
mes_anterior = 7
nome_mes_anterior = "JULHO"


mapa_df = {}
for caso in casos:
	data = Pmo.read(caso[0]+"/pmo.dat").eafpast_tendencia_hidrologica
	mapa_df[caso[0]] = data
	data_ree = Ree.read(caso[0]+"/ree.dat").rees
	print(data_ree)
	
print(data)



fig = go.Figure()
for caso in casos:
	data_ree = Ree.read(caso[0]+"/ree.dat").rees
	print(data_ree)
	df = mapa_df[caso[0]]
	df_ree = df.loc[(df["mes"] == mes_anterior)]
	#codigo_ree = data_ree.loc[data_ree["nome"] == ree]["codigo"].iloc[0]
	fig.add_trace(go.Bar( y = df_ree["valor"], x = df_ree["nome_ree"], name = caso[1], marker_color = caso[2], showlegend = True))
fig.update_layout(title=titulo+" Vazpast "+nome_mes_anterior)
fig.update_xaxes(title_text="REEs")
fig.update_yaxes(title_text="MWmes")
#fig.update_yaxes(range=[-4000,0])
fig.update_layout(font=dict(size= 15), showlegend=True, barmode = "group")
fig.write_image(
os.path.join("resultados/"+titulo+"_vazpast_"+nome_mes_anterior+".png"),width=1200,	height=700)