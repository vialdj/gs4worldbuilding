from typing import Optional

import numpy as np
from astropy import units as u

from gs4worldbuilding.random import RandomGenerator
from gs4worldbuilding.asteroid_belt import AsteroidBelt
from gs4worldbuilding.orbit import Orbit
from gs4worldbuilding.gas_giant import (GasGiant, SmallGasGiant,
                                        MediumGasGiant, LargeGasGiant)
from gs4worldbuilding.gas_giant_arrangement import GasGiantArrangement
from gs4worldbuilding.model.bounds import QuantityBounds
from gs4worldbuilding.terrestrial import Size


def make_first_gas_giant_radius(star) -> Optional[u.Quantity]:
    '''generates an orbital radius given the proper gas giant arrangement'''
    if star.gas_giant_arrangement == GasGiantArrangement.CONVENTIONAL:
        # roll of 2d-2 * .05 + 1 multiplied by the snow line radius
        return ((RandomGenerator().roll2d6(-2, continuous=True) * .05 + 1) *
                star.snow_line)
    elif star.gas_giant_arrangement == GasGiantArrangement.ECCENTRIC:
        # roll of 1d-1 * .125 multiplied by the snow line radius
        return (RandomGenerator().roll1d6(-1, continuous=True)
                * .125 * star.snow_line)
    elif star.gas_giant_arrangement == GasGiantArrangement.EPISTELLAR:
        # roll of 3d * .1 multiplied by the inner limit radius
        return (RandomGenerator().roll3d6(continuous=True) / 10 *
                star.limits.upper)


def make_radius(limits: QuantityBounds, previous_radius: u.Quantity,
                outward=False) -> Optional[QuantityBounds]:
    '''generates a float representing an orbital radius at a random spacing
    from previous radius'''
    # transform last orbit given 3d roll over Orbital Spacing table
    ratio = RandomGenerator().truncnorm_draw(1.4, 2, 1.6976,
                                             0.1120457049600742)
    radius = (previous_radius * ratio if outward else previous_radius / ratio)
    if not outward and (previous_radius - radius) < .15 * u.au:
        # TODO: should not clamp orbit at a distance of exactly .15
        # but rather have it be at least .15
        radius = previous_radius - .15 * u.au
    if radius >= limits.lower and radius <= limits.upper:
        return radius


def make_radii(star):
    '''orbital radii generation procedure'''
    radii = []
    # first gas giant radius
    fgg_radius = np.nan

    # compute inner and outermost limits
    limits = star.limits
    if star.forbidden_zone:
        exclusions = limits.exclusions(star.forbidden_zone)
        if exclusions:
            limits = exclusions[0]

    # place first radius
    if star.gas_giant_arrangement != GasGiantArrangement.NONE:
        # placing first gas giant if applicable
        fgg_radius = make_first_gas_giant_radius(star)
        assert fgg_radius
        radii.append(fgg_radius)
    else:
        # divided outermost legal distance by roll of 1d * .05 + 1
        radii.append(limits.upper / (RandomGenerator()
                                     .roll1d6(continuous=True) * .05 + 1))

    # place radii
    while True:
        # working the orbits inward
        radius = make_radius(limits, radii[-1])
        if not radius:
            break
        radii.append(radius)
    radii.sort()
    while True:
        # working the orbits outward
        radius = make_radius(limits, radii[-1], outward=True)
        if not radius:
            break
        radii.append(radius)

    return radii, (radii.index(fgg_radius) if not fgg_radius else -1)


