# -*- coding: utf-8 -*-

from . import model
from .random import truncexpon_draw, roll3d6
from .populate_star import populate_star

from enum import Enum

import numpy as np
from astropy import units as u


class Star(model.RandomizableModel):
    """the Star model on its main sequence"""

    _precedence = ['seed_mass', 'gas_giant_arrangement']

    class Luminosity(Enum):
        V = 'Main sequence'
        IV = 'Subgiant'
        III = 'Giant'
        D = 'White dwarf'

    class GasGiantArrangement(Enum):
        """class arrangemeent category Enum from Gas Giant Arrangement table"""
        NONE = 'No gas giant'
        CONVENTIONAL = 'Conventional gas giant'
        ECCENTRIC = 'Eccentric gas giant'
        EPISTELLAR = 'Epistellar gas giant'

    def random_seed_mass(self):
        """consecutive sum of a 3d roll times over Stellar Mass Table with
modifier if applicable"""
        self.seed_mass = truncexpon_draw(self.seed_mass_bounds.min.value,
                                         self.seed_mass_bounds.max.value,
                                         (.26953477975949597
                                          if self._star_system.garden_host
                                          else .3905806446817353)) * u.M_sun

    def random_gas_giant_arrangement(self):
        """sum of a 3d roll times over Gas Giant Arrangement Table"""
        arrangements = {11: self.GasGiantArrangement.NONE,
                        13: self.GasGiantArrangement.CONVENTIONAL,
                        15: self.GasGiantArrangement.ECCENTRIC}
        roll = roll3d6()
        filtered = list(filter(lambda x: roll < x[0],
                               list(arrangements.items())))

        self.gas_giant_arrangement = (filtered[0][1] if len(filtered) > 0
                                      else self.GasGiantArrangement.EPISTELLAR)

    @staticmethod
    def __l_max(mass):
        """l_max fitted through the form a*x**b"""
        if mass >= .45 * u.M_sun:
            return 1.417549268949681 * mass.value ** 3.786542028176919
        return np.nan

    @staticmethod
    def __l_min(mass):
        """l_min fitted through the form a*x**b"""
        return 0.8994825154104518 * mass.value ** 4.182711149771404

    @staticmethod
    def __m_span(mass):
        """m_span fitted through the form a*exp(b*x)+c"""
        if mass >= .45 * u.M_sun:
            return 355.25732733 * np.exp(-3.62394465 * mass.value) - 1.19842708
        return np.nan

    @staticmethod
    def __s_span(mass):
        """s_span fitted through the form a*exp(b*x)"""
        if mass >= .95 * u.M_sun:
            return 18.445568275396568 * np.exp(-2.471832533773299 * mass.value)
        return np.nan

    @staticmethod
    def __g_span(mass):
        """g_span fitted through the form a*exp(b*x)"""
        if mass >= .95 * u.M_sun:
            return 11.045171731219448 * np.exp(-2.4574060414344223
                                               * mass.value)
        return np.nan

    @staticmethod
    def __temp_V(mass):
        """temp in interval [3100, 8200] as a forth-degree polynomial"""
        return (1659.4884130666383 * mass.value ** 4 - 7449.958040879493
                * mass.value ** 3 + 10805.399314976361 * mass.value ** 2
                - 2568.323443806999 * mass.value + 3296.2303340370468)

    @staticmethod
    def __temp_III(mass):
        """temp in interval [3000, 5000] linearly through the form a * x + b"""
        return 1052.63157589 * mass.value + 2105.26315789

    @property
    def mass(self) -> u.Quantity:
        """read-only mass in M☉ with applied modifiers"""
        return ((.15 + ((self.seed_mass.value - .1) / 1.9) * 1.05) * u.M_sun
                if self.luminosity_class == type(self).Luminosity.D
                else self.seed_mass)

    @property
    def seed_mass(self) -> u.Quantity:
        """mass in M☉ without modifiers"""
        return self._get_bounded_property('seed_mass') * u.M_sun

    @property
    def seed_mass_bounds(self) -> model.bounds.QuantityBounds:
        """value range for mass in M☉"""
        return (model.bounds.QuantityBounds(.6 * u.M_sun,
                                            1.5 * u.M_sun)
                if self._star_system.garden_host
                else model.bounds.QuantityBounds(.1 * u.M_sun,
                                                 2 * u.M_sun))

    @seed_mass.setter
    def seed_mass(self, value: u.Quantity):
        if not isinstance(value, u.Quantity):
            raise ValueError('expected quantity type value')
        if 'mass' not in value.unit.physical_type:
            raise AttributeError('can\'t set seed_mass to value of %s physical type' %
                                 value.unit.physical_type)
        self._set_bounded_property('seed_mass', value)

    @property
    def gas_giant_arrangement(self) -> GasGiantArrangement:
        """gas giant arrangement category over Gas Giant Arrangement Table"""
        return self._gas_giant_arrangement

    @gas_giant_arrangement.setter
    def gas_giant_arrangement(self, value: GasGiantArrangement):
        if not isinstance(value, self.GasGiantArrangement):
            raise ValueError('gas giant arrangement value type must be {}'
                             .format(self.GasGiantArrangement))
        self._gas_giant_arrangement = value

    @property
    def luminosity_class(self) -> Luminosity:
        """the star luminosity class"""
        m_span = type(self).__m_span(self.seed_mass)
        s_span = type(self).__s_span(self.seed_mass) + m_span
        g_span = type(self).__g_span(self.seed_mass) + s_span
        if (not np.isnan(g_span) and self._star_system.age.value > g_span):
            return type(self).Luminosity.D
        elif (not np.isnan(s_span) and self._star_system.age.value > s_span):
            return type(self).Luminosity.III
        elif (not np.isnan(m_span) and self._star_system.age.value > m_span):
            return type(self).Luminosity.IV
        return type(self).Luminosity.V

    @property
    def luminosity(self) -> u.Quantity:
        """luminosity in L☉"""
        if (self.luminosity_class == type(self).Luminosity.D):
            return .001 * u.L_sun
        if (self.luminosity_class == type(self).Luminosity.III):
            return type(self).__l_max(self.mass) * 25 * u.L_sun
        if (self.luminosity_class == type(self).Luminosity.IV):
            return type(self).__l_max(self.mass) * u.L_sun
        if (np.isnan(type(self).__l_max(self.mass))):
            return type(self).__l_min(self.mass) * u.L_sun
        return (type(self).__l_min(self.mass) +
                (self._star_system.age.value /
                 type(self).__m_span(self.mass)) *
                (type(self).__l_max(self.mass) -
                 type(self).__l_min(self.mass))) * u.L_sun

    @property
    def temperature(self) -> u.Quantity:
        """read-only effective temperature in K"""
        temp = (type(self).__temp_III(self.mass)
                if self.luminosity_class == type(self).Luminosity.III
                else type(self).__temp_V(self.mass))
        if (self.luminosity_class == type(self).Luminosity.IV):
            return (temp - ((self._star_system.age.value -
                             type(self).__m_span(self.mass)) /
                            type(self).__s_span(self.mass)) *
                    (temp - 4800)) * u.K
        return temp * u.K

    @property
    def radius(self) -> u.Quantity:
        """radius in AU"""
        # TODO: handle white dwarf luminosity class
        return ((155000 * np.sqrt(self.luminosity.value)) /
                self.temperature.value ** 2) * u.au

    @property
    def limits(self) -> model.bounds.QuantityBounds:
        """inner and outer limit in AU"""
        return model.bounds.QuantityBounds(
                max(0.1 * self.mass.value,
                    0.01 * np.sqrt(self.luminosity.value)) * u.au,
                40 * self.mass.value * u.au
               )

    @property
    def forbidden_zone(self) -> model.bounds.QuantityBounds:
        """the forbidden zone limits in AU if any"""
        if (hasattr(self, '_companions') and len(self._companions) > 0):
            return model.bounds.QuantityBounds(
                    self._companions[0].orbit.min_separation / 3,
                    self._companions[0].orbit.min_separation * 3
                   )
        return None

    @property
    def snow_line(self) -> u.Quantity:
        """snow line in AU"""
        return 4.85 * np.sqrt(self.__l_min(self.seed_mass)) * u.au

    @property
    def spectral_type(self):
        """spectral type from mass"""
        d = {2: 'A5', 1.9: 'A6', 1.8: 'A7', 1.7: 'A9', 1.6: 'F0', 1.5: 'F2',
             1.45: 'F3', 1.4: 'F4', 1.35: 'F5', 1.3: 'F6', 1.25: 'F7',
             1.2: 'F8', 1.15: 'F9', 1.10: 'G0', 1.05: 'G1', 1: 'G2',
             .95: 'G4', .9: 'G6', .85: 'G8', .8: 'K0', .75: 'K2', .7: 'K4',
             .65: 'K5', .6: 'K6', .55: 'K8', .5: 'M0', .45: 'M1', .4: 'M2',
             .35: 'M3', .3: 'M4', .25: 'M4', .2: 'M5', .15: 'M6', .1: 'M7'}
        return ('D' if self.luminosity_class == type(self).Luminosity.D
                else d[list(filter(lambda x: x * u.M_sun >= self.mass,
                                   sorted(d.keys())))
                       [0]])

    def populate(self):
        self._worlds = populate_star(self)
        for i in range(len(self._worlds)):
            setattr(type(self), chr(ord('b') + i),
                    property(lambda self, i=i: self._worlds[i]))

    def __init__(self, star_system):
        self._star_system = star_system
        self.randomize()
