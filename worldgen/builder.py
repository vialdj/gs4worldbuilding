import worldgen as w
from worldgen.star import Star

from random import choices


class Builder():
    # World generator
    def __init__(self):
        world_types_distribution = {w.TinySulfur: 0.0457488,
                                    w.TinyIce: 0.16274024,
                                    w.TinyRock: 0.11266216,
                                    w.SmallHadean: 0.00312988,
                                    w.SmallIce: 0.00938964,
                                    w.SmallRock: 0.05007808,
                                    w.StandardChthonian: 0.00300024,
                                    w.StandardGreenhouse: 0.01200096,
                                    w.StandardAmmonia: 0.05924988,
                                    w.StandardHadean: 0.01877928,
                                    w.StandardIce: 0.0312988,
                                    w.StandardOcean: 0.11266216,
                                    w.StandardGarden: 0.15899976,
                                    w.LargeChthonian: 0.00300024,
                                    w.LargeGreenhouse: 0.01200096,
                                    w.LargeAmmonia: 0.02699892,
                                    w.LargeIce: 0.00312988,
                                    w.LargeGarden: 0.00300024,
                                    w.LargeOcean: 0.00938964,
                                    w.AsteroidBelt: 0.16274024}

        world_type = choices(list(world_types_distribution.keys()),
                             weights=list(world_types_distribution.values()))[0]
        self.world = w.StandardGarden()

    def __str__(self):
        return str(self.world)
