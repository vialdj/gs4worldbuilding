from .utils import Range
from . import World

import random


class AsteroidBelt(World):
    _temperature_range = Range(140, 500)
    _absorption = .97
    _ressource_range = Range(World.Ressource.WORTHLESS,
                             World.Ressource.MOTHERLODE)

    @classmethod
    def random_ressource(cls):
        """sum of a 3d roll times over default worlds Ressource Value Table"""
        ressource_distribution = [.00463, .01389, .02778, .11574, .21296, .25,
                                  .21296, .11574, .02778, .01389, .00463]
        return random.choices(list(cls.Ressource),
                              weights=ressource_distribution, k=1)[0]

    def __init__(self):
        super(AsteroidBelt, self).__init__()
