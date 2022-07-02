from astropy import units as u

from gs4worldbuilding.terrestrial import Terrestrial, Toxicity, Size, Core
from gs4worldbuilding.model.bounds import QuantityBounds, ScalarBounds
from gs4worldbuilding.random import RandomGenerator
from gs4worldbuilding.terrestrial.atmosphere import Atmosphere
from gs4worldbuilding.terrestrial.marginal_atmosphere import MarginalCandidate


class LargeGreenhouseAtmosphere(Atmosphere):
    '''The large greenhouse atmosphere model'''
    _toxicity = Toxicity.LETHAL
    _suffocating = True
    _corrosive = True

    @property
    def composition(self):
        return (['CO2'] if self._world.hydrographic_coverage < .1
                else ['N2', 'H2O', 'O2'])


class LargeGreenhouse(Terrestrial):
    '''The large greenhouse world model'''
    _temperature_bounds = QuantityBounds(500 * u.K, 950 * u.K)
    _size = Size.LARGE
    _core = Core.LARGE_IRON_CORE
    _pressure_factor = 500
    _greenhouse_factor = 2.0
    _hydrographic_coverage_bounds = ScalarBounds(0, .5)
    _absorption = .77
    _atmosphere_type = LargeGreenhouseAtmosphere

    def random_hydrographic_coverage(self) -> float:
        '''roll of 2d-7 minimum at 0 and divided by 10'''
        return max(RandomGenerator().roll2d6(-7, continuous=True) / 10, 0)

    def randomize(self) -> None:
        self.hydrographic_coverage = self.random_hydrographic_coverage()
        super().randomize()

    def __init__(self, *args, **kwargs):
        self.hydrographic_coverage = self.random_hydrographic_coverage()
        super().__init__(*args, **kwargs)
