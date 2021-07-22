from . import Star

import numpy as np


class EvolutionaryStage(Star):
    """the EvolutionaryStage class to be inherited by concrete Star decorators"""

    @property
    def base(self):
        """the base star"""
        return (self._base if hasattr(self, '_base') else None)

    def __init__(self):
        super(EvolutionaryStage, self).__init__()
        self.Mass.__set__ = None


class Subgiant(EvolutionaryStage):
    """The Subgiant Star decorator"""

    _luminosity_class = Star.Luminosity.IV

    @property
    def luminosity(self):
        """luminosity in L☉"""
        return type(self)._l_max(self.mass)

    @property
    def temperature(self):
        """effective temperature in K"""
        temp = type(self)._temp(self.mass)
        return (temp - ((self.age - type(self)._m_span(self.mass)) /
                type(self)._s_span(self.mass)) * (temp - 4800))

    def __init__(self):
        super(Subgiant, self).__init__()


class Giant(EvolutionaryStage):
    """The Giant Star decorator"""

    _luminosity_class = Star.Luminosity.III

    @staticmethod
    def _temp(mass):
        """temp in interval [3000, 5000] linearly through the form a * x + b)"""
        return 1052.63157589 * mass + 2105.26315789

    @property
    def luminosity(self):
        """luminosity in L☉"""
        return type(self)._l_max(self.mass) * 25

    def __init__(self):
        super(Giant, self).__init__()


class WhiteDwarf(EvolutionaryStage):
    """The White Dwarf Star decorator"""

    _luminosity_class = Star.Luminosity.D

    @property
    def luminosity(self):
        """luminosity in L☉"""
        return np.nan

    def __init__(self):
        super(WhiteDwarf, self).__init__()