from astropy import units as u

from . import Atmosphere, Terrestrial, Toxicity
from .. import model
from ..random import RandomGenerator


class StandardGreenhouse(Terrestrial):
    """the standard greenhouse world model"""
    _designation = 'Standard (Greenhouse)'

    class StandardGreenhouseAtmosphere(Atmosphere):
        """the standard greenhouse atmosphere model"""
        _toxicity = Toxicity.LETHAL
        _suffocating = True
        _corrosive = True

        @property
        def composition(self):
            return (['CO2'] if self._world.hydrographic_coverage < .1
                    else ['N2', 'H2O', 'O2'])

    _temperature_bounds = model.bounds.QuantityBounds(500 * u.K, 950 * u.K)
    _size = Terrestrial.Size.STANDARD
    _core = Terrestrial.Core.LARGE_IRON_CORE
    _pressure_factor = 100
    _greenhouse_factor = 2.0
    _hydrographic_coverage_bounds = model.bounds.ValueBounds(0, .5)
    _absorption = .77
    _atmosphere = StandardGreenhouseAtmosphere

    def random_hydrographic_coverage(self):
        """roll of 2d-7 minimum at 0 and divided by 10"""
        self.hydrographic_coverage = max(RandomGenerator()
                                         .roll2d6(-7, continuous=True) / 10, 0)

    def __init__(self, **kw):
        super().__init__(**kw)
