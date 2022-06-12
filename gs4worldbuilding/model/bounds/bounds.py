# -*- coding: utf-8 -*-


class Bounds(object):
    def __init__(self, lower, upper):
        if upper < lower:
            raise ValueError('inconsistent bounds')
        self.lower = lower
        self.upper = upper

    def __iter__(self):
        """return boundaries"""
        return iter([self.lower, self.upper])

    def __eq__(self, obj):
        return (isinstance(obj, type(self)) and
                self.lower == obj.lower and
                self.upper == obj.upper)
