# -*- coding: utf-8 -*-

class World():
    """The world model."""
    def __init__(self, ocean_coverage, atmospheric_mass,
                 atmospheric_composition):
        # The proportion of surface occupied by liquid elements
        self.ocean_coverage = ocean_coverage
        # Atmospheric mass in earth atm ⊕
        self.atmospheric_mass = atmospheric_mass
        # Atmospheric composition as a list of elements
        self.atmospheric_composition = atmospheric_composition

    def __str__(self):
        return 'self'.format(self=self)

class TinySulfur(World):
    def __init__(self):
        super().__init__(ocean_coverage=.0, atmospheric_mass=.0,
                         atmospheric_composition=[])

class TinyIce(World):
    def __init__(self):
        super().__init__(ocean_coverage=.0, atmospheric_mass=.0,
                         atmospheric_composition=[])

class TinyRock(World):
    def __init__(self):
        super().__init__(ocean_coverage=.0, atmospheric_mass=.0,
                         atmospheric_composition=[])

class SmallHadean(World):
    def __init__(self):
        super().__init__(ocean_coverage=.0, atmospheric_mass=.0,
                         atmospheric_composition=[])

class SmallIce(World):
    def __init__(self):
        super().__init__(ocean_coverage=random.uniform(.3, .8),
                         atmospheric_mass=random.uniform(.5, 1.5),
                         atmospheric_composition=['N2', 'CH4'])

class SmallRock(World):
    def __init__(self):
        super().__init__(ocean_coverage=.0, atmospheric_mass=.0,
                         atmospheric_composition=[])

class StandardChthonian(World):
    def __init__(self):
        super().__init__(ocean_coverage=.0, atmospheric_mass=.0,
                         atmospheric_composition=[])

class StandardGreenhouse(World):
    def __init__(self):
        ocean_coverage = random.uniform(.0, .5)
        super().__init__(ocean_coverage=ocean_coverage,
                         atmospheric_mass=random.uniform(.5, 1.5),
                         atmospheric_composition=['CO2'] if ocean_coverage > 0 else ['N2', 'H2O', 'O2'])

class StandardAmmonia(World):
    def __init__(self):
        super().__init__(ocean_coverage=random.uniform(.5, 1.0),
                         atmospheric_mass=random.uniform(.5, 1.5),
                         atmospheric_composition=['N2', 'NH3', 'CH4'])

class StandardHadean(World):
    def __init__(self):
        super().__init__(ocean_coverage=.0, atmospheric_mass=.0,
                         atmospheric_composition=[])

class StandardIce(World):
    def __init__(self):
        super().__init__(ocean_coverage=random.uniform(.0, .2),
                         atmospheric_mass=random.uniform(.5, 1.5),
                         atmospheric_composition=['CO2', 'N2'])

class StandardOcean(World):
    def __init__(self):
        super().__init__(ocean_coverage=random.uniform(.5, 1.0),
                         atmospheric_mass=random.uniform(.5, 1.5),
                         atmospheric_composition=['CO2', 'N2'])

class StandardGarden(World):
    def __init__(self):
        super().__init__(ocean_coverage=random.uniform(.5, 1.0),
                         atmospheric_mass=random.uniform(.5, 1.5),
                         atmospheric_composition=['N2', 'O2'])

class LargeChthonian(World):
    def __init__(self):
        super().__init__(ocean_coverage=.0, atmospheric_mass=.0
                         atmospheric_composition=[])

class LargeGreenhouse(World):
    def __init__(self):
        super().__init__(ocean_coverage=random.uniform(.0, .5),
                         atmospheric_mass=random.uniform(.5, 1.5),
                         atmospheric_composition=['CO2', 'N2', 'H2O', 'O2'])

class LargeAmmonia(World):
    def __init__(self):
        super().__init__(ocean_coverage=random.uniform(0.5, 1.0),
                         atmospheric_mass=random.uniform(.5, 1.5),
                         atmospheric_composition=['He', 'NH3', 'CH4'])

class LargeIce(World):
    def __init__(self):
        super().__init__(ocean_coverage=random.uniform(.0, .2),
                         atmospheric_mass=random.uniform(.5, 1.5),
                         atmospheric_composition=['He', 'N2'])

class LargeOcean(World):
    def __init__(self):
        super().__init__(ocean_coverage=random.uniform(.6, 1.0),
                         atmospheric_mass=random.uniform(.5, 1.5),
                         atmospheric_composition=['He', 'N2'])

class LargeGarden(World):
    def __init__(self):
        super().__init__(ocean_coverage=random.uniform(.6, 1.0),
                         atmospheric_mass=random.uniform(.5, 1.5),
                         atmospheric_composition=['N2', 'O2', 'He', 'Ne', 'Ar',
                                                  'Kr', 'Xe'])

class AsteroidBelt(World):
    def __init__(self):
        super().__init__(ocean_coverage=.0,
                         atmospheric_mass=.0,
                         atmospheric_composition=[])
