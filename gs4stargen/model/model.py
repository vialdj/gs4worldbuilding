# -*- coding: utf-8 -*-

from abc import ABC


class Model(ABC):
    """the Model class"""

    def _set_bounded_property(self, prop, value):
        """setter for bounded value properties"""
        bounds = getattr(self, '{}_bounds'.format(prop), None)
        if not bounds:
            raise AttributeError('can\'t set attribute, no {}_bounds found'
                                 .format(prop))
        if value < bounds.min or value > bounds.max:
            raise ValueError('{} value out of range {}'
                             .format(prop, bounds))
        setattr(self, '_{}'.format(prop), bounds.normalize(value))

    def _get_bounded_property(self, prop):
        """getter for bounded value properties"""
        bounds = getattr(self, '{}_bounds'.format(prop), None)
        if not bounds:
            raise AttributeError('can\'t get attribute, no {}_bounds found'
                                 .format(prop))
        value = getattr(self, '_{}'.format(prop))
        return bounds.scale(value)

    @property
    def name(self) -> str:
        return self._name if hasattr(self, '_name') else None

    @name.setter
    def name(self, value: str):
        self._name = value

    def __iter__(self):
        """yield property names and values"""
        for prop in list(filter(lambda x: hasattr(type(self), x)
                         and isinstance(getattr(type(self), x), property),
                         dir(self))):
            yield prop, getattr(self, prop)

    def __str__(self):
        return ('{{class: {}, {}}}'
                .format(self.__class__.__name__,
                        ', '.join(['{}: {!s}'.format(prop, value)
                                  for prop, value in self])))
