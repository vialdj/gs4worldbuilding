
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
def G2V_garden_system(garden_system):
    # returns a Star instance analog to the sun
    star = w.Star(garden_system)
    star.seed_mass = 1
    return star


def test_get_luminosity_class(G2V_garden_system):
    assert (G2V_garden_system.luminosity_class == w.Star.Luminosity.V)


def test_get_spectral_type(G2V_garden_system):
    assert (G2V_garden_system.spectral_type == 'G2')


def test_set_seed_mass_raises_exception_on_out_of_range(G2V_garden_system):
    with pytest.raises(ValueError):
        G2V_garden_system.seed_mass = .5


def test_set_seed_mass_raises_exception_on_nan(G2V_garden_system):
    with pytest.raises(ValueError):
        G2V_garden_system.seed_mass = np.nan
