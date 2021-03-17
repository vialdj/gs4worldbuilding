from world import World

"""
world generator.
"""
class WorldGenerator():
    def __init__(self):
        self.world = World()

    def __str__(self):
        return str(self.world)
