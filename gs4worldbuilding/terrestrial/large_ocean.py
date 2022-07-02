from astropy import units as u

from gs4worldbuilding.terrestrial import (Atmosphere, Terrestrial,
                                          Toxicity, Size, Core)
from gs4worldbuilding.model.bounds import QuantityBounds, ScalarBounds
from gs4worldbuilding.random import RandomGenerator


class LargeOceanAtmosphere(Atmosphere):
    '''the large ocean atmosphere model'''
    _composition = ['He', 'N2']
    _toxicity = Toxicity.HIGH
    _suffocating = True


class LargeOcean(Terrestrial):
    '''the large ocean world model'''
    _temperature_bounds = QuantityBounds(250 * u.K, 340 * u.K)
    _size = Size.LARGE
    _core = Core.LARGE_IRON_CORE
    _pressure_factor = 5
    _greenhouse_factor = .16
    _hydrographic_coverage_bounds = ScalarBounds(.7, 1)
    _atmosphere_type = LargeOceanAtmosphere

    def random_hydrographic_coverage(self):
        '''roll of 1d+6 maxed at 10 divided by 10'''
        return min(RandomGenerator().roll1d6(6, continuous=True), 10) / 10

    @property
    def absorption(self):
        '''absorbtion from Temperature Factors Table fitted
through a * x ** 3 + b * x ** 2 + c * x + d'''
        assert self.hydrographic_coverage is not None
        return min(.95, (-0.7500000000000038 *
                         self.hydrographic_coverage ** 3 +
                   1.2000000000000057 * self.hydrographic_coverage ** 2 -
                   0.6475000000000023 * self.hydrographic_coverage +
                   1.0375000000000003))

    def randomize(self) -> None:
        self.hydrographic_coverage = self.random_hydrographic_coverage()
        super().randomize()

    def __init__(self, *args, **kwargs):
        self.hydrographic_coverage = self.random_hydrographic_coverage()
        super().__init__(*args, **kwargs)
