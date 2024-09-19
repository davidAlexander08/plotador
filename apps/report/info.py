
from apps.report.estruturas import Estruturas

class Info(Estruturas):
    def __init__(self,html_file, data):
        self.lista_text = []
        Estruturas.__init__(self)
        Inicio_tabela = """
<table>
<tr>
<th>Nome do Caso</th>
<th>Caminho</th>
<th>Modelo</th>
<th>Cor</th>
</tr>
"""                         
        Template_tabela_caso = """
<tr>
<td>nome</td>
<td>caminho</td>
<td>modelo</td>
<td style="background-color: cor;"></td>
</tr>
"""                         
        self.lista_text.append("<h3>Informações Gerais do Estudo</h3>"+"\n")
        self.lista_text.append(Inicio_tabela)
        print(self.lista_text)
        print("\n".join(lines))
        exit(1)
        for caso in data.casos:
            temp = Template_tabela_caso
            temp = temp.replace("nome", caso.nome)
            temp = temp.replace("caminho", caso.caminho)
            temp = temp.replace("modelo", caso.modelo)
            temp = temp.replace("cor", caso.cor)
            self.lista_text.write(temp)
        self.lista_text.write("</table>"+"\n")
        
        self.lista_text.write("<h2>Eco Dados Entrada</h2>"+"\n")
        
        flag_nw = flag_deco = flag_dss = True
        for caso in data.casos:
            if(caso.modelo == "NEWAVE"):
                if(flag_nw == True):
                    self.lista_text.write(self.mapa_tabela_modelo[caso.modelo])
                    flag_nw = False
                temp = self.preenche_modelo_tabela_modelo_NEWAVE(caso)
            if(caso.modelo == "DECOMP"):
                if(flag_deco == True):
                    self.lista_text.write(self.mapa_tabela_modelo[caso.modelo])
                    flag_deco = False
                temp = self.preenche_modelo_tabela_modelo_DECOMP(caso)
            if(caso.modelo == "DESSEM"):
                if(flag_dss == True):
                    self.lista_text.write(self.mapa_tabela_modelo[caso.modelo])
                    flag_dss = False
                temp = self.preenche_modelo_tabela_modelo_DESSEM(caso)
            self.lista_text.write(temp)
        self.lista_text.write("</table>"+"\n")


        #html_file.write("<h2>Operacao</h2>"+"\n")
        #
        #flag_nw = flag_deco = flag_dss = True
        #for caso in data.casos:
        #    if(caso.modelo == "NEWAVE"):
        #        if(flag_nw == True):
        #            html_file.write(self.mapa_tabela_modelo[caso.modelo])
        #            flag_nw = False
        #        temp = self.preenche_operacao_NEWAVE(caso)
        #    if(caso.modelo == "DECOMP"):
        #        if(flag_deco == True):
        #            html_file.write(self.mapa_tabela_modelo[caso.modelo])
        #            flag_deco = False
        #        temp = self.preenche_operacao_DECOMP(caso)
        #    if(caso.modelo == "DESSEM"):
        #        if(flag_dss == True):
        #            html_file.write(self.mapa_tabela_modelo[caso.modelo])
        #            flag_dss = False
        #        temp = self.preenche_operacao_DESSEM(caso)
        #    html_file.write(temp)
        #html_file.write("</table>"+"\n")



    def preenche_operacao_NEWAVE(self,caso):

        #df_temp = self.eco_indicadores.retorna_df_concatenado("TEMPO")
        #temp = self.mapa_template_tabela_modelo[caso.modelo]
        #temp = temp.replace("Caso", caso.nome)
        #temp = temp.replace("Modelo", caso.modelo)
        #data_pmo = Pmo.read(caso.caminho+"/pmo.dat")
        #data_dger = Dger.read(caso.caminho+"/dger.dat")
        #data_cvar = Cvar.read(caso.caminho+"/cvar.dat")
        #print(data_dger.num_series_sinteticas)
        #temp = temp.replace("Versao", data_pmo.versao_modelo)
        #temp = temp.replace("Mes_I", str(data_dger.mes_inicio_estudo))
        #temp = temp.replace("Ano_I", str(data_dger.ano_inicio_estudo))
        #temp = temp.replace("Anos_Pos", str(data_dger.num_anos_pos_estudo))
        #temp = temp.replace("It_Max", str(data_dger.num_max_iteracoes))
        #temp = temp.replace("It_Min", str(data_dger.num_minimo_iteracoes))
        #temp = temp.replace("FW", str(data_dger.num_forwards))
        #temp = temp.replace("BK", str(data_dger.num_aberturas))
        #temp = temp.replace("N_series_sim_final", str(data_dger.num_series_sinteticas))
        #tipo_sim_fin = "Ind" if data_dger.agregacao_simulacao_final == 1 else "Agr"
        #temp = temp.replace("SF_Ind", tipo_sim_fin)
        #temp = temp.replace("CVAR", str(data_cvar.valores_constantes[0])+"x"+str(data_cvar.valores_constantes[1]))
        ##df_caso = df_temp.loc[(df_temp["caso"] == caso.nome)]
        ##tempo_total = df_caso.loc[(df_caso["etapa"] == "Tempo Total")]["tempo"].iloc[0]/60
        ##iteracoes = data_pmo.convergencia["iteracao"].iloc[-1]
        ##zinf = data_pmo.convergencia["zinf"].iloc[-1]
        ##custo_total = data_pmo.custo_operacao_total
        ##desvio_custo = data_pmo.desvio_custo_operacao_total*1.96
        ##temp = temp.replace("tempo_total", str(tempo_total))
        ##temp = temp.replace("iteracoes", str(iteracoes))
        ##temp = temp.replace("zinf", str(zinf))
        ##temp = temp.replace("custo_total", str(custo_total))
        ##temp = temp.replace("desvio_custo", str(desvio_custo))
