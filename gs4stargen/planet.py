# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from astropy import units as u


class Planet(ABC):
    """the Planet interfaces"""

    @property
    def size(self):
        """size class variable"""
        return self._size

    @property
    @abstractmethod
    def density(self) -> u.Quantity:
        """density in d⊕"""
        pass

    @property
    @abstractmethod
    def diameter(self) -> u.Quantity:
        """diameter in D⊕"""
        pass

    @property
    @abstractmethod
    def mass(self) -> u.Quantity:
        """mass in M⊕"""
        pass
