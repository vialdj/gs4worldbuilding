from typing import Type, Dict, Optional

from gs4worldbuilding import StarSystem
from gs4worldbuilding.terrestrial import (
    TinySulfur, TinyIce, TinyRock, SmallHadean, SmallIce,
    SmallRock, StandardChthonian, StandardGreenhouse,
    StandardAmmonia, StandardHadean, StandardIce,
    StandardOcean, StandardGarden, LargeChthonian,
    LargeGreenhouse, LargeAmmonia, LargeIce,
    LargeGarden, LargeOcean
)
from gs4worldbuilding.asteroid_belt import AsteroidBelt
from gs4worldbuilding.random import RandomGenerator
from gs4worldbuilding.world import World


class Builder():
    '''Builder class'''
    __instance: Optional['Builder'] = None
    __world_distribution: Dict[Type[World], float] = {
        TinySulfur: .0457488,
        TinyIce: .16274024,
        TinyRock: .11266216,
        SmallHadean: .00312988,
        SmallIce: .00938964,
        SmallRock: .05007808,
        StandardChthonian: .00300024,
        StandardGreenhouse: .01200096,
        StandardAmmonia: .05924988,
        StandardHadean: .01877928,
        StandardIce: .0312988,
        StandardOcean: .11266216,
        StandardGarden: .15899976,
        LargeChthonian: .00300024,
        LargeGreenhouse: .01200096,
        LargeAmmonia: .02699892,
        LargeIce: .00312988,
        LargeGarden: .00300024,
        LargeOcean: .00938964,
        AsteroidBelt: .16274024
    }

    def __new__(cls, *args, **kwargs) -> 'Builder':
        if Builder.__instance is None:
            Builder.__instance = super().__new__(cls, *args, **kwargs)
        return Builder.__instance

    def build_world(self, seed: Optional[int] = None) -> World:
        '''Draw a random world'''
        if seed:
            RandomGenerator().seed = seed
        # consecutive 3d6 rolls over Overall Type Table and World Type Table
        world_type = RandomGenerator().choice(
            list(self.__world_distribution.keys()),
            list(self.__world_distribution.values())
        )
        return world_type()

    def build_star_system(self, seed: Optional[int] = None) -> StarSystem:
        """Draw a full star system"""
        if seed:
            RandomGenerator().seed = seed
        return StarSystem()