#
        #return temp
        pass


    def preenche_operacao_DECOMP(self,caso):
        pass

    def preenche_operacao_DESSEM(self,caso):
        pass


    def preenche_modelo_tabela_modelo_NEWAVE(self,caso):

        df_temp = self.eco_indicadores.retorna_df_concatenado("TEMPO")

        tempo_total = iteracoes = zinf = custo_total = desvio_custo = 0
        versao = "0"

        temp = self.mapa_template_tabela_modelo[caso.modelo]
        temp = temp.replace("Caso", caso.nome)
        temp = temp.replace("Modelo", caso.modelo)

        data_pmo = Pmo.read(caso.caminho+"/pmo.dat")
        data_dger = Dger.read(caso.caminho+"/dger.dat")
        data_cvar = Cvar.read(caso.caminho+"/cvar.dat")

        temp = temp.replace("Versao", data_pmo.versao_modelo)
        temp = temp.replace("Mes_I", str(data_dger.mes_inicio_estudo))
        temp = temp.replace("Ano_I", str(data_dger.ano_inicio_estudo))
        temp = temp.replace("Anos_Pos", str(data_dger.num_anos_pos_estudo))
        temp = temp.replace("It_Max", str(data_dger.num_max_iteracoes))
        temp = temp.replace("It_Min", str(data_dger.num_minimo_iteracoes))
        temp = temp.replace("FW", str(data_dger.num_forwards))
        temp = temp.replace("BK", str(data_dger.num_aberturas))
        temp = temp.replace("N_series_sim_final", str(data_dger.num_series_sinteticas))
        tipo_sim_fin = "Ind" if data_dger.agregacao_simulacao_final == 1 else "Agr"
        temp = temp.replace("SF_Ind", tipo_sim_fin)
        temp = temp.replace("CVAR", str(data_cvar.valores_constantes[0])+"x"+str(data_cvar.valores_constantes[1]))
        return temp

    def preenche_modelo_tabela_modelo_DECOMP(self, caso):

        df_temp = self.eco_indicadores.retorna_df_concatenado("TEMPO")

        tempo_total = iteracoes = zinf = custo_total = desvio_custo = 0
        versao = "0"

        temp = self.mapa_template_tabela_modelo[caso.modelo]
        temp = temp.replace("nome", caso.nome)
        temp = temp.replace("modelo", caso.modelo)
        extensao = ""
        with open(caso.caminho+"/caso.dat") as f:
            extensao = f.readline().strip('\n')
        if extensao == "":
            raise FileNotFoundError(f"Arquivo caso.dat não encontrado.") 
        data_relato = Relato.read(caso.caminho+"/relato."+extensao).convergencia
        df_caso = df_temp.loc[(df_temp["caso"] == caso.nome)]
        tempo_total = df_caso.loc[(df_caso["etapa"] == "Tempo Total")]["tempo"].iloc[0]/60
        iteracoes = data_relato["iteracao"].iloc[-1]
        zinf = data_relato["zinf"].iloc[-1]
        custo_total = " "
        versao = " "
        temp = temp.replace("versao", versao)
        temp = temp.replace("tempo_total", str(tempo_total))
        temp = temp.replace("iteracoes", str(iteracoes))
        temp = temp.replace("zinf", str(zinf))
        temp = temp.replace("custo_total", str(custo_total))
        return temp

    def preenche_modelo_tabela_modelo_DESSEM(self, caso):
        df_temp = self.eco_indicadores.retorna_df_concatenado("TEMPO")
        ## FALTA COMPLEMENTAR, ESTA INCOMPLETO
        data_relato = DesLogRelato.read(caso.caminho+"/DES_LOG_RELATO.DAT")
        df_caso = df_temp.loc[(df_temp["caso"] == caso.nome)]
        tempo_total = df_caso["tempo"].sum()/60
        iteracoes = " "
        zinf = " "
        custo_total = " "
        desvio_custo = " "
        versao = data_relato.versao
        return temp
