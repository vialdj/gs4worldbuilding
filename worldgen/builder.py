import worldgen

from random import choices


class Builder():
    # World generator
    def __init__(self):
        self.terrestrial_distribution = {worldgen.TinySulfur: 0.0457488,
                                         worldgen.TinyIce: 0.16274024,
                                         worldgen.TinyRock: 0.11266216,
                                         worldgen.SmallHadean: 0.00312988,
                                         worldgen.SmallIce: 0.00938964,
                                         worldgen.SmallRock: 0.05007808,
                                         worldgen.StandardChthonian: 0.00300024,
                                         worldgen.StandardGreenhouse: 0.01200096,
                                         worldgen.StandardAmmonia: 0.05924988,
                                         worldgen.StandardHadean: 0.01877928,
                                         worldgen.StandardIce: 0.0312988,
                                         worldgen.StandardOcean: 0.11266216,
                                         worldgen.StandardGarden: 0.15899976,
                                         worldgen.LargeChthonian: 0.00300024,
                                         worldgen.LargeGreenhouse: 0.01200096,
                                         worldgen.LargeAmmonia: 0.02699892,
                                         worldgen.LargeIce: 0.00312988,
                                         worldgen.LargeGarden: 0.00300024,
                                         worldgen.LargeOcean: 0.00938964,
                                         worldgen.AsteroidBelt: 0.16274024}

    def build_world(self):
        world_type = choices(list(self.terrestrial_distribution.keys()),
                             weights=list(self.terrestrial_distribution.values()))[0]
        return world_type()

    def build_star_system(self):
        return worldgen.StarSystem()
