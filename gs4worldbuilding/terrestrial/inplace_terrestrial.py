from enum import Enum
from functools import wraps
from abc import ABC
from typing import Tuple, Callable, List, Dict, Type

from ordered_enum import OrderedEnum

from gs4worldbuilding import Planet
from gs4worldbuilding.gas_giant import GasGiant
from gs4worldbuilding.terrestrial import Terrestrial, Size, TinySulfur
from gs4worldbuilding.random import RandomGenerator
from gs4worldbuilding.model.bounds import EnumBounds


class TectonicActivity(OrderedEnum):
    '''class tectonic activity category Enum from corresponding table'''
    NONE = 'No tectonic activity'
    LIGHT = 'Light tectonic activity'
    MODERATE = 'Moderate tectonic activity'
    HEAVY = 'Heavy tectonic activity'
    EXTREME = 'Extreme tectonic activity'


class VolcanicActivity(OrderedEnum):
    '''class volcanic activity category Enum from corresponding table'''
    NONE = 'No volcanic activity'
    LIGHT = 'Light volcanic activity'
    MODERATE = 'Moderate volcanic activity'
    HEAVY = 'Heavy volcanic activity'
    EXTREME = 'Extreme volcanic activity'


class InplaceTerrestrialMixin(Terrestrial, Planet, ABC):
    '''the orbiting world extended model'''
    _precedence = [*[p for p in Terrestrial._precedence if
                     (p != 'temperature' and p != 'resource')],
                   'rotation', 'resonant', 'retrograde', 'axial_tilt',
                   'volcanic_activity', 'tectonic_activity', 'resource']
    _rotation_modifiers = {Size.TINY: 18,
                           Size.SMALL: 14,
                           Size.STANDARD: 10,
                           Size.LARGE: 6}
    _resource_filters: List[Tuple[Callable[['InplaceTerrestrialMixin'], bool],
                            int]] = [
        (lambda x: x.volcanic_activity == VolcanicActivity.NONE, -2),
        (lambda x: x.volcanic_activity == VolcanicActivity.LIGHT, -1),
        (lambda x: x.volcanic_activity == VolcanicActivity.HEAVY, 1),
        (lambda x: x.volcanic_activity == VolcanicActivity.EXTREME, 2)
    ]
    _extra_habitability_filters: List[Tuple[
                                      Callable[['InplaceTerrestrialMixin'],
                                               bool],
                                      int]] = [
        (lambda x: x.volcanic_activity == VolcanicActivity.HEAVY, -1),
        (lambda x: x.tectonic_activity == TectonicActivity.HEAVY, -1),
        (lambda x: x.volcanic_activity == VolcanicActivity.EXTREME, -2),
        (lambda x: x.tectonic_activity == TectonicActivity.EXTREME, -2)
    ]

    _tectonism_table: Dict[int, TectonicActivity] = {
        7: TectonicActivity.NONE,
        11: TectonicActivity.LIGHT,
        15: TectonicActivity.MODERATE,
        19: TectonicActivity.HEAVY
    }

    _tectonism_filters: List[Tuple[Callable[['InplaceTerrestrialMixin'], bool],
                                   int]] = [
        (lambda x: x.volcanic_activity == VolcanicActivity.NONE, -8),
        (lambda x: x.tectonic_activity == VolcanicActivity.LIGHT, -4),
        (lambda x: x.volcanic_activity == VolcanicActivity.HEAVY, 4),
        (lambda x: x.tectonic_activity == VolcanicActivity.EXTREME, 8),
        (lambda x: not x.hydrographic_coverage, -4),
        (lambda x: x.hydrographic_coverage is not None and
         x.hydrographic_coverage < .5, -2),
        (lambda x: x.moons == 1, 2),
        (lambda x: x.moons > 1, 4)
    ]

    def random_resource(self):
        '''sum of a 3d roll times over Resource Value Table with volcanism
modifier'''
        modifier = sum(score if filter(self) else 0 for filter, score
                       in self._resource_filters)
        return self._roll_resource(modifier)

    def random_tectonic_activity(self) -> TectonicActivity:
        '''roll 3d6 on tectonic activity table with modifiers'''
        if self.size > Size.SMALL:
            modifier = sum(score if filter(self) else 0 for filter, score
                           in self._tectonism_filters)
            roll = RandomGenerator().roll3d6(modifier)
            filtered = list(filter(lambda x: roll < x,
                                   self._tectonism_table.keys()))
            return (self._tectonism_table[filtered[0]]
                    if len(filtered) > 0 else TectonicActivity.EXTREME)
        return TectonicActivity.NONE

    def random_volcanic_activity(self) -> None:
        '''roll 3d6 on volcanic activity table with modifiers'''
        table = {17: VolcanicActivity.NONE,
                 21: VolcanicActivity.LIGHT,
                 27: VolcanicActivity.MODERATE,
                 71: VolcanicActivity.HEAVY}
        modifier = round((self.gravity.value /
                          self._orbit.parent_star.age.value) * 40)
        modifiers = [(hasattr(self, '_moons') and len(self._moons) == 1, 5),
                     (hasattr(self, '_moons') and len(self._moons) > 1, 10),
                     (isinstance(self, TinySulfur), 60),
                     (issubclass(type(self._orbit.parent_body), GasGiant), 5)]
        roll = RandomGenerator().roll3d6(modifier + sum(value if truth else 0
                                         for truth, value in modifiers))
        filtered = list(filter(lambda x: roll < x, table.keys()))
        self.volcanic_activity = (table[filtered[0]] if len(filtered) > 0
                                  else VolcanicActivity.EXTREME)

    @property
    def blackbody_temperature(self) -> u.Quantity:
        return Planet.blackbody_temperature.fget(self)

    @property
    def habitability(self) -> int:
        return (Terrestrial.habitability.fget(self) +
                max(sum(score if filter(self) else 0 for filter, score
                        in self._extra_habitability_filters),
                    -2))

    @property
    def resource_bounds(self) -> EnumBounds:
        modifier = sum(score if filter(self) else 0 for filter, score
                       in self._resource_filters)

        value_bounds = self._resource_bounds
        return EnumBounds(value_bounds.lower + modifier,
                          value_bounds.upper + modifier)

    @property
    def temperature(self) -> u.Quantity:
        '''average temperature in K'''
        return (self.blackbody_temperature.value *
                self.blackbody_correction) * u.K

    @temperature.setter
    def temperature(self, _):
        raise AttributeError("can't set overriden attribute")

    @property
    def tectonic_activity(self) -> TectonicActivity:
        '''tectonic activity value on corresponding Table'''
        return self._get_bounded_property('tectonic_activity')

    @property
    def tectonic_activity_bounds(self) -> EnumBounds:
        '''tectonic activity range'''
        table = {7: TectonicActivity.NONE,
                 11: TectonicActivity.LIGHT,
                 15: TectonicActivity.MODERATE,
                 19: TectonicActivity.HEAVY}
        if self.size > Size.SMALL:
            modifier = sum(score if filter(self) else 0 for filter, score
                           in self._tectonism_filters)
            min_roll = sum(value if truth else 0 for truth, value in modifiers) + 3
        filtered = list(filter(lambda x: min_roll < x, table.keys()))
        lower = (table[filtered[0]] if len(filtered) > 0
                 else TectonicActivity.EXTREME)
        max_roll = min_roll + 15
        filtered = list(filter(lambda x: max_roll < x, table.keys()))
        upper = (table[filtered[0]] if len(filtered) > 0
                 else TectonicActivity.EXTREME)
        return (EnumBounds(lower, upper) if self.size > Size.SMALL else
                EnumBounds(TectonicActivity.NONE, TectonicActivity.NONE))

    @tectonic_activity.setter
    def tectonic_activity(self, value):
        if not isinstance(value, TectonicActivity):
            raise ValueError('tectonic activity value type has to be' +
                             f'{TectonicActivity}')
        self._set_bounded_property('tectonic_activity', value)

    @property
    def volcanic_activity(self):
        '''volcanic activity value on corresponding Table'''
        return self._get_bounded_property('volcanic_activity')

    @property
    def volcanic_activity_bounds(self) -> EnumBounds:
        '''volcanic activity range'''
        table = {17: VolcanicActivity.NONE,
                 21: VolcanicActivity.LIGHT,
                 27: VolcanicActivity.MODERATE,
                 71: VolcanicActivity.HEAVY}
        min_roll = round((self.gravity.value /
                         self._orbit.parent_star.age.value) * 40) + 3
        modifiers = [(self.moons == 1, 5),
                     (self.moons > 1, 10),
                     (isinstance(self, TinySulfur), 60),
                     (issubclass(type(self._orbit.parent_body), GasGiant), 5)]
        min_roll += sum(value if truth else 0 for truth, value in modifiers)
        filtered = list(filter(lambda x: min_roll < x, table.keys()))
        lower = (table[filtered[0]] if len(filtered) > 0
                 else VolcanicActivity.EXTREME)
        max_roll = min_roll + 15
        filtered = list(filter(lambda x: max_roll < x, table.keys()))
        upper = (table[filtered[0]] if len(filtered) > 0
                 else VolcanicActivity.EXTREME)
        return EnumBounds(lower, upper)

    @volcanic_activity.setter
    def volcanic_activity(self, value):
        if not isinstance(value, VolcanicActivity):
            raise ValueError('volcanic activity value type has to be ' +
                             f'{VolcanicActivity}')
        self._set_bounded_property('volcanic_activity', value)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)


