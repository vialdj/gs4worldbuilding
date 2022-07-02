from astropy import units as u

from gs4worldbuilding.terrestrial import (Atmosphere, Terrestrial, Toxicity,
                                          Size, Core)
from gs4worldbuilding.model.bounds import ScalarBounds, QuantityBounds
from gs4worldbuilding.random import RandomGenerator


class LargeAmmoniaAtmosphere(Atmosphere):
    '''The large ammonia atmosphere model'''
    _composition = ['He', 'NH3', 'CH4']
    _toxicity = Toxicity.LETHAL
    _suffocating = True
    _corrosive = True


class LargeAmmonia(Terrestrial):
    '''The large ammonia world model'''
    _temperature_bounds = QuantityBounds(140 * u.K, 215 * u.K)
    _size = Size.LARGE
    _core = Core.ICY_CORE
    _pressure_factor = 5
    _greenhouse_factor = .2
    _hydrographic_coverage_bounds = ScalarBounds(.2, 1)
    _absorption = .84
    _atmosphere_type = LargeAmmoniaAtmosphere

    def random_hydrographic_coverage(self) -> float:
        '''roll of 2d capped at 10 and divided by 10'''
        return min(RandomGenerator().roll2d6(continuous=True) / 10, 1)

    def randomize(self) -> None:
        self.hydrographic_coverage = self.random_hydrographic_coverage()
        super().randomize()

    def __init__(self, *args, **kwargs):
        self.hydrographic_coverage = self.random_hydrographic_coverage()
        super().__init__(*args, **kwargs)
