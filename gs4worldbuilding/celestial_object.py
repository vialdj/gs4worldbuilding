from abc import ABC, abstractmethod

from astropy.units import Quantity


class CelestialObject(ABC):
    '''The basic celestial object abstract class'''

    @property
    @abstractmethod
    def mass(self) -> Quantity['mass']:
        '''mass property'''
        raise NotImplementedError()
