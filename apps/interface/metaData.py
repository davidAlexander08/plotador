from apps.model.sintese import Sintese
from apps.model.argumento import Argumento 

class MetaData:
    def __init__(self):
        self.default_sts_cenarios_ending = ["FOR", "SF"]
        self.default_sts_SIN = [Sintese("COP_SIN_EST"), Sintese("CTER_SIN_EST"),Sintese("EARPF_SIN_EST"), Sintese("EVER_SIN_EST"), Sintese("GHID_SIN_EST"), Sintese("GTER_SIN_EST")]
        self.default_sts_SBM = [Sintese("CMO_SBM_EST"), Sintese("EARPF_SBM_EST"), Sintese("EVER_SBM_EST"), Sintese("GHID_SBM_EST"), Sintese("GTER_SBM_EST")]
        self.default_sts_REE = [Sintese("EARPF_REE_EST"), Sintese("EVER_REE_EST"), Sintese("GHID_REE_EST")]
        self.default_sts_UHE = [Sintese("GHID_UHE_EST"), Sintese("QDEF_UHE_EST"), Sintese("QVER_UHE_EST"), Sintese("QTUR_UHE_EST"), Sintese("VARMF_UHE_EST")]
        self.default_sts_CEN = [Sintese("ENAA_SIN_SF"), Sintese("ENAA_SBM_SF"), Sintese("ENAA_REE_SF"), Sintese("QINC_SIN_SF"), Sintese("QINC_SBM_SF"), Sintese("QINC_REE_SF"), Sintese("QINC_UHE_SF")]

        self.mapa_sinteses = {
            "TODOS": self.default_sts_SIN + self.default_sts_SBM + self.default_sts_REE + self.default_sts_UHE,
            "OPER": self.default_sts_SIN + self.default_sts_SBM,
            "SIN": self.default_sts_SIN,
            "SBM": self.default_sts_SBM,
            "REE": self.default_sts_REE,
            "UHE": self.default_sts_UHE,
            "CEN": self.default_sts_CEN
        }

        chave_sbm = "SBM"
        self.lista_submercados = [Argumento(["SUDESTE","NORDESTE","NORTE","SUL"], chave_sbm, "Submercados")] 
        chave_ree = "REE"
        self.lista_rees = [Argumento(['BMONTE','IGUACU','ITAIPU','MADEIRA','MAN-AP','NORDESTE'], chave_ree, "REEs 1"), 
                            Argumento(['PRNPANEMA','SUDESTE','SUL','TPIRES','NORTE','PARANA'], chave_ree, "REEs 2")]
        chave_usina = "UHE"
        self.lista_usinas_principais = [Argumento(["NOVA PONTE", "EMBORCACAO", "SAO SIMAO", "FURNAS", "MARIMBONDO", "A. VERMELHA"], chave_usina, "Usinas 1"),
                                        Argumento(["I. SOLTEIRA", "JUPIA", "P. PRIMAVERA", "A.A. LAYDNER", "G.B. MUNHOZ","MACHADINHO"], chave_usina, "Usinas 2"),
                                        Argumento(["TRES MARIAS", "SOBRADINHO", "ITAPARICA", "SERRA MESA", "TUCURUI", "B MONTE"],    chave_usina  , "Usinas 3"),
                                        ]
        
        self.mapa_argumentos = {
            "TODOS": self.lista_submercados+self.lista_rees+self.lista_usinas_principais,
            "OPER": self.lista_submercados,
            "SIN" : None,
            "SBM": self.lista_submercados,
            "REE": self.lista_rees,
            "UHE": self.lista_usinas_principais,
            "CEN": self.lista_submercados+self.lista_rees+self.lista_usinas_principais
        }
        #####   UNIDADE EIXO Y, TITULO GRAFICO,  LIMITE INFERIOR EIXO Y, LIMITE INFERIOR EIXO X
        self.mapa_sintese =        {
            "GTER":    ("MW","Geração Térmica"),
            "GHID":    ("MW","Geração Hidrelétrica"),
            "EARPF":    ("%","Energ. Armz. Perc."),
            "COP":    ("R$","Custo de Oper."),
            "EARMF":    ("MW","Energ. Armz. Final"),
            "CMO":    ("R$/MWh","Custo Marg."),
            "QTUR":    ("m3/s", "Vaz. Turb."),
            "QDEF":    ("m3/s", "Vaz. Defl."),
            "VRET":    ("hm3", "Volume Retirada"),
            "QINC":    ("m3/s", "Vaz. Incr."),
            "QVER":    ("m3/s", "Vaz. Vert."),
            "QAFL":    ("m3/s", "Vaz. Afl."),
            "VARMF":    ("hm3", "Vol. Armz."),
            "VVMINOP":    ("MWmed", "Viol. VMINOP"),
            "CDEF":    ("10^6 R$", "Custo de Deficit"),
            "CONVERGENCIA":    ("10^3 R$", "Convergencia"),
            "CTER":    ("10^6 R$", "Custo Térmica"),
            "DEF":    ("MWmes", "Deficit"),
            "EARPI":    ("%", "Energ. Armz. Perc Ini."),
            "EARMI":    ("MW", "Energ. Armz. Ini."),
            "EEVAP":    ("MW", "Energ. Evap."),
            "ENAA":    ("MW", "Energ. Natu. Afl."),
            "ENAAF":    ("MW", "Energ. Natu. Afl. Final"),
            "EVER":    ("MW", "Energ. Vertida"),
            "EVERF":    ("MW", "Energ. Vertida Final"),
            "EXC":    ("MW", "Excesso"),
            "CFU":  ("R$", "Custo Futuro"),
            "VAGUA":  ("1000R$/hm3", "Valor Agua"),
            "VAGUAI":  ("1000R$/hm3", "Valor Agua Incr."),
            "VVER":("hm3","Volume Vertido"),
            "TEMPO":("min","Tempo de Execucao"),
            "MERL":("MW","Demanda Líquida"),
            "VFPHA":("MW","Violação FPHA")
        }