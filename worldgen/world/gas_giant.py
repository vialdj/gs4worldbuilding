# -*- coding: utf-8 -*-

from worldgen.model import ValueBounds
from . import World
from .. import QuantityBounds

from random import choices

from astropy import units as u


class GasGiant(World):
    # TODO: this is not a correct model ! It's a placeholder
    _temperature_bounds = QuantityBounds(140 * u.K, 500 * u.K)
    _absorption = .97
    _ressource_bounds = ValueBounds(World.Resource.WORTHLESS,
                                    World.Resource.MOTHERLODE)

    def random_ressource(self):
        """sum of a 3d roll times over default worlds Ressource Value Table"""
        ressource_dist = [.00463, .01389, .02778, .11574, .21296, .25,
                          .21296, .11574, .02778, .01389, .00463]
        self.resource = choices(list(self.Resource),
                                 weights=ressource_dist, k=1)[0]

    def __init__(self):
        super(GasGiant, self).__init__()