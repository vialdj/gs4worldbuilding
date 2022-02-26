# -*- coding: utf-8 -*-

from . import Atmosphere, Terrestrial
from .. import model
from ..random import RandomGenerator

from astropy import units as u


class LargeAmmonia(Terrestrial):
    """The large ammonia world model"""
    _designation = 'Large (Ammonia)'

    class LargeAmmoniaAtmosphere(Atmosphere):
        """The large ammonia atmosphere model"""
        _composition = ['He', 'NH3', 'CH4']
        _toxicity = Atmosphere.Toxicity.LETHAL
        _suffocating = True
        _corrosive = True

    _temperature_bounds = model.bounds.QuantityBounds(140 * u.K, 215 * u.K)
    _size = Terrestrial.Size.LARGE
    _core = Terrestrial.Core.ICY_CORE
    _pressure_factor = 5
    _greenhouse_factor = .2
    _hydrographic_coverage_bounds = model.bounds.ValueBounds(.2, 1)
    _absorption = .84
    _atmosphere = LargeAmmoniaAtmosphere

    def random_hydrographic_coverage(self):
        """roll of 2d capped at 10 and divided by 10"""
        self.hydrographic_coverage = min(RandomGenerator().roll2d6(continuous=True) / 10, 1)

    def __init__(self, **kw):
        super(LargeAmmonia, self).__init__(**kw)
