import enum
from typing import Optional

from ordered_enum.ordered_enum import ValueOrderedEnum
from astropy import units as u
from astropy.units import Quantity

from gs4worldbuilding.star import Star
from gs4worldbuilding.orbit import Orbit
from gs4worldbuilding.model.bounds import QuantityBounds, ScalarBounds
from gs4worldbuilding.random import RandomGenerator


@enum.unique
class Separation(Quantity[u.au], ValueOrderedEnum):
    '''Separation Enum from Orbital Separation Table with radius
multiplier in AU'''
    VERY_CLOSE = .05 * u.au
    CLOSE = .5 * u.au
    MODERATE = 2 * u.au
    WIDE = 10 * u.au
    DISTANT = 50 * u.au


class CompanionStarOrbit(Orbit):
    '''The companion star orbit model'''

    def random_eccentricity(self):
        '''sum of a 3d6 roll over Stellar Orbital Eccentricity Table with
        modifiers if any'''
        if self.body.separation == Separation.MODERATE:
            return (RandomGenerator()
                    .truncnorm_draw(0, .8, .4151, .16553546447815948))
        elif self.body.separation == Separation.CLOSE:
            return (RandomGenerator()
                    .truncnorm_draw(0, .7, .3055, .1839014681833726))
        elif self.body.separation == Separation.VERY_CLOSE:
            return (RandomGenerator()
                    .truncexpon_draw(0, .6, .1819450191678794))
        return (RandomGenerator()
                .truncnorm_draw(0, .95, .5204, .142456449485448))

    def random_radius(self):
        '''roll of 2d6 multiplied by the separation category radius'''
        return (RandomGenerator().roll2d6(continuous=True) *
                self.body.separation.value * u.au)

    @property
    def eccentricity_bounds(self) -> ScalarBounds:
        '''value range for eccentricity dependent separation'''
        rngs = {Separation.MODERATE: ScalarBounds(0, .8),
                Separation.CLOSE: ScalarBounds(0, .7),
                Separation.VERY_CLOSE: ScalarBounds(0, .6)}
        return (rngs[self.body.separation]
                if self.body.separation in rngs else ScalarBounds(0, .95))

    @property
    def radius(self) -> Quantity[u.au]:
        '''The average orbital radius to the parent body in AU'''
        return self._get_bounded_property('radius')

    @property
    def radius_bounds(self) -> QuantityBounds:
        '''value range for average orbital radius'''
        return QuantityBounds(2 * self.body.separation.value * u.au,
                              12 * self.body.separation.value * u.au)

    @property
    def body(self) -> 'CompanionStar':
        '''the orbiting body'''
        return self._body

    @radius.setter
    def radius(self, value: Quantity['length']):
        if not isinstance(value, Quantity):
            raise ValueError('expected quantity type value')
        if 'length' not in value.unit.physical_type:
            raise ValueError("can't set radius to value of " +
                             f"{value.unit.physical_type} physical type")
        self._set_bounded_property('radius', value)

    def randomize(self) -> None:
        self.radius = self.random_radius()
        super().randomize()

    def __init__(self, parent_body: Star, body: 'CompanionStar'):
        self._body = body  # here _body is set early to allow random radius
        # it is still forwarded to the Orbit init later
        super().__init__(parent_body, self.random_radius(), body)


class CompanionStar(Star):
    '''The companion star model'''

    def random_seed_mass(self) -> Quantity[u.M_sun]:
        '''companion star random mass procedure'''
        mass = self._parent_body.mass.value
        # roll 1d6 - 1
        roll = int(RandomGenerator().roll1d6(-1))
        if roll >= 1:
            # sum of nd6 roll
            rolls = int(sum([RandomGenerator().roll1d6()
                             for _ in range(roll)]))
            for _ in range(rolls):
                # count down on the stellar mass table
                mass -= (.05 if mass else .10)
        # add noise to value
        noise = .025 if mass <= 1.5 else .05
        mass += RandomGenerator().rng.uniform(-noise, noise)
        # mass in [.1, parent_body.mass] range
        return min(max(.1, mass) * u.M_sun, self._parent_body.mass)

    def random_separation(self) -> Separation:
        '''sum of a 3d6 roll over Orbital Separation Table'''
        return RandomGenerator().choice(list(Separation),
                                        self._separation_dist)

    @property
    def seed_mass_bounds(self) -> QuantityBounds:
        '''value range for mass adjusted so mass cannot be greater than parent
body mass'''
        # TODO: enforce final mass range to be no more than parent mass (not seed mass)
        return QuantityBounds(.1 * u.M_sun, 2 * u.M_sun)

    @property
    def separation(self) -> Separation:
        '''separation category over Orbital Separation Table'''
        return self._get_bounded_property('separation')

    @property
    def separation_bounds(self) -> QuantityBounds:
        '''separation bounds for instance'''
        return self._separation_bounds

    @separation.setter
    def separation(self, value):
        if not isinstance(value, Separation):
            raise ValueError('separation value type must be ' +
                             f'{Separation}')
        self._set_bounded_property('separation', value)

    @property
    def forbidden_zone(self) -> Optional[QuantityBounds]:
        '''the forbidden zone limits in AU if any'''
        if self._companions:
            return QuantityBounds(self._orbit.min_separation / 3,
                                  self._orbit.max_separation * 3)
        return super(CompanionStar, self).forbidden_zone

    def randomize(self) -> None:
        super().randomize()
        self.separation = self.random_separation()
        self._orbit = CompanionStarOrbit(self._parent_body, self)

    def __init__(self, star_system, parent_body: Star, tertiary_star=False,
                 sub_companion=False):
        self._parent_body = parent_body

        if not sub_companion:
            if star_system.garden_host and tertiary_star:
                self._separation_dist = [0, 0, 0, .01851851851853,
                                         .98148148148193]
                self._separation_bounds = QuantityBounds(Separation.WIDE,
                                                         Separation.DISTANT)
            elif star_system.garden_host:
                self._separation_dist = [0, .0463, .11574, .33796, .5]
                self._separation_bounds = QuantityBounds(Separation.CLOSE,
                                                         Separation.DISTANT)
            elif tertiary_star:
                self._separation_dist = [0, .00462963, .041666667, .212962963,
                                         .740740741]
                self._separation_bounds = QuantityBounds(Separation.CLOSE,
                                                         Separation.DISTANT)
            else:
                self._separation_dist = [.0926, .2824, .25, .2824, .0926]
                self._separation_bounds = QuantityBounds(Separation.VERY_CLOSE,
                                                         Separation.DISTANT)
        else:
            self._separation_dist = [.740740741, .212962963, .041666667,
                                     .00462963, 0]
            self._separation_bounds = QuantityBounds(Separation.VERY_CLOSE,
                                                     Separation.WIDE)
        Star.__init__(self, star_system)
        self.separation = self.random_separation()
        self._orbit = CompanionStarOrbit(parent_body, self)
