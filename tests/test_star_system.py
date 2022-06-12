import pytest
import numpy as np

from astropy import units as u

from gs4worldbuilding import Star, StarSystem


@pytest.fixture
def sol():
    # returns a StarSystem instance analog to the solar system
    system = StarSystem(garden_host=True)
    system.population = StarSystem.Population.INTERMEDIATE_POPULATION_1
    system.age = 4.7 * u.Ga
    system.make_stars(StarSystem.MultipleStars.UNARY)
    # Sol
    system.A.seed_mass = 1 * u.M_sun
    return system

@pytest.fixture
def procyon():
    # returns a StarSystem instance analog to the procyon system
    system = StarSystem()
    system.population = StarSystem.Population.YOUNG_POPULATION_1
    system.age = 1.37 * u.Ga
    system.make_stars(StarSystem.MultipleStars.BINARY)
    # procyon A
    system.A.seed_mass = 1.37 * u.M_sun
    # procyon B
    # TODO: should be 2.56 instead of 2
    system.B.seed_mass = 2 * u.M_sun
    return system


@pytest.fixture
def aldebaran():
    # returns a StarSystem instance analog to the Aldebaran's host system
    system = StarSystem()
    system.population = StarSystem.Population.OLD_POPULATION_1
    system.age = 6.5 * u.Ga
    system.make_stars(1)
    # Aldebaran
    system.A.seed_mass = 1.13 * u.M_sun
    return system

@pytest.fixture
def van_maanen():
    # returns a StarSystem instance analog to the van maanen's star's host system
    system = StarSystem()
    system.population = StarSystem.Population.INTERMEDIATE_POPULATION_1
    system.age = 4.1 * u.Ga
    system.make_stars(1)
    # van maanen star
    # TODO: should be 2.6 instead of 2
    system.A.seed_mass = 2 * u.M_sun
    return system

@pytest.fixture
def alpha_centauri():
    # returns a StarSystem instance analog to the alpha centauri system
    system = StarSystem()
    system.population = StarSystem.Population.INTERMEDIATE_POPULATION_1
    system.age = 5 * u.Ga
    system.make_stars(3)
    # Alpha Centauri A
    system.A.seed_mass = 1.1 * u.M_sun
    # Alpha Centauri B
    system.B.seed_mass = .9 * u.M_sun
    # Proxima Centauri
    system.C.seed_mass = .12 * u.M_sun
    return system


def test_sol(sol):
    assert (sol.A.luminosity_class == Star.Luminosity.V)
    assert (sol.A.spectral_type == 'G2')
    assert (sol.A.temperature >= 5500 * u.K and
            sol.A.temperature <= 6000 * u.K)
    assert (sol.A.radius >= 0.004 * u.au and sol.A.radius <= 0.006 * u.au)


def test_procyon(procyon):
    assert (procyon.A.luminosity_class == Star.Luminosity.IV)
    assert (procyon.A.temperature >= 6400 * u.K and
            procyon.A.temperature <= 6900 * u.K)
    assert (procyon.A.radius >= 0.008 * u.au and procyon.A.radius <= 0.01 * u.au)
    # TODO: here procyon B mass should be tested at .6
    assert (procyon.B.luminosity_class == Star.Luminosity.D)


def test_aldebaran(aldebaran):
    assert (aldebaran.A.luminosity_class == Star.Luminosity.III)
    assert (aldebaran.A.temperature >= 3000 * u.K and
            aldebaran.A.temperature <= 5000 * u.K)


def test_van_maanen(van_maanen):
    assert (van_maanen.A.luminosity_class == Star.Luminosity.D)
    # TODO: here mass should be tested at .67


def test_alpha_centauri(alpha_centauri):
    assert (alpha_centauri.A.luminosity_class == Star.Luminosity.V)
    assert (alpha_centauri.A.temperature >= 5800 * u.K and
            alpha_centauri.A.temperature <= 6300 * u.K)
    assert (alpha_centauri.A.radius >= 0.0045 * u.au and
            alpha_centauri.A.radius <= 0.0065 * u.au)
    assert (alpha_centauri.B.luminosity_class == Star.Luminosity.V)
    assert (alpha_centauri.B.temperature >= 5200 * u.K and
            alpha_centauri.B.temperature <= 5800 * u.K)
    assert (alpha_centauri.B.radius >= 0.003 * u.au and
            alpha_centauri.B.radius <= 0.005 * u.au)
    assert (alpha_centauri.C.luminosity_class == Star.Luminosity.V)
    assert (alpha_centauri.C.temperature >= 3100 * u.K and
            alpha_centauri.C.temperature <= 3200 * u.K)
    assert (alpha_centauri.C.radius >= 0.000 * u.au and
            alpha_centauri.C.radius <= 0.001 * u.au)


def test_set_seed_mass_raises_exception_on_out_of_bounds(sol):
    with pytest.raises(ValueError):
        sol.A.seed_mass = .5 * u.M_sun


def test_set_seed_mass_raises_exception_on_nan(sol):
    with pytest.raises(ValueError):
        sol.A.seed_mass = np.nan
