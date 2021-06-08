import random

from worldgen.world import (TinySulfur, TinyIce, TinyRock, SmallHadean,
                            SmallIce, SmallRock, StandardChthonian,
                            StandardGreenhouse, StandardAmmonia,
                            StandardHadean, StandardIce, StandardOcean,
                            StandardGarden, LargeChthonian, LargeGreenhouse,
                            LargeAmmonia, LargeIce, LargeOcean, LargeGarden,
                            AsteroidBelt)


class WorldGenerator():
    # World generator
    def __init__(self):
        world_types_distribution = {TinySulfur: 0.0457488,
                                    TinyIce: 0.16274024,
                                    TinyRock: 0.11266216,
                                    SmallHadean: 0.00312988,
                                    SmallIce: 0.00938964,
                                    SmallRock: 0.05007808,
                                    StandardChthonian: 0.00300024,
                                    StandardGreenhouse: 0.01200096,
                                    StandardAmmonia: 0.05924988,
                                    StandardHadean: 0.01877928,
                                    StandardIce: 0.0312988,
                                    StandardOcean: 0.11266216,
                                    StandardGarden: 0.15899976,
                                    LargeChthonian: 0.00300024,
                                    LargeGreenhouse: 0.01200096,
                                    LargeAmmonia: 0.02699892,
                                    LargeIce: 0.00312988,
                                    LargeGarden: 0.00300024,
                                    LargeOcean: 0.00938964,
                                    AsteroidBelt: 0.16274024}

        world_type = random.choices(list(world_types_distribution.keys()),
                                    weights=list(world_types_distribution.values()))[0]
        self.world = world_type()

    def __str__(self):
        return str(self.world)
