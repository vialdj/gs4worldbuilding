from . import Atmosphere
from . import World

import numpy as np


class StandardAmmonia(World):
    """the standard ammonia world model"""

    class StandardAmmoniaAtmosphere(Atmosphere):
        """the standard ammonia atmosphere model"""
        _composition = ['N2', 'NH3', 'CH4']
        _toxicity = Atmosphere.Toxicity.LETHAL
        _suffocating = True
        _corrosive = True

    _temperature_range = World.Range(140, 215)
    _size = World.Size.STANDARD
    _core = World.Core.ICY_CORE
    _pressure_factor = 1
    _greenhouse_factor = .2
    _hydrosphere_range = World.Range(.2, 1)
    _absorption = .84
    _atmosphere = StandardAmmoniaAtmosphere

    def random_hydrosphere(self):
        """roll of 2d maximum at 10 and divided by 10"""
        self.hydrosphere = min(np.random.triangular(0.2, .7, 1.2), 1)

    def __init__(self):
        super(StandardAmmonia, self).__init__()
