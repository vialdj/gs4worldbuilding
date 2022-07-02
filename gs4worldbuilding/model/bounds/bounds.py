from typing import Optional, Protocol, TypeVar, List, Generic
from abc import ABC, abstractmethod


class Comparable(Protocol):
    '''comparable protocol that supports lt'''
    @abstractmethod
    def __lt__(self: 'CT', other: 'CT') -> bool:
        '''less than operator'''


CT = TypeVar('CT', bound=Comparable)


class Bounds(Generic[CT], ABC):
    '''The Bounds Abstract class'''
    def __init__(self, lower: CT, upper: CT):
        if upper < lower:
            raise ValueError('inconsistent bounds')
        self.lower = lower
        self.upper = upper

    def __iter__(self):
        '''return boundaries'''
        return iter([self.lower, self.upper])

    def __eq__(self, other):
        return (isinstance(other, type(self)) and
                self.lower == other.lower and
                self.upper == other.upper)

    def intersection(self, other: 'Bounds') -> Optional['Bounds']:
        '''returns the intersection of two sets of bounds if any'''
        if not isinstance(other, type(self)):
            raise ValueError('can only retrieve intersection from' +
                             'bounds of the same type')
        if ((self.lower >= other.lower and other.upper >= self.lower) or
                (self.upper >= other.lower and other.upper >= self.upper)):
            return type(self)(max(self.lower, other.lower),
                              min(self.upper, other.upper))

    def exclusions(self, other: 'Bounds') -> List['Bounds[CT]']:
        '''returns exclusions of the two sets of bounds if any'''
        if not isinstance(other, type(self)):
            raise ValueError('can only retrieve exclusions from' +
                             'bounds of the same type')
        intersection = self.intersection(other)
        if not intersection:
            return [self]
        exclusions = []
        if self.lower < intersection.lower:
            exclusions.append(type(self)(self.lower,
                                         intersection.lower))
        if intersection.upper < self.upper:
            exclusions.append(type(self)(intersection.upper,
                                         self.upper))
        return exclusions

    @abstractmethod
    def normalize(self, value):
        '''Normalize value'''
        raise NotImplementedError()

    @abstractmethod
    def scale(self, value):
        '''Scale value in range'''
        return NotImplementedError()
