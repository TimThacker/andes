from andes.core import Lag, LeadLag, NumParam
from andes.core.block import GainLimiter
from andes.models.governor.tgbase import TGBase, TGBaseData

# Reduced IEESGO Governor model
# K2 = K3 = 0
class IEESGORData(TGBaseData):
    def __init__(self):
        TGBaseData.__init__(self)
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

        self.K1 = NumParam(info='1/pu regulation',
                           default=0.02,
                           tex_name='K_1',
                           vrange=(5, 30),
                           )

        self.PMAX = NumParam(default=5, tex_name='P_{MAX}',
                             info='Max. turbine power',
                             vrange=(0.5, 1.5), power=True,
                             )
        self.PMIN = NumParam(default=0., tex_name='P_{MIN}',
                             info='Min. turbine power',
                             vrange=(0.0, 0.5), power=True,
                             )


class IEESGORModel(TGBase):
    def __init__(self, system, config):
        TGBase.__init__(self, system, config)

        self.F1 = Lag(u='ue * (omega - (wref + uomega0)',
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


        self.pout.e_str = 'ue * F3_y - pout'


class IEESGOR(IEESGORData, IEESGORModel):
    """
    IEEE Standard Governor (IEESGOR) Reduced Model.
    """

    def __init__(self, system, config):
        IEESGORData.__init__(self)
        IEESGORModel.__init__(self, system, config)
