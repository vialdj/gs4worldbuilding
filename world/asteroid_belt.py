from . import World


class AsteroidBelt(World):
    _temperature_range = World.Range(140, 500)
    _absorption = .97

    def __init__(self):
        super(AsteroidBelt, self).__init__()
