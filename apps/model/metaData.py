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

        chave_sbm = "submercado"
        self.lista_submercados = [Argumento("SUDESTE", chave_sbm), Argumento("NORDESTE",chave_sbm), Argumento("NORTE", chave_sbm), Argumento("SUL", chave_sbm)]
        chave_ree = "ree"
        self.lista_rees = [Argumento('BMONTE', chave_ree),
                            Argumento('IGUACU', chave_ree),
                            Argumento('ITAIPU', chave_ree),
                            Argumento('MADEIRA', chave_ree),
                            Argumento('MAN-AP', chave_ree),
                            Argumento('NORDESTE', chave_ree),
                            Argumento('NORTE', chave_ree),
                            Argumento('PARANA', chave_ree),
                            Argumento('PRNPANEMA', chave_ree),
                            Argumento('SUDESTE', chave_ree),
                            Argumento('SUL', chave_ree),
                            Argumento('TPIRES', chave_ree)]
        chave_usina = "usina"
        self.lista_usinas_principais = [Argumento("NOVA PONTE", chave_usina),
                                        Argumento("EMBORCACAO", chave_usina),
                                        Argumento("SAO SIMAO", chave_usina),
                                        Argumento("FURNAS", chave_usina),
                                        Argumento("MARIMBONDO", chave_usina),
                                        Argumento("A. VERMELHA", chave_usina),
                                        Argumento("I. SOLTEIRA", chave_usina),
                                        Argumento("JUPIA", chave_usina),
                                        Argumento("P. PRIMAVERA",chave_usina),
                                        Argumento("A.A. LAYDNER", chave_usina),
                                        Argumento("G.B. MUNHOZ", chave_usina),
                                        Argumento("MACHADINHO", chave_usina),
                                        Argumento("TRES MARIAS", chave_usina),
                                        Argumento("SOBRADINHO", chave_usina),
                                        Argumento("ITAPARICA", chave_usina),
                                        Argumento("SERRA MESA", chave_usina),
                                        Argumento("TUCURUI",    chave_usina  ),
                                        ]
        
        self.mapa_argumentos = {
            "TODOS": self.lista_submercados+self.lista_rees+self.lista_usinas_principais,
            "SBM": self.lista_submercados,
            "REE": self.lista_rees,
            "UHE": self.lista_usinas_principais
        }

        self.mapa_sintese =        {
            "GTER":    ("MWmes","Geração Térmica"),
            "GHID":    ("MWmes","Geração Hidrelétrica"),
            "EARPF":    ("%","Energ. Armz. Perc."),
            "COP":    ("R$","Custo de Oper."),
            "EARMF":    ("MWmes","Energ. Armz. Final"),
            "CMO":    ("R$/MWh","Custo Marg."),
            "QTUR":    ("m3/s", "Vaz. Turb."),
            "QDEF":    ("m3/s", "Vaz. Defl."),
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
            "EARMI":    ("MWmes", "Energ. Armz. Ini."),
            "EEVAP":    ("MWmes", "Energ. Evap."),
            "ENAA":    ("MWmes", "Energ. Natu. Afl."),
            "ENAAF":    ("MWmes", "Energ. Natu. Afl. Final"),
            "EVER":    ("MWmes", "Energ. Vertida"),
            "EVERF":    ("MWmes", "Energ. Vertida Final"),
            "EXC":    ("MWmes", "Excesso"),
        }