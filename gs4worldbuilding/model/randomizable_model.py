from abc import ABC

from . import Model


class RandomizableModel(Model, ABC):
    """the Randomizable model specialization"""

    _precedence = []

    def randomize(self):
        """randomizes applicable properties values with precedence
constraints"""
        # randomizable properties
        props = list(filter(lambda x: hasattr(self, f'random_{x}'),
                            self._precedence))
        for prop in props:
            getattr(type(self), f'random_{prop}')(self)
