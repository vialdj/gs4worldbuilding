from astropy import units as u

from gs4worldbuilding.model import RandomizableModel
from gs4worldbuilding.model.bounds import ScalarBounds, QuantityBounds
from gs4worldbuilding.terrestrial import (Atmosphere, Terrestrial, Toxicity,
                                          Size, Core)
from gs4worldbuilding.random import RandomGenerator


class StandardIceAtmosphere(Atmosphere, RandomizableModel):
    '''the standard ice atmosphere model'''
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


class StandardIce(Terrestrial):
    '''the standard ice world model'''
    _temperature_bounds = QuantityBounds(80 * u.K, 230 * u.K)
    _size = Size.STANDARD
    _core = Core.LARGE_IRON_CORE
    _pressure_factor = 1
    _greenhouse_factor = .2
    _hydrographic_coverage_bounds = ScalarBounds(0, .2)
    _absorption = .86
    _atmosphere_type = StandardIceAtmosphere

    def random_hydrographic_coverage(self) -> float:
        '''roll of 2d-10 minimum at 0 and divided by 10'''
        return max(RandomGenerator().roll2d6(-10, continuous=True) / 10, 0)

    def randomize(self) -> None:
        self.hydrographic_coverage = self.random_hydrographic_coverage()
        super().randomize()

    def __init__(self, *args, **kwargs):
        self.hydrographic_coverage = self.random_hydrographic_coverage()
        super().__init__(*args, **kwargs)
