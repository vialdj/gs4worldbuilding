from astropy import units as u

from gs4worldbuilding.terrestrial import (Atmosphere, Terrestrial,
                                          Toxicity, Size, Core)
from gs4worldbuilding.model.bounds import QuantityBounds, ScalarBounds
from gs4worldbuilding.random import RandomGenerator


class LargeIceAtmosphere(Atmosphere):
    '''the large ice atmosphere model'''
    _composition = ['He', 'N2']
    _toxicity = Toxicity.HIGH
    _suffocating = True


class LargeIce(Terrestrial):
    '''the large ice world model'''
    _temperature_bounds = QuantityBounds(80 * u.K, 230 * u.K)
    _size = Size.LARGE
    _core = Core.LARGE_IRON_CORE
    _pressure_factor = 5
    _greenhouse_factor = .2
    _hydrographic_coverage_bounds = ScalarBounds(0, .2)
    _absorption = .86
    _atmosphere_type = LargeIceAtmosphere

    def random_hydrographic_coverage(self) -> float:
        '''roll of 2d-10 minimum at 0 and divided by 10'''
        return max(RandomGenerator().roll2d6(-10, continuous=True) / 10, 0)

    def randomize(self) -> None:
        self.hydrographic_coverage = self.random_hydrographic_coverage()
        super().randomize()

    def __init__(self, *args, **kwargs):
        self.hydrographic_coverage = self.random_hydrographic_coverage()
        super().__init__(*args, **kwargs)
