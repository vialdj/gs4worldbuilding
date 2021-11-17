from .. import model, world
from ..random import roll2d, roll3d, truncnorm_draw
from .star import Star
from .small_gas_giant import SmallGasGiant
from .medium_gas_giant import MediumGasGiant
from .large_gas_giant import LargeGasGiant

from random import uniform, choices

import numpy as np
from astropy import units as u

from worldgen.star_system import gas_giant

def make_fgg_radius(star: Star):
    """generates a float representing an orbital radius given the proper
    gas giant arrangement"""
    if star.gas_giant_arrangement == Star.GasGiantArrangement.CONVENTIONAL:
        # roll of 2d-2 * .05 + 1 multiplied by the snow line radius
        return (roll2d(-2) * .05 + 1) * star.snow_line.value
    elif star.gas_giant_arrangement == Star.GasGiantArrangement.ECCENTRIC:
        # roll of 1d-1 * .125 multiplied by the snow line radius
        return uniform(0, .625) * star.snow_line.value
    elif star.gas_giant_arrangement == Star.GasGiantArrangement.EPISTELLAR:
        # roll of 3d * .1 multiplied by the inner limit radius
        return roll3d() / 10 * star.limits.min.value
    return np.nan
    
def make_radius(limits, previous_radius, outward=False):
    """generates a float representing an orbital radius at a random spacing
    from previous radius"""
    # transform last orbit given 3d roll over Orbital Spacing table
    ratio = truncnorm_draw(1.4, 2, 1.6976, 0.1120457049600742)
    radius = (previous_radius * ratio if outward else previous_radius / ratio)
    if not outward and (previous_radius - radius) < .15:
        # TODO: should not clamp orbit at a distance of exactly .15
        # but rather have it be at least .15
        radius = previous_radius - .15
    if radius >= limits.min.value and radius <= limits.max.value:
        return radius
    return np.nan

def make_radii(star):
    """orbital radii generation procedure"""
    radii = []
    # first gas giant radius
    fgg_radius = np.nan

    # compute inner and outermost limits
    limits = star.limits
    if star.forbidden_zone:
        if (star.forbidden_zone.max > star.limits.max and
            star.forbidden_zone.min > star.limits.min):
            limits = model.bounds.QuantityBounds(
                        star.limits.min,
                        min(star.limits.max, star.forbidden_zone.min)
                     )
        elif (star.forbidden_zone.min < star.limits.min and
              star.forbidden_zone.max < star.limits.max):
            limits = model.bounds.QuantityBounds(
                        max(star.limits.min, star.forbidden_zone.max),
                        star.limits.max
                     )

    # place first radius
    if star.gas_giant_arrangement != star.GasGiantArrangement.NONE:
        # placing first gas giant if applicable
        fgg_radius = make_fgg_radius(star)
        radii.append(fgg_radius)
    else:
        # divided outermost legal distance by roll of 1d * .05 + 1
        radii.append(limits.max.value / (uniform(0.05, 0.3) + 1))
    
    # place radii
    while True:
        # working the orbits inward
        radius = make_radius(limits, radii[-1])
        if np.isnan(radius):
            break
        radii.append(radius)
    radii.sort()
    while True:
        # working the orbits outward
        radius = make_radius(limits, radii[-1], outward=True)
        if np.isnan(radius):
            break
        radii.append(radius)
    
    return radii, (radii.index(fgg_radius) if not np.isnan(fgg_radius) else -1)

def make_gas_giant(star, radius, fbsl=False):
    
    gas_giant_dist = {SmallGasGiant: .5,
                      MediumGasGiant: .481481481,
                      LargeGasGiant: .018518519}

    if radius <= star.snow_line.value or fbsl:
        gas_giant_dist = {SmallGasGiant: .092592593,
                          MediumGasGiant: .648148148,
                          LargeGasGiant: .259259259}
    
    gas_giant_type = choices(list(gas_giant_dist.keys()),
                             weights=list(gas_giant_dist.values()))[0]
    
    return gas_giant_type(star, radius * u.au)

def make_gas_giants(star, radii, fbsl_radius):
    gas_giants = []

    for radius in radii:
        if (radius <= star.snow_line.value):
            if star.gas_giant_arrangement == Star.GasGiantArrangement.ECCENTRIC:
                if uniform(0, 1) <= .25925926:
                    gas_giants.append(make_gas_giant(star, radius, radius == fbsl_radius))
                    radii.remove(radius)
            elif star.gas_giant_arrangement == Star.GasGiantArrangement.EPISTELLAR:
                if uniform(0, 1) <= .09259259:
                    gas_giants.append(make_gas_giant(star, radius, radius == fbsl_radius))
                    radii.remove(radius)
        else:
            if star.gas_giant_arrangement == Star.GasGiantArrangement.CONVENTIONAL:
                if uniform(0, 1) <= .9537037:
                    gas_giants.append(make_gas_giant(star, radius, radius == fbsl_radius))
                    radii.remove(radius)
            elif uniform(0, 1) <= .90740741:
                gas_giants.append(make_gas_giant(star, radius, radius == fbsl_radius))
                radii.remove(radius)

    return gas_giants

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

def make_worlds(star, radii):
    pass

def populate_star(star):
    """the procedure to populate a star's orbits"""
    # TODO place fgg_idx
    radii, fgg_idx = make_radii(star)
    
    # first radius beyond snow line
    fbsl_radius = list(filter(lambda x: x >= star.snow_line.value, radii))[-1]
    
    worlds = []

    print(len(radii))

    # placing first gas_giant
    if fgg_idx > 0:
        worlds.append(make_gas_giant(star, radii[fgg_idx], radii[fgg_idx] == fbsl_radius))
        radii.remove(radii[fgg_idx])
    
    if star.gas_giant_arrangement != Star.GasGiantArrangement.NONE:
        worlds.extend(make_gas_giants(star, radii, fbsl_radius))
    
    """self._worlds = []
    for i in range(0, len(self._orbits)):
        self._worlds.append(make_world(self, self._orbits[i], World.Size.STANDARD))
        setattr(type(self), chr(ord('b') + i),
                property(lambda self, i=i: self._worlds[i]))"""