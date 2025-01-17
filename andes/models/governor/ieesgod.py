from andes.core import Lag, LeadLag, NumParam, Algeb, State, ConstService
from andes.core.block import GainLimiter, DeadBand1, DeadBand2, DeadBand3
from andes.models.governor.tgbase import TGBase, TGBaseData


class IEESGODData(TGBaseData):
    def __init__(self):
        TGBaseData.__init__(self)

        self.dbL = NumParam(info='Lower bound of deadband',
                            tex_name='db_L',
                            default=0.0,
                            unit='p.u.',
                            )
        self.dbU = NumParam(info='Upper bound of deadband',
                            tex_name='db_U',
                            default=0.0,
                            unit='p.u.',
                            )
        self.T1 = NumParam(info='Controller lag',
                           default=0.02,
                           tex_name='T_1',
                           vrange=(0, 100),
                           )
        self.T2 = NumParam(info='Lead compensation',
                           default=1.0,
                           tex_name='T_2',
                           vrange=(0, 10),
                           )
        self.T3 = NumParam(info='Governor lag',
                           default=1.0,
                           tex_name='T_3',
                           vrange=(0.04, 1.0),
                           )
        self.T4 = NumParam(info='Steam inlet delay',
                           default=0.5,
                           tex_name='T_4',
                           vrange=(0.0, 1.0),
                           )
        self.T5 = NumParam(info='Reheater delay',
                           default=10.0,
                           tex_name='T_5',
                           vrange=(0.0, 50.0),
                           )
        self.T6 = NumParam(info='Crossover delay',
                           default=0.5,
                           tex_name='T_6',
                           vrange=(0.0, 1.0),
                           )

        self.K1 = NumParam(info='1/pu regulation',
                           default=0.02,
                           tex_name='K_1',
                           vrange=(5, 30),
                           )
        self.K2 = NumParam(info='fraction K2',
                           default=1.0,
                           tex_name='K_2',
                           vrange=(0, 3),
                           )
        self.K3 = NumParam(info='fraction K3',
                           default=1.0,
                           tex_name='K_3',
                           vrange=(-1.0, 1.0),
                           )

        self.PMAX = NumParam(default=5, tex_name='P_{MAX}',
                             info='Max. turbine power',
                             vrange=(0.5, 1.5), power=True,
                             )
        self.PMIN = NumParam(default=0., tex_name='P_{MIN}',
                             info='Min. turbine power',
                             vrange=(0.0, 0.5), power=True,
                             )


class IEESGODModel(TGBase):
    def __init__(self, system, config):
        TGBase.__init__(self, system, config)
                
        self.wd = Algeb(info='Generator speed deviation',
                        unit='p.u.',
                        tex_name=r'\omega_{dev}',
                        v_str='0',
                        e_str='ue * (omega - wref - uomega0) - wd',
                        )
        
        self.DB = DeadBand2(u=self.wd,
                            center=0.0, lower=self.dbL,
                            upper=self.dbU
                            
                            )
        #tex_name='DB',info='deadband for speed deviation',

        self.F1 = Lag(u=self.DB_y,
                      T=self.T1,
                      K=self.K1,
                      )

        self.F2 = LeadLag(u=self.F1_y,
                          T1=self.T2,
                          T2=self.T3,
                          K=1.0,
                          )

        self.HL = GainLimiter(u='ue * (paux + pref0 - F2_y)',
                              K=1.0,
                              R=1.0,
                              lower=self.PMIN,
                              upper=self.PMAX,
                              )
        self.F3 = Lag(u=self.HL_y, T=self.T4, K=1.0,
                      )

        self.F4 = Lag(u=self.F3_y, T=self.T5, K=self.K2,
                      )

        self.F5 = Lag(u=self.F4_y, T=self.T6, K=self.K3,
                      )

        self.pout.e_str = 'ue * ((1-K2)*F3_y + (1-K3)*F4_y + F5_y) - pout'


class IEESGOD(IEESGODData, IEESGODModel):
    """
    IEEE Standard Governor (IEESGO) with Governor Deadband.
    """

    def __init__(self, system, config):
        IEESGODData.__init__(self)
        IEESGODModel.__init__(self, system, config)