def terrestrial_type(parent, size, radius=np.nan):
    blackbody_temperature = (parent.blackbody_temperature
                             if issubclass(type(parent), planet.Planet)
                             else (278 * np.power(parent.luminosity.value,
                                                  (1 / 4)) / np.sqrt(radius))
                             * u.K)

    parent_star = (parent.orbit._parent_body
                   if issubclass(type(parent), planet.Planet) else parent)

    types = {}
    if size == Size.SMALL:
        types = {0 * u.K: terrestrial.SmallHadean,
                 81 * u.K: terrestrial.SmallIce,
                 141 * u.K: terrestrial.SmallRock}
    elif size == Size.STANDARD:
        garden_roll_modifier = min(parent_star._star_system.age // (.5 * u.Ga),
                                   10)
        types = {0 * u.K: terrestrial.StandardHadean,
                 81 * u.K: (terrestrial.StandardAmmonia
                            if parent_star.mass <= .65 *
                            u.M_sun else terrestrial.StandardIce),
                 241 * u.K: (terrestrial.StandardGarden
                             if RandomGenerator().roll3d6(garden_roll_modifier) >= 18
                             else terrestrial.StandardOcean),
                 321 * u.K: terrestrial.StandardGreenhouse,
                 501 * u.K: terrestrial.StandardChthonian}
    elif size == Size.LARGE:
        garden_roll_modifier = min(parent_star._star_system.age // .5 * u.Ga, 5)
        types = {0 * u.K: (terrestrial.LargeAmmonia
                           if parent_star.mass <= .65 * u.M_sun
                           else terrestrial.LargeIce),
                 241 * u.K: (terrestrial.LargeGarden
                             if RandomGenerator().roll3d6(garden_roll_modifier) >= 18
                             else terrestrial.LargeOcean),
                 321 * u.K: terrestrial.LargeGreenhouse,
                 501 * u.K: terrestrial.LargeChthonian}

    world_type = None
    if size == Size.TINY:
        # TODO: tiny sulfur is almost always the innermost moon, not respected here
        world_type = ((terrestrial.TinySulfur if
                      issubclass(type(parent), GasGiant) and
                      not hasattr(parent, '_moons') and
                      RandomGenerator().roll1d6() < 4 else terrestrial.TinyIce)
                      if blackbody_temperature <= 140 * u.K
                      else terrestrial.TinyRock)
    else:
        world_type = (list(filter(lambda x: blackbody_temperature >= x[0],
                                  types.items()))[-1][1])

    return world_type


def make_moon(parent):
    sizes = sorted(list(Size))
    parent_size = sizes.index(Size.LARGE
                              if issubclass(type(parent), GasGiant)
                              else parent.size)

    size_roll = RandomGenerator().roll3d6()
    scale = -3 if size_roll < 12 else (-2 if size_roll < 15 else -1)
    moon_size = max(parent_size + scale, 0)

    if issubclass(type(parent), terrestrial.Terrestrial):
        # orbital radius for major moons of terrestrial planets
        diff = parent_size - moon_size
        modifier = 2 if diff == 2 else (4 if diff == 1 else 0)
        radius = RandomGenerator().roll2d6(modifier, continuous=True) * 2.5 * parent.diameter.to(u.au).value
        # TODO: ensure that major moons are not in 5 planetary diameter of each other
    else:
        radius_roll = RandomGenerator().roll3d6(3, continuous=True)
        radius_roll += RandomGenerator().roll2d6() if radius_roll >= 15 else 0
        radius = radius_roll / 2 * parent.diameter.to(u.au).value
        # TODO: ensure that major moons are not in 1 planetary diameter of each other
    moon_type = terrestrial_type(parent, sizes[moon_size], radius)
    moon = moon_type(orbit=Orbit(parent, radius * u.au))
    return moon


def make_gas_giant_moons(parent):
    # roll for moonlets:
    moons = []
    modifiers = {.1 * u.au: -10, .5 * u.au: -8, .75 * u.au: -6,
                 1.5 * u.au: -3}
    filtered = list(filter(lambda x: parent.orbit.radius <= x[0],
                           modifiers.items()))
    modifier = filtered[0][1] if len(filtered) > 0 else 0
    parent._n_moonlets = max(RandomGenerator().roll2d6(modifier), 0)
    parent._n_captured = 0
    # roll for moons
    if parent.orbit.radius > .1 * u.au:
        modifiers = {.5 * u.au: -5, .75 * u.au: -4, 1.5 * u.au: -1}
        filtered = list(filter(lambda x: parent.orbit.radius <= x[0],
                               modifiers.items()))
        modifier = filtered[0][1] if len(filtered) > 0 else 0
        n_moons = max(RandomGenerator().roll1d6(modifier), 0)
        for _ in range(n_moons):
            moons.append(make_moon(parent))
    # roll for captured moonlets
    if parent.orbit.radius > .5 * u.au:
        modifiers = {.75 * u.au: -5, 1.5 * u.au: -4, 3 * u.au: -1}
        filtered = list(filter(lambda x: parent.orbit.radius <= x[0],
                               modifiers.items()))
        modifier = filtered[0][1] if len(filtered) > 0 else 0
        parent._n_captured = max(RandomGenerator().roll1d6(modifier), 0)

    moons.sort(key=lambda m: m.orbit.radius)
    return moons


def make_gas_giant(star, radius, fbsl=False):
    gas_giant_types = {11: SmallGasGiant,
                       17: MediumGasGiant}
    size_roll = RandomGenerator().roll3d6(4 if radius <= star.snow_line.value or fbsl else 0)
    filtered = list(filter(lambda x: size_roll < x[0],
                           list(gas_giant_types.items())))
    gas_giant_type = filtered[0][1] if len(filtered) > 0 else LargeGasGiant
    gas_giant = gas_giant_type(star, radius * u.au)
    gas_giant._moons = make_gas_giant_moons(gas_giant)

    return gas_giant


def make_gas_giants(star, radii, fbsl_radius):
    gas_giants = []

    for radius in radii:
        if (radius <= star.snow_line.value):
            if star.gas_giant_arrangement == GasGiantArrangement.ECCENTRIC:
                if RandomGenerator().roll3d6() <= 8:
                    gas_giants.append(make_gas_giant(star, radius,
                                                     radius == fbsl_radius))
                    radii.remove(radius)
            elif star.gas_giant_arrangement == GasGiantArrangement.EPISTELLAR:
                if RandomGenerator().roll3d6() <= 6:
                    gas_giants.append(make_gas_giant(star, radius,
                                                     radius == fbsl_radius))
                    radii.remove(radius)
        else:
            if star.gas_giant_arrangement == GasGiantArrangement.CONVENTIONAL:
                if RandomGenerator().roll3d6() <= 15:
                    gas_giants.append(make_gas_giant(star, radius,
                                                     radius == fbsl_radius))
                    radii.remove(radius)
            elif RandomGenerator().roll3d6() <= 14:
                gas_giants.append(make_gas_giant(star, radius,
                                                 radius == fbsl_radius))
                radii.remove(radius)

    return gas_giants


def make_terrestrial_moons(parent):
    moons = []
    parent._n_moonlets = 0
    if parent.orbit.radius > .5 * u.au:
        modifier = (-3 if parent.orbit.radius <= .75 * u.au
                    else (-1 if parent.orbit.radius <= 1.5 * u.au else 0))
        size_modifiers = {Size.TINY: -2,
                          Size.SMALL: -1,
                          Size.STANDARD: 0,
                          Size.LARGE: 1}
        modifier += size_modifiers[parent.size]
        n_moons = max(RandomGenerator().roll1d6(-4 + modifier), 0)
        for _ in range(n_moons):
            moons.append(make_moon(parent))
        parent._n_moonlets = (max(RandomGenerator().roll1d6(-2 + modifier), 0)
                              if len(moons) == 0 else 0)

    moons.sort(key=lambda m: m.orbit.radius)
    return moons


def make_terrestrial(star, radius, size: Size):
    world_type = terrestrial_type(star, size, radius)
    terrestrial = world_type(orbit=Orbit(star, radius * u.au))
    terrestrial._moons = make_terrestrial_moons(terrestrial)

    return terrestrial


def make_worlds(star, worlds, radii):

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
               9: lambda x: make_terrestrial(star, x, Size.TINY),
               12: lambda x: make_terrestrial(star, x, Size.SMALL),
               16: lambda x: make_terrestrial(star, x, Size.STANDARD)}

    for i in range(1, len(orbits)):
        if not orbits[i][1]:
            if (orbits[i - 1][1] == 'LIMIT' or
                (i + 1 < len(orbits) and orbits[i + 1][1] == 'LIMIT')):
                orbits[i][2] -= 3
            if (orbits[i - 1][1] == 'FORBIDDEN_ZONE' or (i + 1 < len(orbits) and orbits[i + 1][1] == 'FORBIDDEN_ZONE')):
                orbits[i][2] -= 6
            if orbits[i - 1][1] == 'GAS_GIANT':
                orbits[i][2] -= 3
            if i + 1 < len(orbits) and orbits[i + 1][1] == 'GAS_GIANT':
                orbits[i][2] -= 6

            roll = RandomGenerator().roll3d6(orbits[i][2])
            filtered = list(filter(lambda x: roll < x[0], list(methods.items())))
            method = filtered[0][1] if len(filtered) > 0 else lambda x: make_terrestrial(star, x, Size.LARGE)
            w = method(orbits[i][0])
            if w:
                worlds.append(w)

    return worlds


def populate_star(star):
    '''the procedure to populate a star's orbits'''

    radii, fgg_idx = make_radii(star)

    # first radius beyond snow line
    bsl_radii = list(filter(lambda x: x >= star.snow_line.value, radii))
    fbsl_radius = bsl_radii[-1] if len(bsl_radii) > 0 else -1

    worlds = []

    # placing first gas_giant
    if fgg_idx > 0:
        worlds.append(make_gas_giant(star, radii[fgg_idx],
                                     radii[fgg_idx] == fbsl_radius))
        radii.remove(radii[fgg_idx])

    if star.gas_giant_arrangement != GasGiantArrangement.NONE:
        worlds.extend(make_gas_giants(star, radii, fbsl_radius))

    make_worlds(star, worlds, radii)

    worlds.sort(key=lambda w: w.orbit.radius)

    return worlds
