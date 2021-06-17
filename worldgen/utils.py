from collections import namedtuple


class Range(namedtuple('Range', ['min', 'max'])):
    """value range named tuple"""
    def __str__(self):
        return ('({} to {})'.format(self.min, self.max))
