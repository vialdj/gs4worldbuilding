from typing import List, Union, Optional, TypeVar
from abc import ABC
from ctypes import c_uint32
from functools import wraps

import numpy as np
from numpy.random import Generator
from scipy.stats import truncnorm, truncexpon


def require_init(func):
    '''init requirement decorator'''
    @wraps(func)
    def lazy_init(self, *args, **kwargs):
        if not isinstance(self, RandomGenerator):
            TypeError('require_init decorator is to be used only '
                      + 'in RandomGenerator definition')
        # accessing a protected member of a client class is a bad practice
        if not getattr(self, '_rng'):
            self.randomize_seed()
        return func(self, *args, **kwargs)
    return lazy_init


T = TypeVar("T")


class RandomGenerator(ABC):
    '''singleton to serves random generation through a seeded rng'''
    _rng: Optional[Generator] = None
    __seed: Optional[int] = None
    __instance: Optional['RandomGenerator'] = None

    @property
    @require_init
    def rng(self) -> Generator:
        '''the wrapped numpy random number generator'''
        assert self._rng
        return self._rng

    def randomize_seed(self) -> None:
        '''Randomize seed with value in 0 INT_MAX range'''
        self.seed = np.random.randint(c_uint32(-1).value // 2)

    @property
    @require_init
    def seed(self) -> int:
        '''the generator's seed'''
        assert self.__seed
        return self.__seed

    @seed.setter
    def seed(self, value: int) -> None:
        self.__seed = value
        self._rng = np.random.default_rng(value)

    def truncnorm_draw(self, lower, upper, mu, sigma) -> float:
        '''returns a continuous value from the corresponding truncated
        normal distribution'''
        a, b = (lower - mu) / sigma, (upper - mu) / sigma
        return truncnorm.rvs(a, b, loc=mu, scale=sigma, random_state=self.rng)

    def truncexpon_draw(self, lower, upper, sigma) -> float:
        '''returns a continuous value from the corresponding truncated
        exponential distribution'''
        b = (upper - lower) / sigma
        return truncexpon.rvs(b=b, loc=lower, scale=sigma,
                              random_state=self.rng)

    def roll1d6(self, modifier=0, continuous=False) -> Union[int, float]:
        '''returns a discrete or continuous value mimicking a
        d6 roll probability function'''
        if continuous:
            return self.rng.uniform(1 + modifier, 6 + modifier)
        return self.rng.integers(1, 6) + modifier

    def roll2d6(self, modifier=0, continuous=False) -> Union[int, float]:
        '''returns a discrete or continuous value mimicking a
        2d6 roll probability function'''
        if continuous:
            left = 2 + modifier
            right = 12 + modifier
            mode = (left + right) / 2
            return self.rng.triangular(left, mode, right)
        return sum(self.rng.integers(1, 6, 2)) + modifier

    def roll3d6(self, modifier=0, continuous=False) -> Union[int, float]:
        '''returns a discrete or continuous value mimicking a
        3d6 roll probability function'''
        if continuous:
            lower = 3 + modifier
            upper = 18 + modifier
            mu = ((upper - lower) / 2) + lower
            return self.truncnorm_draw(lower, upper, mu, sigma=2.958040)
        return sum(self.rng.integers(1, 6, 3)) + modifier

    def choice(self, values: List[T],
               weights: Optional[List[float]] = None) -> T:
        '''pick a random value in a list based on weight'''
        return values[self.rng.choice(list(range(0, len(values))), p=weights)]

    def __new__(cls, *args, **kwargs) -> 'RandomGenerator':
        if RandomGenerator.__instance is None:
            RandomGenerator.__instance = super().__new__(cls, *args, **kwargs)
        return RandomGenerator.__instance
