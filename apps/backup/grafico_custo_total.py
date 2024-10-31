


titulo = "AGOSTO"
casos =[ ("c_2023_08_OFICIAL_29_4", "HIB12","blue"), ("c_2023_08_OFICIAL_29_4_VAZPAST","HIB12 Vazpast","red")]

titulo = "JANEIRO"
casos =[ ("c_2023_01_OFICIAL_29_4", "HIB12","blue"), ("c_2023_01_OFICIAL_29_4_VAZPAST","HIB12 Vazpast","red")]

fig = go.Figure()
for caso in casos:
	data = Pmo.read(caso[0]+"/pmo.dat")
	custo_total= data.custo_operacao_total
	desvio = data.desvio_custo_operacao_total*1.96
	#print(custo_total)
	#print(desvio)
	fig.add_trace(go.Bar( y = [custo_total], x = [caso[1]], text=np.round(custo_total,0), textposition = "outside", error_y = dict(type="data", array=[desvio]), name = caso[1], marker_color = caso[2], showlegend = False))
fig.update_layout(title=titulo+" Custo Total")
fig.update_xaxes(title_text="Casos")
fig.update_yaxes(title_text="R$")
#fig.update_yaxes(range=[-4000,0])
fig.update_layout(font=dict(size= 20), showlegend=False, barmode = "group")
fig.write_image(
os.path.join("resultados/"+titulo+"_custo_total.png"),width=1200,	height=700)
