# -*- coding: utf-8 -*-

from random import randint

import numpy as np
from scipy.stats import truncnorm, truncexpon


def truncnorm_draw(lower, upper, mu, sigma):
    a, b = (lower - mu) / sigma, (upper - mu) / sigma
    return truncnorm(a, b, mu, sigma).rvs()

def truncexpon_draw(lower, upper, sigma):
    mu = lower
    b = (upper - lower) / sigma
    return truncexpon(b, mu, sigma).rvs()

def roll1d6(modifier=0, continuous=False):
    if continuous:
        return np.random.uniform(1 + modifier, 6 + modifier)
    else:
        return np.random.randint(1, 6) + modifier

def roll2d6(modifier=0, continuous=False):
    if continuous:
        left = 2 + modifier
        right = 12 + modifier
        mode = (left + right) / 2
        return np.random.triangular(left, mode, right)
    else:
        return sum(np.random.randint(1, 6, 2)) + modifier

def roll3d6(modifier=0, continuous=False):
    if continuous:
        lower = 3 + modifier
        upper = 18 + modifier
        mu = ((upper - lower) / 2) + lower
        return truncnorm_draw(lower, upper, mu, sigma=2.958040)
    else:
        return sum(np.random.randint(1, 6, 3)) + modifier
