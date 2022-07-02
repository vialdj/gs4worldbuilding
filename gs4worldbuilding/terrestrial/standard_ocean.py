from astropy import units as u

from gs4worldbuilding.random import RandomGenerator
from gs4worldbuilding.model import RandomizableModel
from gs4worldbuilding.model.bounds import QuantityBounds, ScalarBounds
from gs4worldbuilding.terrestrial import (Atmosphere, Terrestrial, Toxicity,
                                          Size, Core)


class StandardOceanAtmosphere(Atmosphere, RandomizableModel):
    '''the standard ocean atmosphere model'''
    _composition = ['CO2', 'N2']
    _suffocating = True

    def random_toxicity(self) -> Toxicity:
        '''sum of a 3d roll to define toxicity if value > 12'''
        return (Toxicity.MILD if RandomGenerator().roll3d6() > 12
                else Toxicity.NONE)

    def randomize(self):
        self._toxicity = self.random_toxicity()

    def __init__(self, *args, **kwargs):
        self._toxicity = self.random_toxicity()
        super().__init__(*args, **kwargs)


class StandardOcean(Terrestrial):
    '''the standard ocean world model'''
    _temperature_bounds = QuantityBounds(250 * u.K, 340 * u.K)
    _size = Size.STANDARD
    _core = Core.LARGE_IRON_CORE
    _pressure_factor = 1
    _greenhouse_factor = .16
    _hydrographic_coverage_bounds = ScalarBounds(.5, 1)
    _atmosphere_type = StandardOceanAtmosphere

    def random_hydrographic_coverage(self) -> float:
        '''roll of 1d+4 divided by 10'''
        return RandomGenerator().roll1d6(4, continuous=True) / 10

    @property
    def absorption(self):
        '''absorbtion from Temperature Factors Table fitted
through a * x ** 3 + b * x ** 2 + c * x + d'''
        assert self.hydrographic_coverage is not None
        return min(.95,
                   (-0.7500000000000038 * self.hydrographic_coverage ** 3 +
                    1.2000000000000057 * self.hydrographic_coverage ** 2 -
                    0.6475000000000023 * self.hydrographic_coverage +
                    1.0375000000000003))

    def randomize(self) -> None:
        self.hydrographic_coverage = self.random_hydrographic_coverage()
        super().randomize()

    def __init__(self, *args, **kwargs):
        self.hydrographic_coverage = self.random_hydrographic_coverage()
        super().__init__(*args, **kwargs)
