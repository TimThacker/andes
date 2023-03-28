"""
COI rate-of-change of frequency measurement based on COI.
"""

from andes.core import NumParam, Washout
from andes.models.coi import COI


class ROCOFcoi(COI):
    """
    COI and ROCOFcoi measurement.
    The ROCOF output variable is ``Wf_y``.
    """

    def __init__(self, system, config):
        COI.__init__(self, system, config)
        self.Tr = NumParam(default=0.1,
                           info="frequency washout time constant",
                           tex_name='T_r')

        self.Wf = Washout(u=self.omega,
                          K=1,
                          T=self.Tr,
                          info='frequency washout yielding ROCOF',
                          )
