from . import model, terrestrial
from .random import roll1d6, roll2d6, roll3d6, truncnorm_draw
from .asteroid_belt import AsteroidBelt
from .orbit import Orbit
from .gas_giant import GasGiant, SmallGasGiant, MediumGasGiant, LargeGasGiant

from collections import namedtuple

import numpy as np
from astropy import units as u


def make_first_gas_giant_radius(star):
    """generates a float representing an orbital radius given the proper
    gas giant arrangement"""
    if star.gas_giant_arrangement == type(star).GasGiantArrangement.CONVENTIONAL:
        # roll of 2d-2 * .05 + 1 multiplied by the snow line radius
        return (roll2d6(-2, continuous=True) * .05 + 1) * star.snow_line.value
    elif star.gas_giant_arrangement == type(star).GasGiantArrangement.ECCENTRIC:
        # roll of 1d-1 * .125 multiplied by the snow line radius
        return roll1d6(-1, continuous=True) * .125 * star.snow_line.value
    elif star.gas_giant_arrangement == type(star).GasGiantArrangement.EPISTELLAR:
        # roll of 3d * .1 multiplied by the inner limit radius
        return roll3d6(continuous=True) / 10 * star.limits.min.value
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
    if star.gas_giant_arrangement != type(star).GasGiantArrangement.NONE:
        # placing first gas giant if applicable
        fgg_radius = make_first_gas_giant_radius(star)
        radii.append(fgg_radius)
    else:
        # divided outermost legal distance by roll of 1d * .05 + 1
        radii.append(limits.max.value / (roll1d6(continuous=True) * .05 + 1))

    
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


