"""
A pert file template.
"""


def pert(t, system):
    """
    Perturbation function called at each step.
    The function needs to be named ``pert`` and takes two positional arguments:
    ``t`` for the simulation time, and ``system`` for the system object.
    Arbitrary logic and calculations can be applied in this function to
    ``system``.
    If the perturbation event involves switching, such as disconnecting a line,
    one will need to set the ``system.TDS.custom_event`` flag to ``True`` to
    trigger a system connectivity checking, and Jacobian rebuilding and
    refactorization. To implement, add the following line to the scope where the
    event is triggered:
    .. code-block :: python
        system.TDS.custom_event = True
    In other scopes of the code where events are not triggered, do not add the
    above line as it may cause significant slow-down.
    The perturbation file can be supplied to the CLI using the ``--pert``
    argument or supplied to :py:func:`andes.main.run` using the ``pert``
    keyword.
    Parameters
    ----------
    t : float
        Simulation time.
    system : andes.system.System
        System object supplied by the simulator.
    """
    coordination = [0.5999,
                    0.5332,
                    0.5084,
                    0.4998,
                    0.462541521,
                    0.429121226,
                    0.340299815,
                    0.282600701,
                    0.276334584,
                    0.289933205,
                    0.269690573,
                    0.287803233,
                    0.295975417,
                    0.302936882,
                    0.278517008,
                    0.290291786,
                    0.228976682,
                    0.274061799,
                    0.288022757,
                    0.285998553,
                    0.315802068]


    if t > 0:
        system.PQ.alter('Req', 'PQ_1', 1.05)
        
    if t <= 2:
        x=t*10
        system.IEESGORM.alter('uomega0', 'IEESGORM_1', coordination(x)
