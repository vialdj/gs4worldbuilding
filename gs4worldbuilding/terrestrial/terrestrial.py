from enum import Enum
from abc import ABC
from typing import Callable, Optional, Type, List, Tuple

from ordered_enum import OrderedEnum
from astropy import units as u
import numpy as np


from gs4worldbuilding.world import World, Resource, Climate
from gs4worldbuilding.model import RandomizableModel
from gs4worldbuilding.model.bounds import ScalarBounds, EnumBounds, QuantityBounds
from gs4worldbuilding.units import d_earth, D_earth, G_earth
from gs4worldbuilding.random import RandomGenerator
from gs4worldbuilding.terrestrial.marginal_atmosphere import MarginalMixin
from gs4worldbuilding.terrestrial.atmosphere import Atmosphere, Pressure


class Size(tuple, OrderedEnum):
    '''Size Enum for terrestrials from Size Constraints Table'''
    TINY = (.004, .024)
    SMALL = (.024, .030)
    STANDARD = (.030, .065)
    LARGE = (.065, .091)


class Core(tuple, Enum):
    '''Core Enum from World Density Table'''
    ICY_CORE = (.3 * d_earth, .7 * d_earth)
    SMALL_IRON_CORE = (.6 * d_earth, 1 * d_earth)
    LARGE_IRON_CORE = (.8 * d_earth, 1.2 * d_earth)


