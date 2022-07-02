from enum import Enum
from typing import Optional, List

import numpy as np
from astropy import units as u
from astropy.units import Quantity

from gs4worldbuilding.celestial_object import CelestialObject
from .model.bounds import QuantityBounds
from .model import RandomizableModel
from .random import RandomGenerator
# from .populate_star import populate_star
from .gas_giant_arrangement import GasGiantArrangement


class Luminosity(Enum):
    '''luminosity classes enum'''
    V = 'Main sequence'
    IV = 'Subgiant'
    III = 'Giant'
    D = 'White dwarf'


class Star(RandomizableModel, CelestialObject):
    '''the Star model'''

    def random_seed_mass(self) -> u.Quantity:
        '''consecutive sum of a 3d roll times over Stellar Mass Table with
modifier if applicable'''
        return (RandomGenerator()
                .truncexpon_draw(self.seed_mass_bounds.lower.value,
                                 self.seed_mass_bounds.upper.value,
                                 (.26953477975949597
                                  if self._star_system.garden_host
                                  else .3905806446817353)) * u.M_sun)

    def random_gas_giant_arrangement(self) -> GasGiantArrangement:
        '''sum of a 3d roll times over Gas Giant Arrangement Table'''
        arrangements = {11: GasGiantArrangement.NONE,
                        13: GasGiantArrangement.CONVENTIONAL,
                        15: GasGiantArrangement.ECCENTRIC}
        roll = RandomGenerator().roll3d6()
        filtered = list(filter(lambda x: roll < x[0],
                        list(arrangements.items())))
        return (filtered[0][1] if len(filtered) > 0
                else GasGiantArrangement.EPISTELLAR)

    @staticmethod
    def __l_max(mass) -> float:
        '''l_max fitted through the form a*x**b'''
        if mass >= .45 * u.M_sun:
            return 1.417549268949681 * mass.value ** 3.786542028176919
        return np.nan

    @staticmethod
    def __l_min(mass) -> float:
        '''l_min fitted through the form a*x**b'''
        return 0.8994825154104518 * mass.value ** 4.182711149771404

    @staticmethod
    def __m_span(mass) -> float:
        '''m_span fitted through the form a*exp(b*x)+c'''
        if mass >= .45 * u.M_sun:
            return 355.25732733 * np.exp(-3.62394465 * mass.value) - 1.19842708
        return np.nan

    @staticmethod
    def __s_span(mass) -> float:
        '''s_span fitted through the form a*exp(b*x)'''
        if mass >= .95 * u.M_sun:
            return 18.445568275396568 * np.exp(-2.471832533773299 * mass.value)
        return np.nan

    @staticmethod
    def __g_span(mass) -> float:
        '''g_span fitted through the form a*exp(b*x)'''
        if mass >= .95 * u.M_sun:
            return 11.045171731219448 * np.exp(-2.4574060414344223
                                               * mass.value)
        return np.nan

    @staticmethod
    def __temp_V(mass) -> float:
        '''temp in interval [3100, 8200] as a forth-degree polynomial'''
        return (1659.4884130666383 * mass.value ** 4 - 7449.958040879493
                * mass.value ** 3 + 10805.399314976361 * mass.value ** 2
                - 2568.323443806999 * mass.value + 3296.2303340370468)

    @staticmethod
    def __temp_III(mass) -> float:
        '''temp in interval [3000, 5000] linearly through the form a * x + b'''
        return 1052.63157589 * mass.value + 2105.26315789

    @property
    def mass(self) -> Quantity[u.M_sun]:
        '''read-only mass in M☉ with applied modifiers'''
        return ((.15 + ((self.seed_mass.value - .1) / 1.9) * 1.05) * u.M_sun
                if self.luminosity_class == Luminosity.D
                else self.seed_mass)

    @property
    def seed_mass(self) -> Quantity[u.M_sun]:
        '''mass in M☉ without modifiers'''
        return self._get_bounded_property('seed_mass')

    @property
    def seed_mass_bounds(self) -> QuantityBounds:
        '''value range for mass in M☉'''
        return (QuantityBounds(.6 * u.M_sun, 1.5 * u.M_sun)
                if self._star_system.garden_host
                else QuantityBounds(.1 * u.M_sun, 2 * u.M_sun))

    @seed_mass.setter
    def seed_mass(self, value: Quantity['mass']):
        if not isinstance(value, Quantity):
            raise ValueError('expected quantity type value')
        if 'mass' not in value.unit.physical_type:
            raise AttributeError("can't set seed_mass to value of " +
                                 f'{value.unit.physical_type} physical type')
        self._set_bounded_property('seed_mass', value)

    @property
    def gas_giant_arrangement(self) -> GasGiantArrangement:
        '''gas giant arrangement category over Gas Giant Arrangement Table'''
        return self._gas_giant_arrangement

    @gas_giant_arrangement.setter
    def gas_giant_arrangement(self, value: GasGiantArrangement):
        if not isinstance(value, GasGiantArrangement):
            raise ValueError('gas giant arrangement value type must be ' +
                             f'{GasGiantArrangement}')
        self._gas_giant_arrangement = value

    @property
    def luminosity_class(self) -> Luminosity:
        '''the star luminosity class'''
        m_span = type(self).__m_span(self.seed_mass)
        s_span = type(self).__s_span(self.seed_mass) + m_span
        g_span = type(self).__g_span(self.seed_mass) + s_span
        if (not np.isnan(g_span) and self._star_system.age.value > g_span):
            return Luminosity.D
        elif (not np.isnan(s_span) and self._star_system.age.value > s_span):
            return Luminosity.III
        elif (not np.isnan(m_span) and self._star_system.age.value > m_span):
            return Luminosity.IV
        return Luminosity.V

    @property
    def luminosity(self) -> Quantity[u.L_sun]:
        '''luminosity in L☉'''
        if (self.luminosity_class == Luminosity.D):
            return .001 * u.L_sun
        if (self.luminosity_class == Luminosity.III):
            return type(self).__l_max(self.mass) * 25 * u.L_sun
        if (self.luminosity_class == Luminosity.IV):
            return type(self).__l_max(self.mass) * u.L_sun
        if (np.isnan(type(self).__l_max(self.mass))):
            return type(self).__l_min(self.mass) * u.L_sun
        return (type(self).__l_min(self.mass) +
                (self._star_system.age.value /
                 type(self).__m_span(self.mass)) *
                (type(self).__l_max(self.mass) -
                 type(self).__l_min(self.mass))) * u.L_sun

    @property
    def temperature(self) -> Quantity[u.K]:
        '''read-only effective temperature in K'''
        temp = (type(self).__temp_III(self.mass)
                if self.luminosity_class == Luminosity.III
                else type(self).__temp_V(self.mass))
        if (self.luminosity_class == Luminosity.IV):
            return (temp - ((self._star_system.age.value -
                             type(self).__m_span(self.mass)) /
                            type(self).__s_span(self.mass)) *
                    (temp - 4800)) * u.K
        return temp * u.K

    @property
    def radius(self) -> Quantity[u.au]:
        '''radius in AU'''
        # TODO: handle white dwarf luminosity class
        return ((155000 * np.sqrt(self.luminosity.value)) /
                self.temperature.value ** 2) * u.au

    @property
    def limits(self) -> QuantityBounds:
        '''inner and outer limit in AU'''
        return QuantityBounds(max(0.1 * self.mass.value,
                                  0.01 * np.sqrt(self.luminosity.value))
                              * u.au,
                              40 * self.mass.value * u.au)

    @property
    def forbidden_zone(self) -> Optional[QuantityBounds]:
        '''the forbidden zone limits in AU if any'''
        if (self._companions and len(self._companions) > 0):
            return QuantityBounds(
                    self._companions[0].orbit.min_separation / 3,
                    self._companions[0].orbit.min_separation * 3
                   )
        return None

    @property
    def snow_line(self) -> Quantity[u.au]:
        '''snow line in AU'''
        return 4.85 * np.sqrt(self.__l_min(self.seed_mass)) * u.au

    @property
    def spectral_type(self) -> str:
        '''spectral type from mass'''
        d = {2: 'A5', 1.9: 'A6', 1.8: 'A7', 1.7: 'A9', 1.6: 'F0', 1.5: 'F2',
             1.45: 'F3', 1.4: 'F4', 1.35: 'F5', 1.3: 'F6', 1.25: 'F7',
             1.2: 'F8', 1.15: 'F9', 1.10: 'G0', 1.05: 'G1', 1: 'G2',
             .95: 'G4', .9: 'G6', .85: 'G8', .8: 'K0', .75: 'K2', .7: 'K4',
             .65: 'K5', .6: 'K6', .55: 'K8', .5: 'M0', .45: 'M1', .4: 'M2',
             .35: 'M3', .3: 'M4', .25: 'M4', .2: 'M5', .15: 'M6', .1: 'M7'}
        return ('D' if self.luminosity_class == Luminosity.D
                else d[list(filter(lambda x: x * u.M_sun >= self.mass,
                                   sorted(d.keys())))
                       [0]])

    @property
    def age(self) -> Quantity[u.Ga]:
        '''The attached system age'''
        return self._star_system.age

    def populate(self):
        self._worlds = []
        '''" worlds = populate_star(self)
        for i in range(len(worlds)):
            worlds[i].name = f"{self.name}{chr(ord('b') + i)}"
            self._worlds.append(worlds[i])
            if hasattr(worlds[i], '_moons'):
                for j in range(len(worlds[i]._moons)):
                    worlds[i]._moons[j].name = f"{self.name}{chr(ord('b') + i)}{int_to_roman(j + 1)}"'''

    def randomize(self) -> None:
        self.seed_mass = self.random_seed_mass()
        self.gas_giant_arrangement = self.random_gas_giant_arrangement()

    def __eq__(self, other: 'Star') -> bool:
        return (isinstance(other, type(self)) and
                self.mass == other.mass and
                self.radius == other.radius and
                self.gas_giant_arrangement == other.gas_giant_arrangement and
                self.seed_mass == other.seed_mass and
                self.snow_line == other.snow_line and
                self.luminosity == other.luminosity and
                self.luminosity_class == other.luminosity_class and
                self.temperature == other.temperature and
                self.limits == other.limits)

    def __init__(self, star_system):
        self._star_system = star_system
        self._companions: Optional[List[Star]] = None
        self.seed_mass = self.random_seed_mass()
        self.gas_giant_arrangement = self.random_gas_giant_arrangement()
