from typing import Optional
from abc import ABC


class Model(ABC):
    '''the Model class'''
    _name: Optional[str] = None

    def _set_bounded_property(self, prop, value):
        '''setter for bounded value properties'''
        bounds = getattr(self, f'{prop}_bounds', None)
        if not bounds:
            raise AttributeError("can't set attribute, no " +
                                 f'{prop}_bounds found')
        if value < bounds.lower or value > bounds.upper:
            raise ValueError(f'{prop} value {value} out of range {bounds}')
        setattr(self, f'_{prop}', bounds.normalize(value))

    def _get_bounded_property(self, prop):
        '''getter for bounded value properties'''
        bounds = getattr(self, f'{prop}_bounds', None)
        if not bounds:
            raise AttributeError("can't get attribute, no " +
                                 f'{prop}_bounds found')
        value = getattr(self, f'_{prop}')
        return bounds.scale(value)

    @property
    def name(self) -> Optional[str]:
        '''The model instance name'''
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value
