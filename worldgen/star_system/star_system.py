from .. import RandomizableModel
from .. import Star

from collections import namedtuple
from random import choices


class StarSystem(RandomizableModel):
    """the StarSystem model"""

    _precedence = ['stars']

    def __random_unary(self):
        pass

    def __random_binary(self):
        self.secondary_star = Star()

    def __random_tertiary(self):
        self.secondary_star = Star()
        self.tertiary_star = Star()

    def random_stars(self):
        self.primary_star = Star()
        randomize = choices([self.__random_unary, self.__random_binary, self.__random_tertiary],
                            weights=[.5, .4537, .0463],
                            k=1)[0]
        randomize()

    @property
    def primary_star(self):
        return self._primary_star

    @primary_star.setter
    def primary_star(self, value):
        self._primary_star = value

    @property
    def secondary_star(self):
        return self._secondary_star if hasattr(self, '_secondary_star') else None

    @secondary_star.setter
    def secondary_star(self, value):
        self._secondary_star = value

    @property
    def tertiary_star(self):
        return self._tertiary_star if hasattr(self, '_tertiary_star') else None

    @tertiary_star.setter
    def tertiary_star(self, value):
        self._tertiary_star = value

    def __init__(self):
        self.randomize()
