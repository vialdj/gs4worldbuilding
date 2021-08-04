import worldgen as wgen

from random import choices


class Builder():
    # World generator
    def __init__(self):
        self.terrestrial_dist = {wgen.TinySulfur: .0457488,
                                 wgen.TinyIce: .16274024,
                                 wgen.TinyRock: .11266216,
                                 wgen.SmallHadean: .00312988,
                                 wgen.SmallIce: .00938964,
                                 wgen.SmallRock: .05007808,
                                 wgen.StandardChthonian: .00300024,
                                 wgen.StandardGreenhouse: .01200096,
                                 wgen.StandardAmmonia: .05924988,
                                 wgen.StandardHadean: .01877928,
                                 wgen.StandardIce: .0312988,
                                 wgen.StandardOcean: .11266216,
                                 wgen.StandardGarden: .15899976,
                                 wgen.LargeChthonian: .00300024,
                                 wgen.LargeGreenhouse: .01200096,
                                 wgen.LargeAmmonia: .02699892,
                                 wgen.LargeIce: .00312988,
                                 wgen.LargeGarden: .00300024,
                                 wgen.LargeOcean: .00938964,
                                 wgen.AsteroidBelt: .16274024}

    def build_world(self):
        world_type = choices(list(self.terrestrial_dist.keys()),
                             weights=list(self.terrestrial_dist.values()))[0]
        return world_type()

    def build_star_system(self):
        return wgen.StarSystem()
