from .. import model
from ..random import roll2d, roll3d, truncnorm_draw
from .orbit import Orbit

from random import uniform

import numpy as np
from astropy import units as u

def make_gas_giant_orbit(star):
    """generating an orbital radius given the proper gas giant
    arrangement"""
    if star.gas_giant_arrangement == star.GasGiantArrangement.CONVENTIONAL:
        # roll of 2d-2 * .05 + 1 multiplied by the snow line radius
        return Orbit(star, roll2d(-2) * .05 * star.snow_line)
    elif star.gas_giant_arrangement == star.GasGiantArrangement.ECCENTRIC:
        # roll of 1d-1 * .125 multiplied by the snow line radius
        return Orbit(star, uniform(0, .625) * star.snow_line)
    elif star.gas_giant_arrangement == star.GasGiantArrangement.EPISTELLAR:
        # roll of 3d * .1 multiplied by the inner limit radius
        return Orbit(roll3d() / 10 * star.limits.min)
    return np.nan
    
def make_orbit(star, limits, previous_radius, outward=False):
    """generating an orbital radius at a random spacing from previous"""
    # transform last orbit given 3d roll over Orbital Spacing table
    ratio = truncnorm_draw(1.4, 2, 1.6976, 0.1120457049600742)
    radius = (previous_radius * ratio if outward else previous_radius / ratio)
    if not outward and (previous_radius - radius) < .15 * u.au:
        # TODO: should not clamp orbit at a distance of exactly .15
        # but rather have it be at least .15
        radius = previous_radius - .15 * u.au
    if radius >= limits.min and radius <= limits.max:
        return Orbit(star, radius)
    return None


def make_orbits(star):
    """orbits generation procedure"""
    orbits = []

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

    if star.gas_giant_arrangement != star.GasGiantArrangement.NONE:
        # placing first gas giant if applicable
        orbits.append(make_gas_giant_orbit(star))
    else:
        # divided outermost legal distance by roll of 1d * .05 + 1
        orbits.append(limits.max / (uniform(0.05, 0.3) + 1))
    while True:
        # working the orbits inward
        orbit = make_orbit(star, limits, orbits[-1])
        if orbit is np.nan:
            break
        orbits.append(orbit)
    orbits.sort()
    while True:
        # working the orbits outward
        orbit = make_orbit(star, limits, orbits[-1], outward=True)
        if orbit is None:
            break
        orbits.append(orbit)


def populate_star(star):
    """the procedure to populate a star's orbits"""
    orbits = make_orbits(star)
        """self._worlds = []
        for i in range(0, len(self._orbits)):
            self._worlds.append(make_world(self, self._orbits[i], World.Size.STANDARD))
            setattr(type(self), chr(ord('b') + i),
                    property(lambda self, i=i: self._worlds[i]))"""