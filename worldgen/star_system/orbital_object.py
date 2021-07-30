from .. import Model


class OrbitalObject(Model):

    @property
    def average_orbital_radius(self):
        """The average orbital radius to the parent body in AU"""
        return self._average_orbital_radius

    @average_orbital_radius.setter
    def average_orbital_radius(self, value):
        self._set_ranged_property('average_orbital_radius', value)

    @property
    def eccentricity(self):
        """the orbital orbit eccentricity"""
        return self._eccentricity

    @property
    def eccentricity_range(self):
        """value range for eccentricity"""
        return self._eccentricity_range

    @eccentricity.setter
    def eccentricity(self, value):
        self._set_ranged_property('eccentricity', value)

    def __init__(self, parent_body):
        self.parent_body = parent_body
