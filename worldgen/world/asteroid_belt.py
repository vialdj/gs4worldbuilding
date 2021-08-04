from . import World

from random import choices


class AsteroidBelt(World):
    _temperature_range = World.Range(140, 500)
    _absorption = .97
    _ressource_range = World.Range(World.Ressource.WORTHLESS,
                                   World.Ressource.MOTHERLODE)

    def random_ressource(self):
        """sum of a 3d roll times over default worlds Ressource Value Table"""
        ressource_dist = [.00463, .01389, .02778, .11574, .21296, .25,
                          .21296, .11574, .02778, .01389, .00463]
        self.ressource = choices(list(self.Ressource),
                                 weights=ressource_dist, k=1)[0]

    def __init__(self):
        super(AsteroidBelt, self).__init__()
