# -*- coding: utf-8 -*-

from . import Atmosphere, Terrestrial
from .. import model
from ..random import roll2d6

from astropy import units as u


class StandardAmmonia(Terrestrial):
    """the standard ammonia world model"""
    _designation = 'Standard (Ammonia)'

    class StandardAmmoniaAtmosphere(Atmosphere):
        """the standard ammonia atmosphere model"""
        _composition = ['N2', 'NH3', 'CH4']
        _toxicity = Atmosphere.Toxicity.LETHAL
        _suffocating = True
        _corrosive = True

    _temperature_bounds = model.bounds.QuantityBounds(140 * u.K, 215 * u.K)
    _size = Terrestrial.Size.STANDARD
    _core = Terrestrial.Core.ICY_CORE
    _pressure_factor = 1
    _greenhouse_factor = .2
    _hydrographic_coverage_bounds = model.bounds.ValueBounds(.2, 1)
    _absorption = .84
    _atmosphere = StandardAmmoniaAtmosphere

    def random_hydrographic_coverage(self):
        """roll of 2d maximum at 10 and divided by 10"""
        self.hydrographic_coverage = min(roll2d6(continuous=True) / 10, 1)

    def __init__(self, **kw):
        super(StandardAmmonia, self).__init__(**kw)
