# -*- coding: utf-8 -*-

import numpy as np
from scipy.stats import truncnorm, truncexpon


def truncnorm_draw(lower, upper, mu, sigma):
    a, b = (lower - mu) / sigma, (upper - mu) / sigma
    return truncnorm(a, b, mu, sigma).rvs()

def truncexpon_draw(lower, upper, sigma):
    mu = lower
    b = (upper - lower) / sigma
    return truncexpon(b, mu, sigma).rvs()

def roll2d(modifier=0):
    left = 2 + modifier
    right = 12 + modifier
    mode = (left + right) / 2
    return np.random.triangular(left, mode, right)

def roll3d(modifier=0):
    lower = 3 + modifier
    upper = 18 + modifier
    mu = ((upper - lower) / 2) + lower

    return truncnorm_draw(lower, upper, mu, sigma=2.958040)
