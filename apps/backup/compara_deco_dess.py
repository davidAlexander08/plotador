
#parquet = "CMO_SBM_EST"
#filtro = "SE"
#unidade = "R$/MWh"
#titulo = "Custo Marginal"

#parquet = "GHID_SIN_EST"
#filtro = ""
#unidade = "MW"
#titulo = "Geracao Hidreletrica"

parquet = "GTER_SIN_EST"
filtro = ""
unidade = "MW"
titulo = "Geracao Termica"

tipos = ["ree","hib12_25x35","hib12_15x35","hib12_15x40","hib12_15x45","hib12_15x50"]
dic_Decomp= {}
dic_Dess= {}
dic_Dess_48 = {}
casos = [("AGO_Deco","ago21/dessem_d16/","16 DE AGOSTO"),("NOV_Deco","nov21/dessem_d10/", "10 DE NOVEMBRO")]
for caso in casos:
	for elemento in tipos:
		arq = "/home/ESTUDO/PEM/Atividades/Ciclo23_24/Analise_CVAR/"+caso[0]+"/"+parquet+"_"+elemento+".parquet.gzip"
		df_GT_Deco = pd.read_parquet(arq, engine='pyarrow')
		if(filtro != ""):
			df_GT_Deco = df_GT_Deco.loc[(df_GT_Deco["submercado"] == filtro)]
			#print(df_GT_Deco)
		#print(df_GT_Deco.loc[df_GT_Deco["cenario"] == "mean"]["valor"].iloc[0])
		valor_gt_Deco = df_GT_Deco.loc[df_GT_Deco["cenario"] == "mean"]["valor"].iloc[0]
		#print("Deco: ", valor_gt_Deco)
		dic_Decomp[elemento] = [valor_gt_Deco]

		ent = Entdados.read("/home/ESTUDO/PEM/Atividades/Ciclo23_24/Analise_CVAR/"+caso[1]+elemento+"/entdados.dat")
		df = ent.tm(df=True)
		df_linha = df.reset_index(drop = False)["duracao"]

		arq = "/home/ESTUDO/PEM/Atividades/Ciclo23_24/Analise_CVAR/"+caso[1]+elemento+"/sintese/"+parquet+".parquet.gzip"
		df_GT_Dess = pd.read_parquet(arq, engine='pyarrow')
		if(filtro != ""):
			df_GT_Dess = df_GT_Dess.loc[(df_GT_Dess["submercado"] == filtro)]
		df_valor_Dess = df_GT_Dess.reset_index(drop=True)["valor"]
		
		#PRIMEIRO DIA
		df_valor_Dess_48 = df_valor_Dess.loc[(df_valor_Dess.index <= 48)]
		df_linha_48 = df_linha.loc[(df_valor_Dess.index <= 48)]
		df_valor_Dess_48.to_csv(caso[2]+elemento+"df_valor_Dess_48.csv")
		df_linha_48.to_csv(caso[2]+elemento+"df_linha_48.csv")

		df_novo = (df_valor_Dess*df_linha)
		valor_Dess = df_novo.sum()/df_linha.sum()
		dic_Dess[elemento] = [valor_Dess]
		#print(df_novo)
		print(elemento, " " ,valor_Dess)
		
		df_novo_48 = (df_valor_Dess_48*df_linha_48)
		valor_Dess_48 = df_novo_48.sum()/df_linha_48.sum()
		dic_Dess_48[elemento] = [valor_Dess_48]
		#print(df_novo_48)
		print(elemento, " " ,valor_Dess_48)
		#exit(1)

	df_deco = pd.DataFrame(dic_Decomp)
	df_deco["Modelo"] = "Decomp"
	df_dess = pd.DataFrame(dic_Dess)
	df_dess["Modelo"] = "Dessem"
	df_concat = pd.concat([df_deco,df_dess] )
	print(df_concat)
	
	df_deco_48 = pd.DataFrame(dic_Decomp)
	df_deco_48["Modelo"] = "Decomp"
	df_dess_48 = pd.DataFrame(dic_Dess_48)
	df_dess_48["Modelo"] = "Dessem"
	df_concat_48 = pd.concat([df_deco_48,df_dess_48] )
	print(df_concat_48)

	fig = go.Figure()
	contador = 0
	color = {"Decomp":"#bfc4dc", "Dessem":"#3b5998"}
	for modelo in df_concat["Modelo"].unique():
		#coly = df_concat.loc[(df_concat["Modelo"] == modelo)][elemento].iloc[0]
		#print(df_concat.loc[(df_concat["Modelo"] == modelo)])
		df = df_concat.loc[(df_concat["Modelo"] == modelo)]
		df = df.drop(["Modelo"], axis = 1)
		fig.add_trace(
			go.Bar(
				x = tipos,
				y = df.iloc[0].tolist(),
				text = df.iloc[0].round(1).tolist(),
				textposition = "inside",
				name = modelo,
				textfont=dict(size=15),
				marker_color= color[modelo],
				showlegend=True
			)
		)
	contador += 1
	fig.update_xaxes(title_text="Casos")
	fig.update_yaxes(title_text=unidade)
	fig.update_layout(font=dict(size= 20))
	fig.update_layout(title="Comparação DCP-DSS "+parquet+" "+filtro+" "+caso[2])
	fig.write_image(
		os.path.join("compar_dcp_dss_"+parquet+"_1_est_"+caso[2]+".png"),
		width=800,
		height=600)





	fig = go.Figure()
	contador = 0
	color = {"Decomp":"#bfc4dc", "Dessem":"#3b5998"}
	for modelo in df_concat_48["Modelo"].unique():
		#coly = df_concat.loc[(df_concat["Modelo"] == modelo)][elemento].iloc[0]
		#print(df_concat.loc[(df_concat["Modelo"] == modelo)])
		df = df_concat_48.loc[(df_concat_48["Modelo"] == modelo)]
		df = df.drop(["Modelo"], axis = 1)
		fig.add_trace(
			go.Bar(
				x = tipos,
				y = df.iloc[0].tolist(),
				text = df.iloc[0].round(1).tolist(),
				textposition = "inside",
				name = modelo,
				textfont=dict(size=20),
				marker_color= color[modelo],
				showlegend=True
			)
		)
	contador += 1
	fig.update_xaxes(title_text="Casos")
	fig.update_yaxes(title_text=unidade)
	fig.update_layout(font=dict(size=20))
	fig.update_layout(title="Comparação DCP-DSS 1 dia "+titulo+" "+filtro+" "+caso[2])
	fig.write_image(
		os.path.join("comparar_1_dia_dcp_dss_"+parquet+"_1_est_"+caso[2]+".png"),
		width=1200,
		height=375)

exit(1)