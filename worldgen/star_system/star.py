# -*- coding: utf-8 -*-

from .. import RandomizableModel

from enum import Enum
from math import sqrt
from random import choices, uniform

import numpy as np
from scipy.stats import truncexpon, truncnorm


class Star(RandomizableModel):
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
        upper, lower = (.6, 1.5) if self._star_system.garden_host else (2, .1)
        mu = lower
        sigma = (.37733756770297866 if self._star_system.garden_host
                 else .376928361893875)
        b = (upper - lower) / sigma

        self.seed_mass = truncexpon(b=b, loc=mu, scale=sigma).rvs()

    def random_gas_giant_arrangement(self):
        """sum of a 3d roll times over Gas Giant Arrangement Table"""
        distribution = [.5, .24074, 0.16666, .0926]
        self.gas_giant_arrangement = choices(list(self.GasGiantArrangement),
                                             weights=distribution,
                                             k=1)[0]

    @staticmethod
    def __l_max(mass):
        """l_max fitted through the form a*x**b"""
        if mass >= .45:
            return 1.417549268949681 * mass ** 3.786542028176919
        return np.nan

    @staticmethod
    def __l_min(mass):
        """l_min fitted through the form a*x**b"""
        return 0.8994825154104518 * mass ** 4.182711149771404

    @staticmethod
    def __m_span(mass):
        """m_span fitted through the form a*exp(b*x)+c"""
        if mass >= .45:
            return 355.25732733 * np.exp(-3.62394465 * mass) - 1.19842708
        return np.nan

    @staticmethod
    def __s_span(mass):
        """s_span fitted through the form a*exp(b*x)"""
        if mass >= .95:
            return 18.445568275396568 * np.exp(-2.471832533773299 * mass)
        return np.nan

    @staticmethod
    def __g_span(mass):
        """g_span fitted through the form a*exp(b*x)"""
        if mass >= .95:
            return 11.045171731219448 * np.exp(-2.4574060414344223 * mass)
        return np.nan

    @staticmethod
    def __temp_V(mass):
        """temp in interval [3100, 8200] linearly through the form a * x + b"""
        return 2684.21052632 * mass + 2831.57894737

    @staticmethod
    def __temp_III(mass):
        """temp in interval [3000, 5000] linearly through the form a * x + b"""
        return 1052.63157589 * mass + 2105.26315789

    @property
    def mass(self):
        """read-only mass in M☉ with applied modifiers"""
        return (.9 + ((self.seed_mass - .1) / 1.9) * .5
                if self.luminosity_class == type(self).Luminosity.D
                else self.seed_mass)

    @property
    def seed_mass(self):
        """mass in M☉ without modifiers"""
        return self._get_ranged_property('seed_mass')

    @property
    def seed_mass_range(self):
        """value range for mass"""
        return (type(self).Range(.6, 1.5)
                if self._star_system.garden_host
                else type(self).Range(.1, 2))

    @seed_mass.setter
    def seed_mass(self, value):
        self._set_ranged_property('seed_mass', value)

    @property
    def gas_giant_arrangement(self):
        """gas giant arrangement category over Gas Giant Arrangement Table"""
        return self._gas_giant_arrangement

    @gas_giant_arrangement.setter
    def gas_giant_arrangement(self, value):
        if not isinstance(value, self.GasGiantArrangement):
            raise ValueError('gas giant arrangement value type must be {}'
                             .format(self.GasGiantArrangement))
        self._gas_giant_arrangement = value

    @property
    def luminosity_class(self):
        """the star luminosity class"""
        m_span = type(self).__m_span(self.seed_mass)
        s_span = type(self).__s_span(self.seed_mass) + m_span
        g_span = type(self).__g_span(self.seed_mass) + s_span
        if (not np.isnan(g_span) and self._star_system.age > g_span):
            return type(self).Luminosity.D
        elif (not np.isnan(s_span) and self._star_system.age > s_span):
            return type(self).Luminosity.III
        elif (not np.isnan(m_span) and self._star_system.age > m_span):
            return type(self).Luminosity.IV
        return type(self).Luminosity.V

    @property
    def luminosity(self):
        """luminosity in L☉"""
        if (self.luminosity_class == type(self).Luminosity.D):
            return .001
        if (self.luminosity_class == type(self).Luminosity.III):
            type(self).__l_max(self.mass) * 25
        if (self.luminosity_class == type(self).Luminosity.IV):
            return type(self).__l_max(self.mass)
        if (np.isnan(type(self).__l_max(self.mass))):
            return type(self).__l_min(self.mass)
        return (type(self).__l_min(self.mass) +
                (self._star_system.age / type(self).__m_span(self.mass)) *
                (type(self).__l_max(self.mass) -
                 type(self).__l_min(self.mass)))

    @property
    def temperature(self):
        """effective temperature in K"""
        temp = (type(self).__temp_III(self.mass)
                if self.luminosity_class == type(self).Luminosity.III
                else type(self).__temp_V(self.mass))
        if (self.luminosity_class == type(self).Luminosity.IV):
            return (temp - ((self._star_system.age -
                             type(self).__m_span(self.mass)) /
                            type(self).__s_span(self.mass)) *
                    (temp - 4800))
        return temp

    @property
    def radius(self):
        """radius in AU"""
        # TODO: handle white dwarf luminosity class
        return (155000 * sqrt(self.luminosity)) / self.temperature ** 2

    @property
    def limits(self):
        """inner and outer limit in AU"""
        return type(self).Range(max(0.1 * self.mass,
                                    0.01 * sqrt(self.luminosity)),
                                40 * self.mass)

    @staticmethod
    def __get_separation(self, companion):
        parent_body = getattr(self, '_parent_body', None)
        if parent_body == companion:
            type(self).Range(getattr(self, 'minimum_separation', None),
                             getattr(self, 'maximum_separation', None))

    @property
    def forbidden_zone(self):
        """the forbidden zone limits in AU if any"""
        separation = type(self).Range(getattr(self, 'minimum_separation', None),
                                      getattr(self, 'maximum_separation', None))
        if separation.min and separation.max:
            return type(self).Range(separation.min / 3, separation.max * 3)
        return None

    @property
    def snow_line(self):
        """snow line in AU"""
        return 4.85 * sqrt(self.luminosity)

    @property
    def spectral_type(self):
        """spectral type from mass"""
        d = {2: 'A5', 1.9: 'A6', 1.8: 'A7', 1.7: 'A9', 1.6: 'F0', 1.5: 'F2',
             1.45: 'F3', 1.4: 'F4', 1.35: 'F5', 1.3: 'F6', 1.25: 'F7',
             1.2: 'F8', 1.15: 'F9', 1.10: 'G0', 1.05: 'G1', 1: 'G2',
             .95: 'G4', .9: 'G6', .85: 'G8', .8: 'K0', .75: 'K2', .7: 'K4',
             .65: 'K5', .6: 'K6', .55: 'K8', .5: 'M0', .45: 'M1', .4: 'M2',
             .35: 'M3', .3: 'M4', .25: 'M4', .2: 'M5', .15: 'M6', .1: 'M7'}
        return (None if self.luminosity_class == type(self).Luminosity.D
                else d[list(filter(lambda x: x >= self.mass, sorted(d.keys())))
                       [0]])

    @property
    def orbits(self):
        """objects orbiting the star"""
        return getattr(self, '_orbits', None)

    def __random_first_gas_giant(self):
        """generating an orbital radius given the proper gas giant
arrangement"""
        if self.gas_giant_arrangement == self.GasGiantArrangement.CONVENTIONAL:
            # roll of 2d-2 * .05 + 1 multiplied by the snow line radius
            return np.random.triangular(1, 1.25, 1.5) * self.snow_line
        elif self.gas_giant_arrangement == self.GasGiantArrangement.ECCENTRIC:
            # roll of 1d-1 * .125 multiplied by the snow line radius
            return uniform(0, .625) * .125 * self.snow_line
        # (EPISTELLAR) roll of 3d * .1 multiplied by the inner limit radius
        return ((truncnorm((3 - 10.5) / 2.958040, (18 - 10.5) / 2.958040,
                           loc=10.5, scale=2.958040).rvs() / 10) *
                self.limits.min)

    def generate_orbits(self):
        """generate the stars planetary orbits"""
        self._orbits = []
        if self.gas_giant_arrangement != self.GasGiantArrangement.NONE:
            # placing first gas giant if applicable
            self._orbits.append(self.__random_first_gas_giant())

    def __init__(self, star_system):
        self._star_system = star_system
        self.randomize()