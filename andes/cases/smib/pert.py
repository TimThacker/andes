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

        
    if t == 0:
        system.IEESGORM.alter('uomega0', 'IEESGORM_1', 0.005999)
    if t == 0.1:
        system.IEESGORM.alter('uomega0', 'IEESGORM_1', 0.005332)
    if t == 0.2:
        system.IEESGORM.alter('uomega0', 'IEESGORM_1', 0.005084)
    if t == 0.3:
        system.IEESGORM.alter('uomega0', 'IEESGORM_1', 0.004998)       
    if t == 0.4:
        system.IEESGORM.alter('uomega0', 'IEESGORM_1', 0.00462541521)
    if t == 0.5:
        system.IEESGORM.alter('uomega0', 'IEESGORM_1', 0.00429121226)       
    if t == 0.6:
        system.IEESGORM.alter('uomega0', 'IEESGORM_1', 0.00340299815)        
    if t == 0.7:
        system.IEESGORM.alter('uomega0', 'IEESGORM_1', 0.00282600701)        
    if t == 0.8:
        system.IEESGORM.alter('uomega0', 'IEESGORM_1', 0.00276334584)        
    if t == 0.9:
        system.IEESGORM.alter('uomega0', 'IEESGORM_1', 0.00289933205)       
    if t == 1.0:
        system.IEESGORM.alter('uomega0', 'IEESGORM_1', 0.00269690573)       
    if t == 1.1:
        system.IEESGORM.alter('uomega0', 'IEESGORM_1', 0.00287803233)
    if t == 1.2:
        system.IEESGORM.alter('uomega0', 'IEESGORM_1', 0.00295975417)
    if t == 1.3:
        system.IEESGORM.alter('uomega0', 'IEESGORM_1', 0.00302936882)
    if t == 1.4:
        system.IEESGORM.alter('uomega0', 'IEESGORM_1', 0.00278517008)       
    if t == 1.5:
        system.IEESGORM.alter('uomega0', 'IEESGORM_1', 0.00290291786)
    if t == 1.6:
        system.IEESGORM.alter('uomega0', 'IEESGORM_1', 0.00228976682)       
    if t == 1.7:
        system.IEESGORM.alter('uomega0', 'IEESGORM_1', 0.00274061799)        
    if t == 1.8:
        system.IEESGORM.alter('uomega0', 'IEESGORM_1', 0.00288022757)        
    if t == 1.9:
        system.IEESGORM.alter('uomega0', 'IEESGORM_1', 0.00285998553)        
    if t == 2.0:
        system.IEESGORM.alter('uomega0', 'IEESGORM_1', 0.00315802068)       
   
