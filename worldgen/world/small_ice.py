# -*- coding: utf-8 -*-

from .. import model
from . import Atmosphere, World

from random import uniform

from astropy import units as u


class SmallIce(World):
    """the small ice world model"""

    class SmallIceAtmosphere(Atmosphere, model.RandomizableModel):
        """the small ice atmosphere model"""
        _composition = ['N2', 'CH4']
        _suffocating = True

        def randomize(self):
            """sum of a 3d roll to define toxicity conditionally on <= 15"""
            if uniform(0, 1) < .9537:
                self._toxicity = Atmosphere.Toxicity.MILD
            else:
                self._toxicity = Atmosphere.Toxicity.HIGH

    _temperature_bounds = model.bounds.QuantityBounds(80 * u.K, 140 * u.K)
    _size = World.Size.SMALL
    _core = World.Core.ICY_CORE
    _pressure_factor = 10
    _greenhouse_factor = .1
    _hydrosphere_bounds = model.bounds.ValueBounds(.3, .8)
    _absorption = .93
    _atmosphere = SmallIceAtmosphere

    def random_hydrosphere(self):
        """roll of 1d+2 divided by 10"""
        self.hydrosphere = uniform(.3, .8)

    def __init__(self, **kw):
        super(SmallIce, self).__init__(**kw)
