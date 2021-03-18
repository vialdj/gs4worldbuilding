# -*- coding: utf-8 -*-

import random
from math import floor

class World(object):
    """The world model. Each World Types is build using a proccess close to the
    World Design Sequence from gurps space 4th edition step 2 to step 5.
    World Types are represented by the World subclasses"""
    def __init__(self, avg_srf_temperature, absorption_factor,
                 ocean_coverage=.0, atm_mass=.0, atm_composition=[],
                 greenhouse_factor=.0):
        # The proportion of surface occupied by liquid elements
        self.ocean_coverage = ocean_coverage
        # atm mass in earth atm⊕
        self.atm_mass = atm_mass
        # atm composition as a list of elements
        self.atm_composition = atm_composition
        # The average temperature in kelvins K
        self.avg_srf_temperature = avg_srf_temperature

        """dependent to worldtype given in gurps space 4th edition Temperature
        Factors Table"""
        self.absorption_factor = absorption_factor
        self.greenhouse_factor = greenhouse_factor


        # A string corresponding to the projected climate
        self.climate = self.__climate(avg_srf_temperature)
        # The blackbody temperature in kelvin K
        self.blackbody_temperature = self.__blackbody_temperature(absorption_factor,
                                                                  greenhouse_factor,
                                                                  atm_mass,
                                                                  avg_srf_temperature)

    def __str__(self):
        return '{self.__class__.__name__} (ocean coverage= {self.ocean_coverage},\
 atmosphere mass= {self.atm_mass} atm⊕, \
atmosphere composition= {self.atm_composition}, \
average surface temperature= {self.avg_srf_temperature} K, \
climate= {self.climate}, \
blackbody temperature= {self.blackbody_temperature} K)'.format(self=self)

    """associate proper climate from given average surface temperature in K
    based on gurps space 4th edition World Climate Table"""
    def __climate(self, temperature):
        if temperature < 244:
            return 'Frozen'
        elif 244 <= temperature < 255:
            return 'Very Cold'
        elif 255 <= temperature < 266:
            return 'Cold'
        elif 266 <= temperature < 278:
            return 'Chilly'
        elif 278 <= temperature < 289:
            return 'Cool'
        elif 289 <= temperature < 300:
            return 'Normal'
        elif 300 <= temperature < 311:
            return 'Warm'
        elif 311 <= temperature < 322:
            return 'Tropical'
        elif 322 <= temperature < 333:
            return 'Hot'
        elif 333 <= temperature < 344:
            return 'Very Hot'
        else:
            return 'Infernal'

    """ From gurps space 4th edition as blackbody temperature B = T / C where
    C = A * [1 + (M * G)] """
    def __blackbody_temperature(self,
                                absorption_factor,
                                greenhouse_factor,
                                atm_mass,
                                avg_srf_temperature):
        return avg_srf_temperature / (absorption_factor * floor(1 + atm_mass * greenhouse_factor))

class TinySulfur(World):
    def __init__(self):
        super(TinySulfur, self).__init__(avg_srf_temperature=random.randint(80, 140),
                         absorption_factor=.77)

class TinyIce(World):
    def __init__(self):
        super(TinyIce, self).__init__(avg_srf_temperature=random.randint(80, 140),
                         absorption_factor=.86)

class TinyRock(World):
    def __init__(self):
        super(TinyRock, self).__init__(avg_srf_temperature=random.randint(140, 500),
                         absorption_factor=.97)

class SmallHadean(World):
    def __init__(self):
        super(SmallHadean, self).__init__(avg_srf_temperature=random.randint(50, 80),
                         absorption_factor=.67)

class SmallIce(World):
    def __init__(self):
        super(SmallIce, self).__init__(ocean_coverage=random.uniform(.3, .8),
                         atm_mass=random.uniform(.5, 1.5),
                         atm_composition=['N2', 'CH4'],
                         avg_srf_temperature=random.randint(80, 140),
                         absorption_factor=.93, greenhouse_factor=.1)

class SmallRock(World):
    def __init__(self):
        super(SmallRock, self).__init__(avg_srf_temperature=random.randint(140, 500),
                         absorption_factor=.96)

class StandardChthonian(World):
    def __init__(self):
        super(StandardChthonian, self).__init__(avg_srf_temperature=random.randint(500, 950),
                         absorption_factor=.97)