class Terrestrial(World, ABC):
    '''the Terrestrial World Model'''
    _resource_bounds = EnumBounds(Resource.SCANT, Resource.RICH)
    _core: Core
    _size: Size
    _pressure_factor: Optional[float] = None
    _greenhouse_factor: Optional[float] = None
    _atmosphere_type: Optional[Type[Atmosphere]] = None
    _hydrographic_coverage_bounds: Optional[ScalarBounds] = None
    _habitability_filters: List[Tuple[Callable[['Terrestrial'], bool],
                                      int]] = [
        (lambda x: x.hydrographic_coverage is not None and
         x.hydrographic_coverage >= .1 and
         x.hydrographic_coverage < .6, 1),
        (lambda x: x.hydrographic_coverage is not None and
         x.hydrographic_coverage >= .6 and
         x.hydrographic_coverage < .9, 2),
        (lambda x: x.hydrographic_coverage is not None and
         x.hydrographic_coverage >= .9, 2),
        (lambda x: x.atmosphere is not None and
         x.atmosphere.breathable and
         x.atmosphere.pressure_category == Pressure.VERY_THIN, 1),
        (lambda x: x.atmosphere is not None and
         x.atmosphere.breathable and
         x.atmosphere.pressure_category == Pressure.THIN, 2),
        (lambda x: x.atmosphere is not None and
         x.atmosphere.breathable and
         x.atmosphere.pressure_category in
         [Pressure.STANDARD, Pressure.DENSE], 3),
        (lambda x: x.atmosphere is not None and
         x.atmosphere.breathable and
         x.atmosphere.pressure_category in
         [Pressure.VERY_DENSE, Pressure.SUPER_DENSE], 1),
        (lambda x: x.atmosphere is not None and
         x.atmosphere.breathable and
         not issubclass(type(x.atmosphere), MarginalMixin), 1),
        (lambda x: x.atmosphere is not None and
         x.atmosphere.breathable and
         x.climate == Climate.COLD, 1),
        (lambda x: x.atmosphere is not None and
         x.atmosphere.breathable and
         x.climate >= Climate.CHILLY and
         x.climate <= Climate.TROPICAL, 2),
        (lambda x: x.atmosphere is not None and
         x.atmosphere.breathable and
         x.climate == Climate.HOT, 1),
        (lambda x: x.atmosphere is not None and
         not x.atmosphere.breathable and
         x.atmosphere.corrosive, -2),
        (lambda x: x.atmosphere is not None and
         not x.atmosphere.breathable and
         x.atmosphere.suffocating, -1)
    ]
    _resource_table = {
        3: Resource.SCANT,
        5: Resource.VERY_POOR,
        8: Resource.POOR,
        14: Resource.AVERAGE,
        17: Resource.ABUNDANT,
        19: Resource.VERY_ABUNDANT
    }

    def _roll_resource(self, modifier: int = 0) -> Resource:
        roll = RandomGenerator().roll3d6(modifier)
        filtered = list(filter(lambda x: roll < x,
                               self._resource_table.keys()))
        return (self._resource_table[filtered[0]] if len(filtered) > 0
                else Resource.RICH)

    def random_resource(self) -> Resource:
        '''sum of a 3d roll times over Resource Value Table'''
        return self._roll_resource()

    def random_density(self) -> u.Quantity[d_earth]:
        '''sum of a 3d6 roll over World Density Table'''
        return (self.density_bounds.lower + (self.density_bounds.upper -
                                             self.density_bounds.lower) *
                RandomGenerator().truncnorm_draw(0, 1, .376, .2))

    def random_diameter(self) -> u.Quantity[D_earth]:
        '''roll of 2d6-2 in range [Dmin, Dmax]'''
        if self.size is not None and self.core is not None:
            return (self.diameter_bounds.lower +
                    (RandomGenerator().roll2d6(-2, continuous=True) / 10) *
                    (self.diameter_bounds.upper - self.diameter_bounds.lower))

    def random_volatile_mass(self) -> Optional[float]:
        '''sum of a 3d6 roll divided by 10'''
        if self._atmosphere_type is not None:
            return RandomGenerator().roll3d6(continuous=True) / 10

    @property
    def core(self) -> Core:
        '''core class variable'''
        return self._core

    @property
    def pressure_factor(self) -> Optional[float]:
        '''pressure factor class variable'''
        return self._pressure_factor

    @property
    def greenhouse_factor(self) -> Optional[float]:
        '''greenhouse_factor class variable'''
        return self._greenhouse_factor

    @property
    def atmosphere(self) -> Optional[Atmosphere]:
        '''the terrestrial atmosphere property'''
        return self._atmosphere

    @property
    def volatile_mass(self) -> Optional[float]:
        '''relative supply of gaseous elements to other worlds of
the same type'''
        if self.volatile_mass_bounds is not None:
            return self._get_bounded_property('volatile_mass')

    @property
    def volatile_mass_bounds(self) -> Optional[ScalarBounds]:
        '''computed value range for volatile mass'''
        return ScalarBounds(.3, 1.8) if self._atmosphere_type else None

    @volatile_mass.setter
    def volatile_mass(self, value: Optional[float]) -> None:
        if value is not None:
            self._set_bounded_property('volatile_mass', value)
        else:
            self._volatile_mass = value

    @property
    def density(self) -> u.Quantity[d_earth]:
        '''density in earth density'''
        return self._get_bounded_property('density')

    @property
    def density_bounds(self) -> QuantityBounds:
        '''value range for density'''
        return QuantityBounds(*self.core.value)

    @density.setter
    def density(self, value: u.Quantity['mass density']) -> None:
        if not isinstance(value, u.Quantity):
            raise ValueError('expected quantity type value')
        if 'mass density' not in value.unit.physical_type:
            raise ValueError("can't set diameter to value of " +
                             f'{value.unit.physical_type} physical type')
        self._set_bounded_property('density', value.to(d_earth))

    @property
    def gravity(self) -> u.Quantity[G_earth]:
        '''surface gravity in g'''
        return self.density.value * self.diameter.value * G_earth

    @property
    def hydrographic_coverage(self) -> Optional[float]:
        '''proportion of surface covered by liquid elements'''
        if self._hydrographic_coverage_bounds:
            return self._get_bounded_property('hydrographic_coverage')

    @property
    def hydrographic_coverage_bounds(self) -> Optional[ScalarBounds]:
        '''hydrographic_coverage value range class variable'''
        return self._hydrographic_coverage_bounds

    @hydrographic_coverage.setter
    def hydrographic_coverage(self, value: Optional[float]) -> None:
        if not isinstance(value, float):
            raise ValueError("hydrographic_coverage should be a float")
        self._set_bounded_property('hydrographic_coverage', value)


    @property
    def diameter(self) -> u.Quantity[D_earth]:
        '''diameter in D🜨'''
        return self._get_bounded_property('diameter')

    @property
    def diameter_bounds(self) -> QuantityBounds:
        '''computed value range for diameter'''
        return QuantityBounds(np.sqrt(self.blackbody_temperature.value /
                                      self.density.value) *
                              self.size[0] * D_earth,
                              np.sqrt(self.blackbody_temperature.value /
                                      self.density.value)
                              * self.size[1] * D_earth)

    @diameter.setter
    def diameter(self, value: u.Quantity['length']):
        if not isinstance(value, u.Quantity):
            raise ValueError('expected quantity type value')
        if 'length' not in value.unit.physical_type:
            raise ValueError("can't set diameter to value of " +
                             f'{value.unit.physical_type} physical type')
        self._set_bounded_property('diameter', value.to(D_earth))

    @property
    def blackbody_correction(self) -> float:
        return ((self.absorption *
                 (1 + self.volatile_mass * self.greenhouse_factor))
                if self.volatile_mass is not None and
                self.greenhouse_factor is not None
                else self.absorption)

    @property
    def blackbody_temperature(self) -> u.Quantity[u.K]:
        '''blackbody temperature in K'''
        return self.temperature / self.blackbody_correction

    @property
    def mass(self) -> u.Quantity[u.M_earth]:
        '''mass in M🜨'''
        return self.density.value * self.diameter.value ** 3 * u.M_earth

    @property
    def habitability(self) -> int:
        '''the habitability score'''
        return sum(score if filter(self) else 0
                   for filter, score in self._habitability_filters)

    @property
    def size(self) -> Size:
        '''the size property'''
        return self._size

    def randomize(self) -> None:
        self.volatile_mass = self.random_volatile_mass()
        self.density = self.random_density()
        self.temperature = self.random_temperature()
        self.diameter = self.random_diameter()
        if isinstance(self.atmosphere, RandomizableModel):
            self.atmosphere.randomize()
        self.resource = self.random_resource()

    def __init__(self):
        self.volatile_mass = self.random_volatile_mass()
        self.density = self.random_density()
        self.temperature = self.random_temperature()
        self.diameter = self.random_diameter()
        self._atmosphere: Optional[Atmosphere] = (self._atmosphere_type(self)
                                                  if self._atmosphere_type
                                                  else None)
        self.resource = self.random_resource()
