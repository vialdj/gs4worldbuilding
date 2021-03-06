from astropy import units as u

from ..random import RandomGenerator
from .. import model
from . import Atmosphere, Terrestrial, Toxicity


class SmallIce(Terrestrial):
    """the small ice world model"""
    _designation = 'Small (Ice)'

    class SmallIceAtmosphere(Atmosphere, model.RandomizableModel):
        """the small ice atmosphere model"""
        _composition = ['N2', 'CH4']
        _suffocating = True

        def randomize(self):
            """sum of a 3d roll to define toxicity conditionally on <= 15"""
            if RandomGenerator().roll3d6() <= 15:
                self._toxicity = Toxicity.MILD
            else:
                self._toxicity = Toxicity.HIGH

    _temperature_bounds = model.bounds.QuantityBounds(80 * u.K, 140 * u.K)
    _size = Terrestrial.Size.SMALL
    _core = Terrestrial.Core.ICY_CORE
    _pressure_factor = 10
    _greenhouse_factor = .1
    _hydrographic_coverage_bounds = model.bounds.ValueBounds(.3, .8)
    _absorption = .93
    _atmosphere = SmallIceAtmosphere

    def random_hydrographic_coverage(self):
        """roll of 1d+2 divided by 10"""
        self.hydrographic_coverage = (RandomGenerator()
                                      .roll1d6(2, continuous=True) / 10)

    def __init__(self, **kw):
        super().__init__(**kw)
