from enum import IntEnum, auto
from abc import ABC, abstractmethod

from astropy import units as u
from astropy.units import Quantity
import numpy as np
from ordered_enum import OrderedEnum

from gs4worldbuilding.planet import Planet
from gs4worldbuilding import units
from gs4worldbuilding.model.bounds import ScalarBounds, QuantityBounds
from gs4worldbuilding.random import RandomGenerator
from gs4worldbuilding.orbit import Orbit
from gs4worldbuilding.gas_giant_arrangement import GasGiantArrangement
from gs4worldbuilding.star import Star


class Size(OrderedEnum, IntEnum):
    '''class Size Enum for gas giants'''
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()


class GasGiantOrbit(Orbit):
    '''The gas giant orbit model'''

    # TODO: watchout for epistellar modifier
    def random_eccentricity(self) -> float:
        if (self.parent_body.gas_giant_arrangement ==
                GasGiantArrangement.ECCENTRIC and
                self.radius <= self.parent_body.snow_line):
            return (RandomGenerator().truncnorm_draw(.1, .8, .45435,
                                                     .23165400385057022))
        return (RandomGenerator().truncnorm_draw(.0, .2, .04625,
                                                 .042877004326328585))

    @property
    def parent_body(self) -> Star:
        return self.parent_body

    @property
    # TODO: watchout for epistellar modifier
    def eccentricity_bounds(self) -> ScalarBounds:
        '''value range for eccentricity dependent separation'''
        if (self.parent_body.gas_giant_arrangement
                == GasGiantArrangement.ECCENTRIC and
                self.radius <= self.parent_body.snow_line):
            return ScalarBounds(.1, .8)
        else:
            return ScalarBounds(.0, .2)

    def __init__(self, parent_body: Star, radius: Quantity['length'],
                 body: 'GasGiant'):
        super().__init__(parent_body, radius, body)


class GasGiant(Planet, ABC):
    '''the World Model'''

    _precedence = ['mass', 'rotation', 'resonant', 'retrograde', 'axial_tilt']
    _size: Size
    _mass_bounds: QuantityBounds
    _rotation_modifiers = {Size.SMALL: 6,
                           Size.MEDIUM: 0,
                           Size.LARGE: 0}

    @abstractmethod
    def random_mass(self) -> Quantity['mass']:
        '''random mass in M🜨'''

    @property
    def size(self) -> Size:
        '''size class variable'''
        return self._size

    @property
    def mass(self) -> Quantity[u.M_earth]:
        '''mass in M🜨'''
        return self._get_bounded_property('mass')

    @property
    def mass_bounds(self) -> QuantityBounds:
        '''Mass range static class variable in M🜨'''
        return self._mass_bounds

    @mass.setter
    def mass(self, value: Quantity['mass']):
        if not isinstance(value, Quantity):
            raise ValueError('expected quantity type value')
        if 'mass' not in value.unit.physical_type:
            raise ValueError("can't set mass to value of " +
                             f'physical type {value.unit.physical_type}')
        self._set_bounded_property('mass', value.to(u.M_earth))

    @property
    def moons(self):
        return super().moons + self._n_captured

    @property
    def diameter(self) -> Quantity['length']:
        '''diameter in D🜨'''
        return (np.power(self.mass.value / self.density.value, (1 / 3))
                * units.D_earth)

    @property
    @abstractmethod
    def density(self) -> Quantity['mass density']:
        '''density in d🜨'''

    @property
    def gravity(self) -> Quantity['acceleration']:
        '''surface gravity in g'''
        return self.density.value * self.diameter.value * units.G_earth

    def randomize(self) -> None:
        self.mass = self.random_mass()
        self.rotation = self.random_rotation()
        self.resonant = self.random_resonant()
        self.retrograde = self.random_retrograde()
        self.axial_tilt = self.random_axial_tilt()

    def __init__(self, parent_body, radius):
        self._orbit = GasGiantOrbit(parent_body, radius, self)
        self.mass = self.random_mass()
        self.rotation = self.random_rotation()
        self.resonant = self.random_resonant()
        self.retrograde = self.random_retrograde()
        self.axial_tilt = self.random_axial_tilt()


class SmallGasGiant(GasGiant):
    '''The small gas giant model'''
    _designation = 'Small Gas Giant'

    _mass_bounds = QuantityBounds(10 * u.M_earth, 80 * u.M_earth)
    _size = Size.SMALL

    def random_mass(self) -> Quantity['mass']:
        '''small mass pdf fit as a truncated exponential'''
        return (RandomGenerator()
                .truncexpon_draw(10, 80, 17.69518578597015) *
                u.M_earth)

    @property
    def density(self) -> Quantity['mass density']:
        '''small density in d🜨 from Gas Giant Size Table fitted as ax**b+c'''
        return (74.43464003356911 * self.mass.value ** -2.473690314600168
                + .17) * units.d_earth


class MediumGasGiant(GasGiant):
    '''The medium gas giant model'''
    _designation = 'Medium Gas Giant'

    _mass_bounds = QuantityBounds(100 * u.M_earth, 500 * u.M_earth)
    _size = Size.MEDIUM

    def random_mass(self) -> Quantity['mass']:
        '''medium mass pdf fit as a truncated normal'''
        return (RandomGenerator()
                .truncexpon_draw(100, 500, 102.41483046902924) *
                u.M_earth)

    @property
    def density(self) -> Quantity['mass density']:
        '''medium density in d🜨 from Gas Giant Size Table fitted as ax+b'''
        return ((.0002766666669434452 * self.mass.value + .15033333325029977)
                * units.d_earth)


class LargeGasGiant(GasGiant):
    '''The large gas giant model'''
    _designation = 'Large Gas Giant'

    _mass_bounds = QuantityBounds(600 * u.M_earth, 4000 * u.M_earth)
    _size = Size.LARGE

    def random_mass(self) -> Quantity['mass']:
        '''large mass pdf fit as a truncated exponential'''
        return (RandomGenerator()
                .truncexpon_draw(600, 4000, 872.1918137657565) *
                u.M_earth)

    @property
    def density(self) -> Quantity['mass density']:
        '''large density in d🜨 from Gas Giant Size Table fitted as ax+b'''
        return ((.0003880597018732323 * self.mass.value + .036185736947409355)
                * units.d_earth)