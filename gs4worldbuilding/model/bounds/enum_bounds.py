from typing import TypeVar, cast
from ordered_enum import OrderedEnum, ValueOrderedEnum

from gs4worldbuilding.model.bounds import Bounds

ET = TypeVar('ET', OrderedEnum, ValueOrderedEnum)


class EnumBounds(Bounds[ET]):
    '''Bounds for enum values'''
    lower: ET
    upper: ET

    def normalize(self, value: ET):
        '''Normalize value'''
        return value.value

    def scale(self, value):
        '''Scale value in range'''
        return cast(ET, value)

    def __str__(self):
        return f'[{self.lower.name}, {self.upper.name}]'

    def __init__(self, lower: ET, upper: ET):
        super().__init__(lower, upper)
