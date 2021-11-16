# -*- coding: utf-8 -*-

from .. import world

import numpy as np
from astropy import units as u


def make_world(orbit, size: world.World.Size):
    bb_temp = (278 * np.power(orbit._parent_body.luminosity.value, (1 / 4))
               / np.sqrt(orbit.radius.value)) * u.K
    types = {}
    if size == world.World.Size.SMALL:
        types = {0 * u.K: world.SmallHadean,
                 81 * u.K: world.SmallIce,
                 141 * u.K: world.SmallRock}
    elif size == world.World.Size.STANDARD:
        types = {0 * u.K: world.StandardHadean,
                 81 * u.K: world.StandardIce,
                 241 * u.K: world.StandardOcean,
                 321 * u.K: world.StandardGreenhouse,
                 501 * u.K: world.StandardChthonian}
    elif size == world.World.Size.LARGE:
        types = {0 * u.K: world.LargeIce,
                 241 * u.K: world.LargeOcean,
                 321 * u.K: world.LargeGreenhouse,
                 501 * u.K: world.LargeChthonian}

    world_type = None
    if size == world.World.Size.TINY:
        world_type = world.TinyIce if bb_temp <= 140 * u.K else world.TinyRock
    else:
        world_type = list(filter(lambda x: bb_temp >= x[0], types.items()))[-1][1]

    return world_type(orbit)