class StandardGreenhouse(World):
    def __init__(self):
        ocean_coverage = random.uniform(.0, .5)
        super(StandardGreenhouse, self).__init__(ocean_coverage=ocean_coverage,
                         atm_mass=random.uniform(.5, 1.5),
                         atm_composition=['CO2'] if ocean_coverage == 0 else ['N2', 'H2O', 'O2'],
                         avg_srf_temperature=random.randint(500, 950),
                         absorption_factor=.77, greenhouse_factor=2.0)

class StandardAmmonia(World):
    def __init__(self):
        super(StandardAmmonia, self).__init__(ocean_coverage=random.uniform(.5, 1.0),
                         atm_mass=random.uniform(.5, 1.5),
                         atm_composition=['N2', 'NH3', 'CH4'],
                         avg_srf_temperature=random.randint(140, 215),
                         absorption_factor=.84, greenhouse_factor=.2)

class StandardHadean(World):
    def __init__(self):
        super(StandardHadean, self).__init__(avg_srf_temperature=random.randint(50, 80),
                         absorption_factor=.67)

class StandardIce(World):
    def __init__(self):
        super(StandardIce, self).__init__(ocean_coverage=random.uniform(.0, .2),
                         atm_mass=random.uniform(.5, 1.5),
                         atm_composition=['CO2', 'N2'],
                         avg_srf_temperature=random.randint(80, 230),
                         absorption_factor=.86, greenhouse_factor=.2)

class StandardOcean(World):
    def __init__(self):
        super(StandardOcean, self).__init__(ocean_coverage=random.uniform(.5, 1.0),
                         atm_mass=random.uniform(.5, 1.5),
                         atm_composition=['CO2', 'N2'],
                         avg_srf_temperature=random.randint(80, 140),
                         absorption_factor=.88, greenhouse_factor=.16)

class StandardGarden(World):
    def __init__(self):
        super(StandardGarden, self).__init__(ocean_coverage=random.uniform(.5, 1.0),
                         atm_mass=random.uniform(.5, 1.5),
                         atm_composition=['N2', 'O2'],
                         avg_srf_temperature=random.randint(250, 340),
                         absorption_factor=.88, greenhouse_factor=.16)

class LargeChthonian(World):
    def __init__(self):
        super(LargeChthonian, self).__init__(avg_srf_temperature=random.randint(500, 950),
                         absorption_factor=.97)

class LargeGreenhouse(World):
    def __init__(self):
        ocean_coverage = random.uniform(.0, .5)
        super(LargeGreenhouse, self).__init__(ocean_coverage=ocean_coverage,
                         atm_mass=random.uniform(.5, 1.5),
                         atm_composition=['CO2'] if ocean_coverage == 0 else ['N2', 'H2O', 'O2'],
                         avg_srf_temperature=random.randint(500, 950),
                         absorption_factor=.77, greenhouse_factor=2.0)

class LargeAmmonia(World):
    def __init__(self):
        super(LargeAmmonia, self).__init__(ocean_coverage=random.uniform(0.5, 1.0),
                         atm_mass=random.uniform(.5, 1.5),
                         atm_composition=['He', 'NH3', 'CH4'],
                         avg_srf_temperature=random.randint(140, 215),
                         absorption_factor=.84, greenhouse_factor=.2)

class LargeIce(World):
    def __init__(self):
        super(LargeIce, self).__init__(ocean_coverage=random.uniform(.0, .2),
                         atm_mass=random.uniform(.5, 1.5),
                         atm_composition=['He', 'N2'],
                         avg_srf_temperature=random.randint(80, 230),
                         absorption_factor=.86, greenhouse_factor=.2)

class LargeOcean(World):
    def __init__(self):
        super(LargeOcean, self).__init__(ocean_coverage=random.uniform(.7, 1.0),
                         atm_mass=random.uniform(.5, 1.5),
                         atm_composition=['He', 'N2'],
                         avg_srf_temperature=random.randint(250, 340),
                         absorption_factor=.88, greenhouse_factor=.16)

class LargeGarden(World):
    def __init__(self):
        super(LargeGarden, self).__init__(ocean_coverage=random.uniform(.6, 1.0),
                         atm_mass=random.uniform(.5, 1.5),
                         atm_composition=['N2', 'O2', 'He', 'Ne', 'Ar',
                                                  'Kr', 'Xe'],
                         avg_srf_temperature=random.randint(250, 340),
                         absorption_factor=.88, greenhouse_factor=.16)

class AsteroidBelt(World):
    def __init__(self):
        super(AsteroidBelt, self).__init__(avg_srf_temperature=random.randint(140, 500),
                         absorption_factor=.97)
