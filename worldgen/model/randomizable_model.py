from . import Model


class RandomizableModel(Model):
    """the Randomizable model specialization"""

    _precedence = []
    locked = False

    def randomize(self):
        """randomizes applicable properties values with precedence
constraints"""
        # randomizable properties
        if not self.locked:
            props = list(filter(lambda x: hasattr(self, 'random_{}'.format(x)),
                                self._precedence))
            for prop in props:
                getattr(type(self), 'random_{}'.format(prop))(self)