def place_terrestrial(world_type: Type[Terrestrial], orbit: Orbit):
    '''decorator to make concrete inplace terrestrials'''
    @wraps(world_type, updated=())
    class InplaceTerrestrial(world_type, InplaceTerrestrialMixin):
        '''concrete inplace terrestrial'''

    return InplaceTerrestrial(orbit)


class SatelliteOrbit(Orbit):
    '''the satellite specialized orbit'''
    @property
    def period(self) -> u.Quantity:
        return np.sqrt(self.radius.to(D_earth).value ** 3 /
                       (self._parent_body.mass.value +
                        self._body.mass.value)) * .166 * u.a


def place_satellite(world_type: Type[Terrestrial], orbit: Orbit):
    '''decorator to make concrete satellite from terrestrials'''

    @wraps(world_type, updated=())
    class Satellite(world_type, InplaceTerrestrialMixin):
        '''satellite terrestrial'''

        _precedence = InplaceTerrestrialMixin._precedence

        @property
        def blackbody_temperature(self) -> u.Quantity:
            '''blackbody temperature in K from parent body'''
            return self._orbit.parent_body.blackbody_temperature

        @property
        def solar_day(self) -> u.Quantity:
            '''solar day in standard hours'''
            rotation = -self.rotation if self.retrograde else self.rotation
            return abs((self._orbit.parent_body._orbit.period.to(u.h).value *
                        rotation.to(u.h).value) /
                       (self._orbit.parent_body._orbit.period.to(u.h).value -
                        rotation.to(u.h).value)
                       if rotation != self._orbit.period else np.inf) * u.h

        @property
        def tidal_effect(self) -> float:
            '''the total tidal effect property'''
            # computing the planet tidal force
            tidal_force = ((2230000 * self._orbit.parent_body.mass.value *
                            self.diameter.value) /
                           self._orbit.radius.to(D_earth).value ** 3)
            return round(tidal_force *
                         self._orbit.parent_star.age.value /
                         self.mass.value)

    return Satellite(orbit)