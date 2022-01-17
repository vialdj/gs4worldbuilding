# -*- coding: utf-8 -*-


class Bounds(object):
    def __init__(self, min, max):
        if max < min:
            raise ValueError('inconsistent bounds')
        self.min = min
        self.max = max

    def __iter__(self):
        """return boundaries"""
        return iter([self.min, self.max])

    def __eq__(self, obj):
        return (isinstance(obj, type(self)) and
                self.min == obj.min and
                self.max == obj.max)
