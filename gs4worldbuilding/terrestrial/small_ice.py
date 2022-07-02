from astropy import units as u

from gs4worldbuilding.random import RandomGenerator
from gs4worldbuilding.model.bounds import QuantityBounds, ScalarBounds
from gs4worldbuilding.model import RandomizableModel
from gs4worldbuilding.terrestrial import (Atmosphere, Terrestrial, Toxicity,
                                          Size, Core)


class SmallIceAtmosphere(Atmosphere, RandomizableModel):
    '''the small ice atmosphere model'''
    _composition = ['N2', 'CH4']
    _suffocating = True

    def random_toxicity(self) -> Toxicity:
        '''sum of a 3d roll to define toxicity conditionally on <= 15'''
        return (Toxicity.MILD if RandomGenerator().roll3d6() <= 15
                else Toxicity.HIGH)

    def randomize(self):
        self._toxicity = self.random_toxicity()

    def __init__(self, *args, **kwargs):
        self._toxicity = self.random_toxicity()
        super().__init__(*args, **kwargs)


class SmallIce(Terrestrial):
    '''the small ice world model'''
    _temperature_bounds = QuantityBounds(80 * u.K, 140 * u.K)
    _size = Size.SMALL
    _core = Core.ICY_CORE
    _pressure_factor = 10
    _greenhouse_factor = .1
    _hydrographic_coverage_bounds = ScalarBounds(.3, .8)
    _absorption = .93
    _atmosphere_type = SmallIceAtmosphere

    def random_hydrographic_coverage(self) -> float:
        '''roll of 1d+2 divided by 10'''
        return RandomGenerator().roll1d6(2, continuous=True) / 10

    def randomize(self) -> None:
        self.hydrographic_coverage = self.random_hydrographic_coverage()
        super().randomize()

    def __init__(self, *args, **kwargs):
        self.hydrographic_coverage = self.random_hydrographic_coverage()
        super().__init__(*args, **kwargs)
