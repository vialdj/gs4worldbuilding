
import worldgen as w

import pytest
import numpy as np


@pytest.fixture
def garden_system():
    # returns a StarSystem instance analog to the solar system
    system = w.StarSystem(garden_host=True)
    system.population = w.StarSystem.Population.INTERMEDIATE_POPULATION_1
    system.age = 4.7
    return system

@pytest.fixture
def subgiant_system():
    # returns a StarSystem instance analog to the procyon system
    system = w.StarSystem()
    system.population = w.StarSystem.Population.YOUNG_POPULATION_1
    system.age = 1.37
    return system


@pytest.fixture
def red_giant_system():
    # returns a StarSystem instance analog to the aldebaran system
    system = w.StarSystem()
    system.population = w.StarSystem.Population.OLD_POPULATION_1
    system.age = 6.5
    return system

@pytest.fixture
def white_dwarf_system():
    # returns a StarSystem instance analog to the van maanen system
    system = w.StarSystem()
    system.population = w.StarSystem.Population.INTERMEDIATE_POPULATION_1
    system.age = 4.1
    return system

@pytest.fixture
def G2V_garden_system(garden_system):
    # returns a Star instance analog to the Sun
    # sol
    star = w.Star(garden_system)
    star.seed_mass = 1
    return star

@pytest.fixture
def IV(subgiant_system):
    # returns a Star instance of the subgiant classification
    # procyon
    star = w.Star(subgiant_system)
    star.seed_mass = 1.37
    return star

@pytest.fixture
def III(red_giant_system):
    # returns a Star instance of the red giant classification
    # aldebaran
    star = w.Star(red_giant_system)
    star.seed_mass = 1.13
    return star

@pytest.fixture
def D(white_dwarf_system):
    # returns a Star instance of the white dwarf classification
    # van maanen star
    star = w.Star(white_dwarf_system)
    # TODO: should be 2.6 instead of 2
    star.seed_mass = 2
    return star


def test_G2V_garden_system(G2V_garden_system):
    assert (G2V_garden_system.luminosity_class == w.Star.Luminosity.V)
    assert (G2V_garden_system.spectral_type == 'G2')
    assert (G2V_garden_system.temperature >= 3100 and
            G2V_garden_system.temperature <= 8200)


def test_IV(IV):
    assert (IV.luminosity_class == w.Star.Luminosity.IV)


def test_III(III):
    assert (III.luminosity_class == w.Star.Luminosity.III)
    assert (III.temperature >= 3000 and III.temperature <= 5000)


def test_D(D):
    assert (D.luminosity_class == w.Star.Luminosity.D)
    # TODO: here mass should be tested at .67


def test_set_seed_mass_raises_exception_on_out_of_range(G2V_garden_system):
    with pytest.raises(ValueError):
        G2V_garden_system.seed_mass = .5


def test_set_seed_mass_raises_exception_on_nan(G2V_garden_system):
    with pytest.raises(ValueError):
        G2V_garden_system.seed_mass = np.nan
