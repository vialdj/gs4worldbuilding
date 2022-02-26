# -*- coding: utf-8 -*-

from .. import model
from . import Atmosphere, Terrestrial
from ..random import RandomGenerator

from astropy import units as u


class StandardIce(Terrestrial):
    """the standard ice world model"""
    _designation = 'Standard (Ice)'

    class StandardIceAtmosphere(Atmosphere, model.RandomizableModel):
        """the standard ice atmosphere model"""
        _composition = ['CO2', 'N2']
        _suffocating = True

        def randomize(self):
            """sum of a 3d roll to define toxicity if value > 12"""
            if RandomGenerator().roll3d6() > 12:
                self._toxicity = Atmosphere.Toxicity.MILD

    _temperature_bounds = model.bounds.QuantityBounds(80 * u.K, 230 * u.K)
    _size = Terrestrial.Size.STANDARD
    _core = Terrestrial.Core.LARGE_IRON_CORE
    _pressure_factor = 1
    _greenhouse_factor = .2
    _hydrographic_coverage_bounds = model.bounds.ValueBounds(0, .2)
    _absorption = .86
    _atmosphere = StandardIceAtmosphere

    def random_hydrographic_coverage(self):
        """roll of 2d-10 minimum at 0 and divided by 10"""
        self.hydrographic_coverage = max(RandomGenerator().roll2d6(-10, continuous=True) / 10, 0)

    def __init__(self, **kw):
        super(StandardIce, self).__init__(**kw)
