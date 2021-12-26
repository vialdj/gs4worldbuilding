from gs4stargen import terrestrial, StarSystem
from random import choices


class Builder():

    @staticmethod
    def build_world():
        dist = {terrestrial.TinySulfur: .0457488,
                terrestrial.TinyIce: .16274024,
                terrestrial.TinyRock: .11266216,
                terrestrial.SmallHadean: .00312988,
                terrestrial.SmallIce: .00938964,
                terrestrial.SmallRock: .05007808,
                terrestrial.StandardChthonian: .00300024,
                terrestrial.StandardGreenhouse: .01200096,
                terrestrial.StandardAmmonia: .05924988,
                terrestrial.StandardHadean: .01877928,
                terrestrial.StandardIce: .0312988,
                terrestrial.StandardOcean: .11266216,
                terrestrial.StandardGarden: .15899976,
                terrestrial.LargeChthonian: .00300024,
                terrestrial.LargeGreenhouse: .01200096,
                terrestrial.LargeAmmonia: .02699892,
                terrestrial.LargeIce: .00312988,
                terrestrial.LargeGarden: .00300024,
                terrestrial.LargeOcean: .00938964,
                # terrestrial.AsteroidBelt: .16274024
                }

        # consecutive 3d6 rolls over Overall Type Table and World Type Table
        terrestrial_type = choices(list(dist.keys()),
                             weights=list(dist.values()))[0]
        return terrestrial_type()

    @staticmethod
    def build_star_system():
        return StarSystem()
