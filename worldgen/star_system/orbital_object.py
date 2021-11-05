from .. import Model

import numpy as np


class OrbitalObject(Model):
    """the orbital object model"""
    _eccentricity_range = Model.Range(0, 1)

    @property
    def average_orbital_radius(self):
        """The average orbital radius to the parent body in AU"""
        return self._get_ranged_property('average_orbital_radius')

    @average_orbital_radius.setter
    def average_orbital_radius(self, value):
        self._set_ranged_property('average_orbital_radius', value)

    @property
    def eccentricity(self):
        """the orbital orbit eccentricity"""
        return self._get_ranged_property('eccentricity')

    @property
    def minimum_separation(self):
        """the minimum separation in AU"""
        return (1 - self.eccentricity) * self.average_orbital_radius

    @property
    def maximum_separation(self):
        """the maximum separation in AU"""
        return (1 + self.eccentricity) * self.average_orbital_radius

    @property
    def orbital_period(self):
        """the orbital period in earth years"""
        # watch out for unit of mass i.e. planets
        np.sqrt(self.average_orbital_radius ** 3 /
                (self.parent_body.mass + self.mass))

    @property
    def eccentricity_range(self):
        """value range for eccentricity"""
        return self._eccentricity_range

    @eccentricity.setter
    def eccentricity(self, value):
        self._set_ranged_property('eccentricity', value)

    def __init__(self, parent_body):
        self._parent_body = parent_body
