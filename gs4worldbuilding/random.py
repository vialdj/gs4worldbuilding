# -*- coding: utf-8 -*-

import numpy as np
import ctypes
from scipy.stats import truncnorm, truncexpon


class RandomGenerator:
    """Serves random generation through a seeded rng"""
    __instance = None
    __rng = None
    __seed = 0

    def __new__(cls, *args, **kwargs):
        if RandomGenerator.__instance is None:
            RandomGenerator.__instance = super(RandomGenerator, cls).__new__(cls, *args, **kwargs)
        return RandomGenerator.__instance

    @property
    def seed(self):
        """the generator's seed"""
        return self.__seed

    @seed.setter
    def seed(self, value):
        self.__seed = value
        self.__rng = np.random.default_rng(value)

    @property
    def rng(self):
        """the readonly numpy random number generator"""
        return self.__rng

    def randomize_seed(self):
        """Randomize seed with value in 0 INT_MAX range"""
        self.seed = np.random.randint(ctypes.c_uint32(-1).value // 2)

    def _seed_dependent(func):
        def init_seed(*args, **kwargs):
            self = args[0]
            if not self.__rng:
                self.randomize_seed()
            return func(*args, **kwargs)
        return init_seed

    @_seed_dependent
    def truncnorm_draw(self, lower, upper, mu, sigma):
        """returns a continuous value from the corresponding truncated
        normal distribution"""
        a, b = (lower - mu) / sigma, (upper - mu) / sigma
        return truncnorm(a, b, mu, sigma).rvs(random_state=self.__rng)

    @_seed_dependent
    def truncexpon_draw(self, lower, upper, sigma):
        """returns a continuous value from the corresponding truncated
        exponential distribution"""
        mu = lower
        b = (upper - lower) / sigma
        return truncexpon(b, mu, sigma).rvs(random_state=self.__rng)

    @_seed_dependent
    def roll1d6(self, modifier=0, continuous=False):
        """returns a discrete or continuous value mimicking a
        d6 roll probability function"""
        if continuous:
            return self.__rng.uniform(1 + modifier, 6 + modifier)
        return self.__rng.integers(1, 6) + modifier

    @_seed_dependent
    def roll2d6(self, modifier=0, continuous=False):
        """returns a discrete or continuous value mimicking a
        2d6 roll probability function"""
        if continuous:
            left = 2 + modifier
            right = 12 + modifier
            mode = (left + right) / 2
            return self.__rng.triangular(left, mode, right)
        return sum(self.__rng.integers(1, 6, 2)) + modifier

    @_seed_dependent
    def roll3d6(self, modifier=0, continuous=False):
        """returns a discrete or continuous value mimicking a
        3d6 roll probability function"""
        if continuous:
            lower = 3 + modifier
            upper = 18 + modifier
            mu = ((upper - lower) / 2) + lower
            return self.truncnorm_draw(lower, upper, mu, sigma=2.958040)
        return sum(self.__rng.integers(1, 6, 3)) + modifier

    @_seed_dependent
    def choice(self, a, p):
        return a[self.__rng.choice(list(range(0, len(a))), p=p)]
