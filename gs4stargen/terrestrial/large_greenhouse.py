# -*- coding: utf-8 -*-

from . import Atmosphere, Terrestrial
from .. import model
from ..random import roll2d6

from astropy import units as u


class LargeGreenhouse(Terrestrial):
    """The large greenhouse world model"""

    class LargeGreenhouseAtmosphere(Atmosphere):
        """The large greenhouse atmosphere model"""
        _toxicity = Atmosphere.Toxicity.LETHAL
        _suffocating = True
        _corrosive = True

        @property
        def composition(self):
            return (['CO2'] if self._world.hydrographic_coverage < .1
                    else ['N2', 'H2O', 'O2'])

    _temperature_bounds = model.bounds.QuantityBounds(500 * u.K, 950 * u.K)
    _size = Terrestrial.Size.LARGE
    _core = Terrestrial.Core.LARGE_IRON_CORE
    _pressure_factor = 500
    _greenhouse_factor = 2.0
    _hydrographic_coverage_bounds = model.bounds.ValueBounds(0, .5)
    _absorption = .77
    _atmosphere = LargeGreenhouseAtmosphere

    def random_hydrographic_coverage(self):
        """roll of 2d-7 minimum at 0 and divided by 10"""
        self.hydrographic_coverage = max(roll2d6(-7, continuous=True) / 10, 0)

    def __init__(self, **kw):
        super(LargeGreenhouse, self).__init__(**kw)
