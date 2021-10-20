
import worldgen as w

import pytest
import numpy as np


@pytest.fixture
def sol():
    # returns a StarSystem instance analog to the solar system
    system = w.StarSystem(garden_host=True)
    system.population = w.StarSystem.Population.INTERMEDIATE_POPULATION_1
    system.age = 4.7
    system.make_stars(1)
    # Sol
    system.A.seed_mass = 1
    return system

@pytest.fixture
def procyon():
    # returns a StarSystem instance analog to the procyon system
    system = w.StarSystem()
    system.population = w.StarSystem.Population.YOUNG_POPULATION_1
    system.age = 1.37
    system.make_stars(w.StarSystem.MultipleStars.BINARY)
    # procyon A
    system.A.seed_mass = 1.37
    # procyon B
    # TODO: should be 2.56 instead of 2
    system.B.seed_mass = 2
    return system


@pytest.fixture
def aldebaran():
    # returns a StarSystem instance analog to the Aldebaran's host system
    system = w.StarSystem()
    system.population = w.StarSystem.Population.OLD_POPULATION_1
    system.age = 6.5
    system.make_stars(1)
    # Aldebaran
    system.A.seed_mass = 1.13
    return system

@pytest.fixture
def van_maanen():
    # returns a StarSystem instance analog to the van maanen's star's host system
    system = w.StarSystem()
    system.population = w.StarSystem.Population.INTERMEDIATE_POPULATION_1
    system.age = 4.1
    system.make_stars(1)
    # van maanen star
    # TODO: should be 2.6 instead of 2
    system.A.seed_mass = 2
    return system

@pytest.fixture
def alpha_centauri():
    # returns a StarSystem instance analog to the alpha centauri system
    system = w.StarSystem()
    system.population = w.StarSystem.Population.INTERMEDIATE_POPULATION_1
    system.age = 5
    system.make_stars(3)
    # Alpha Centauri A
    system.A.seed_mass = 1.1
    # Alpha Centauri B
    system.B.seed_mass = .9
    # Proxima Centauri
    system.C.seed_mass = .12
    return system


def test_sol(sol):
    assert (sol.A.luminosity_class == w.Star.Luminosity.V)
    assert (sol.A.spectral_type == 'G2')
    assert (sol.A.temperature >= 3100 and
            sol.A.temperature <= 8200)


def test_procyon(procyon):
    assert (procyon.A.luminosity_class == w.Star.Luminosity.IV)
    # TODO: here procyon B mass should be tested at .6
    assert (procyon.B.luminosity_class == w.Star.Luminosity.D)


def test_aldebaran(aldebaran):
    assert (aldebaran.A.luminosity_class == w.Star.Luminosity.III)
    assert (aldebaran.A.temperature >= 3000 and
            aldebaran.A.temperature <= 5000)


def test_van_maanen(van_maanen):
    assert (van_maanen.A.luminosity_class == w.Star.Luminosity.D)
    # TODO: here mass should be tested at .67


def test_alpha_centauri(alpha_centauri):
    assert (alpha_centauri.A.luminosity_class == w.Star.Luminosity.V)
    assert (alpha_centauri.B.luminosity_class == w.Star.Luminosity.V)
    assert (alpha_centauri.C.luminosity_class == w.Star.Luminosity.V)


def test_set_seed_mass_raises_exception_on_out_of_range(sol):
    with pytest.raises(ValueError):
        sol.A.seed_mass = .5


def test_set_seed_mass_raises_exception_on_nan(sol):
    with pytest.raises(ValueError):
        sol.A.seed_mass = np.nan