def terrestrial_type(parent, size, radius=np.nan):
    blackbody_temperature = parent.blackbody_temperature if issubclass(type(parent), terrestrial.Terrestrial) else (278 * np.power(parent.luminosity.value, (1 / 4)) / np.sqrt(radius)) * u.K

    parent_star = parent.orbit._parent_body if issubclass(type(parent), terrestrial.Terrestrial) else parent

    types = {}
    if size == terrestrial.Terrestrial.Size.SMALL:
        types = {0 * u.K: terrestrial.SmallHadean,
                 81 * u.K: terrestrial.SmallIce,
                 141 * u.K: terrestrial.SmallRock}
    elif size == terrestrial.Terrestrial.Size.STANDARD:
        garden_roll_modifier = min(parent_star._star_system.age // (.5 * u.Ga), 10)
        types = {0 * u.K: terrestrial.StandardHadean,
                 81 * u.K: terrestrial.StandardAmmonia if parent_star.mass <= .65 * u.M_sun else terrestrial.StandardIce,
                 241 * u.K: terrestrial.StandardGarden if roll3d6(garden_roll_modifier) >= 18 else terrestrial.StandardOcean,
                 321 * u.K: terrestrial.StandardGreenhouse,
                 501 * u.K: terrestrial.StandardChthonian}
    elif size == terrestrial.Terrestrial.Size.LARGE:
        garden_roll_modifier = min(parent_star._star_system.age // .5 * u.Ga, 5)
        types = {0 * u.K: terrestrial.LargeAmmonia if parent_star.mass <= .65 * u.M_sun else terrestrial.LargeIce,
                 241 * u.K: terrestrial.LargeGarden if roll3d6(garden_roll_modifier) >= 18 else terrestrial.LargeOcean,
                 321 * u.K: terrestrial.LargeGreenhouse,
                 501 * u.K: terrestrial.LargeChthonian}

    world_type = None
    if size == terrestrial.Terrestrial.Size.TINY:
        # TODO: add tiny sulfur type
        world_type = terrestrial.TinyIce if blackbody_temperature <= 140 * u.K else terrestrial.TinyRock
    else:
        world_type = list(filter(lambda x: blackbody_temperature >= x[0], types.items()))[-1][1]

    return world_type


def make_moon(parent):
    sizes = sorted(list(terrestrial.Terrestrial.Size))
    parent_size = terrestrial.Terrestrial.Size.LARGE if issubclass(type(parent), GasGiant) else parent.size

    roll = roll3d6()
    scale = -3 if roll < 12 else (-2 if roll < 15 else -1)
    size = sizes[max(sizes.index(parent_size) - scale, 0)]

    # orbital radius for major moons of terrestrial planets
    diff = sizes.index(parent_size) - sizes.index(size)
    modifier = 2 if diff == 2 else (4 if diff == 1 else 0)
    radius = roll2d6(modifier, continuous=True) * 2.5 * parent.diameter
    # TODO: ensure that major moons are not in 5 planetary diameter of each other

    print(terrestrial_type(parent.blackbody_temperature, size))


def make_gas_giant_moons(w):
    # roll for moonlets:
    orbit_modifiers = {.1 * u.au: -10,
                       .5 * u.au: -8,
                       .75 * u.au: -6,
                       1.5 * u.au: -3}
    filtered = list(filter(lambda x: w.orbit.radius <= x[0], orbit_modifiers.items()))
    modifier = filtered[0][1] if len(filtered) > 0 else 0
    w._n_moonlets = max(roll2d6(modifier), 0)
    # roll for moons
    if w.orbit.radius > .1 * u.au:
        orbit_modifiers = {.5 * u.au: -5,
                           .75 * u.au: -4,
                           1.5 * u.au: -1}
        filtered = list(filter(lambda x: w.orbit.radius <= x[0], orbit_modifiers.items()))
        modifier = filtered[0][1] if len(filtered) > 0 else 0
        w._n_moons = max(roll1d6(modifier), 0)
    # roll for captured moonlets
    if w.orbit.radius > .5 * u.au:
        orbit_modifiers = {.75 * u.au: -5,
                           1.5 * u.au: -4,
                           3 * u.au: -1}
        filtered = list(filter(lambda x: w.orbit.radius <= x[0], orbit_modifiers.items()))
        modifier = filtered[0][1] if len(filtered) > 0 else 0
        w._n_captured = max(roll1d6(modifier), 0)


def make_gas_giant(star, radius, fbsl=False):
    gas_giant_types = {11: SmallGasGiant,
                       17: MediumGasGiant}
    roll = roll3d6(+4) if radius <= star.snow_line.value or fbsl else roll3d6()
    filtered = list(filter(lambda x: roll < x[0], list(gas_giant_types.items())))
    gas_giant_type = filtered[0][1] if len(filtered) > 0 else LargeGasGiant
    world = gas_giant_type(star, radius * u.au)
    make_gas_giant_moons(world)

    return world

def make_gas_giants(star, radii, fbsl_radius):
    gas_giants = []

    for radius in radii:
        if (radius <= star.snow_line.value):
            if star.gas_giant_arrangement == type(star).GasGiantArrangement.ECCENTRIC:
                if roll3d6() <= 8:
                    gas_giants.append(make_gas_giant(star, radius, radius == fbsl_radius))
                    radii.remove(radius)
            elif star.gas_giant_arrangement == type(star).GasGiantArrangement.EPISTELLAR:
                if roll3d6() <= 6:
                    gas_giants.append(make_gas_giant(star, radius, radius == fbsl_radius))
                    radii.remove(radius)
        else:
            if star.gas_giant_arrangement == type(star).GasGiantArrangement.CONVENTIONAL:
                if roll3d6() <= 15:
                    gas_giants.append(make_gas_giant(star, radius, radius == fbsl_radius))
                    radii.remove(radius)
            elif roll3d6() <= 14:
                gas_giants.append(make_gas_giant(star, radius, radius == fbsl_radius))
                radii.remove(radius)

    return gas_giants

def make_terrestrial_moons(w):
    if not issubclass(type(w), AsteroidBelt):
        if w.orbit.radius >.5 * u.au:
            modifier = -3 if w.orbit.radius <= .75 * u.au else (-1 if w.orbit.radius <= 1.5 * u.au else 0)
            size_modifiers = {terrestrial.Terrestrial.Size.TINY: -2,
                              terrestrial.Terrestrial.Size.SMALL: -1,
                              terrestrial.Terrestrial.Size.STANDARD: 0,
                              terrestrial.Terrestrial.Size.LARGE: 1}
            modifier += size_modifiers[w.size]
            w._n_moons = max(roll1d6(-4 + modifier), 0)
            w._n_moonlets = max(roll1d6(-2 + modifier), 0) if w._n_moons == 0 else 0


def make_terrestrial(star, radius, size: terrestrial.Terrestrial.Size):
    world_type = terrestrial_type(star, size, radius)
    world = world_type(orbit=Orbit(star, radius * u.au))
    make_terrestrial_moons(world)
    return world


def make_terrestrials(star, worlds, radii):

    # TODO: implement modifiers

    orbits = []
    orbits.extend([[limit.value, 'LIMIT', 0] for limit in star.limits])
    if star.forbidden_zone:
        orbits.extend([[limit.value, 'FORBIDDEN_ZONE', 0] for limit in star.forbidden_zone])

    for w in worlds:
        orbits.append([w.orbit.radius.value, 'GAS_GIANT', 0])

    orbits.extend([[radius, None, 0] for radius in radii])
    orbits.sort(key=lambda o: o[0])

    methods = {4: lambda _: None,
               7: lambda x: AsteroidBelt(orbit=Orbit(star, x * u.au)),
               9: lambda x: make_terrestrial(star, x, terrestrial.Terrestrial.Size.TINY),
               12: lambda x: make_terrestrial(star, x, terrestrial.Terrestrial.Size.SMALL),
               16: lambda x: make_terrestrial(star, x, terrestrial.Terrestrial.Size.STANDARD)}

    for i in range(1, len(orbits)):
        if not orbits[i][1]:
            if orbits[i - 1][1] == 'LIMIT' or (i + 1 < len(orbits) and orbits[i + 1][1] == 'LIMIT'):
                orbits[i][2] -= 3
            if orbits[i - 1][1] == 'FORBIDDEN_ZONE' or (i + 1 < len(orbits) and orbits[i + 1][1] == 'FORBIDDEN_ZONE'):
                orbits[i][2] -= 6
            if orbits[i - 1][1] == 'GAS_GIANT':
                orbits[i][2] -= 3
            if i + 1 < len(orbits) and orbits[i + 1][1] == 'GAS_GIANT':
                orbits[i][2] -= 6

            roll = roll3d6(orbits[i][2])
            filtered = list(filter(lambda x: roll < x[0], list(methods.items())))
            method = filtered[0][1] if len(filtered) > 0 else lambda x: make_terrestrial(star, x, terrestrial.Terrestrial.Size.LARGE)
            w = method(orbits[i][0])
            if w:
                worlds.append(w)

    return worlds


def populate_star(star):
    """the procedure to populate a star's orbits"""

    radii, fgg_idx = make_radii(star)

    # first radius beyond snow line
    l = list(filter(lambda x: x >= star.snow_line.value, radii))
    fbsl_radius = l[-1] if len(l) > 0 else -1

    worlds = []

    # placing first gas_giant
    if fgg_idx > 0:
        worlds.append(make_gas_giant(star, radii[fgg_idx], radii[fgg_idx] == fbsl_radius))
        radii.remove(radii[fgg_idx])

    if star.gas_giant_arrangement != type(star).GasGiantArrangement.NONE:
        worlds.extend(make_gas_giants(star, radii, fbsl_radius))

    make_terrestrials(star, worlds, radii)

    worlds.sort(key=lambda w: w.orbit.radius)

    return worlds
