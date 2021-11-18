from worldgen import world, StarSystem
from random import choices


class Builder():
        
    @staticmethod
    def build_world():
        dist = {world.TinySulfur: .0457488,
                world.TinyIce: .16274024,
                world.TinyRock: .11266216,
                world.SmallHadean: .00312988,
                world.SmallIce: .00938964,
                world.SmallRock: .05007808,
                world.StandardChthonian: .00300024,
                world.StandardGreenhouse: .01200096,
                world.StandardAmmonia: .05924988,
                world.StandardHadean: .01877928,
                world.StandardIce: .0312988,
                world.StandardOcean: .11266216,
                world.StandardGarden: .15899976,
                world.LargeChthonian: .00300024,
                world.LargeGreenhouse: .01200096,
                world.LargeAmmonia: .02699892,
                world.LargeIce: .00312988,
                world.LargeGarden: .00300024,
                world.LargeOcean: .00938964,
                world.AsteroidBelt: .16274024}

        world_type = choices(list(dist.keys()),
                             weights=list(dist.values()))[0]
        return world_type()

    @staticmethod
    def build_star_system():
        return StarSystem()
