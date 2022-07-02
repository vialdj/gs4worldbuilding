import pytest
import numpy as np

from astropy import units as u

from gs4worldbuilding.star_system import StarSystem, Population
from gs4worldbuilding.star import Luminosity


@pytest.fixture
def sol():
    # returns a StarSystem instance analog to the solar system
    system = StarSystem(garden_host=True, n_stars=1)
    system.population = Population.INTERMEDIATE_POPULATION_1
    system.age = 4.7 * u.Ga
    # Sol
    system[0].seed_mass = 1 * u.M_sun
    return system


@pytest.fixture
def procyon():
    # returns a StarSystem instance analog to the procyon system
    system = StarSystem(n_stars=2)
    system.population = Population.YOUNG_POPULATION_1
    system.age = 1.37 * u.Ga
    # procyon A
    system[0].seed_mass = 1.37 * u.M_sun
    # procyon B
    # TODO: should be 2.56 instead of 2
    system[1].seed_mass = 2 * u.M_sun
    return system


@pytest.fixture
def aldebaran():
    # returns a StarSystem instance analog to the Aldebaran's host system
    system = StarSystem(n_stars=1)
    system.population = Population.OLD_POPULATION_1
    system.age = 6.5 * u.Ga
    # Aldebaran
    system[0].seed_mass = 1.13 * u.M_sun
    return system


@pytest.fixture
def van_maanen():
    # returns a StarSystem instance analog to the van maanen's star's host system
    system = StarSystem(n_stars=1)
    system.population = Population.INTERMEDIATE_POPULATION_1
    system.age = 4.1 * u.Ga
    # van maanen star
    # TODO: should be 2.6 instead of 2
    system[0].seed_mass = 2 * u.M_sun
    return system


@pytest.fixture
def alpha_centauri():
    # returns a StarSystem instance analog to the alpha centauri system
    system = StarSystem(n_stars=3)
    system.population = Population.INTERMEDIATE_POPULATION_1
    system.age = 5 * u.Ga
    # Alpha Centauri A
    system[0].seed_mass = 1.1 * u.M_sun
    # Alpha Centauri B
    system[1].seed_mass = .9 * u.M_sun
    # Proxima Centauri
    system[2].seed_mass = .12 * u.M_sun
    return system


def test_sol(sol):
    assert len(sol) == 1
    assert sol[0].luminosity_class == Luminosity.V
    assert sol[0].spectral_type == 'G2'
    assert (sol[0].temperature >= 5500 * u.K and
            sol[0].temperature <= 6000 * u.K)
    assert (sol[0].radius >= 0.004 * u.au and
            sol[0].radius <= 0.006 * u.au)


def test_procyon(procyon):
    assert len(procyon) == 2
    assert procyon[0].luminosity_class == Luminosity.IV
    assert (procyon[0].temperature >= 6400 * u.K and
            procyon[0].temperature <= 6900 * u.K)
    assert (procyon[0].radius >= 0.008 * u.au and
            procyon[0].radius <= 0.01 * u.au)
    # TODO: here procyon B mass should be tested at .6
    assert procyon[1].luminosity_class == Luminosity.D


def test_aldebaran(aldebaran):
    assert len(aldebaran) == 1
    assert aldebaran[0].luminosity_class == Luminosity.III
    assert (aldebaran[0].temperature >= 3000 * u.K and
            aldebaran[0].temperature <= 5000 * u.K)


def test_van_maanen(van_maanen):
    assert len(van_maanen) == 1
    assert van_maanen[0].luminosity_class == Luminosity.D
    # TODO: here mass should be tested at .67


def test_alpha_centauri(alpha_centauri):
    assert len(alpha_centauri) == 3
    assert alpha_centauri[0].luminosity_class == Luminosity.V
    assert (alpha_centauri[0].temperature >= 5800 * u.K and
            alpha_centauri[0].temperature <= 6300 * u.K)
    assert (alpha_centauri[0].radius >= 0.0045 * u.au and
            alpha_centauri[0].radius <= 0.0065 * u.au)
    assert alpha_centauri[1].luminosity_class == Luminosity.V
    assert (alpha_centauri[1].temperature >= 5200 * u.K and
            alpha_centauri[1].temperature <= 5800 * u.K)
    assert (alpha_centauri[1].radius >= 0.003 * u.au and
            alpha_centauri[1].radius <= 0.005 * u.au)
    assert alpha_centauri[2].luminosity_class == Luminosity.V
    assert (alpha_centauri[2].temperature >= 3100 * u.K and
            alpha_centauri[2].temperature <= 3200 * u.K)
    assert (alpha_centauri[2].radius >= 0.000 * u.au and
            alpha_centauri[2].radius <= 0.001 * u.au)


def test_set_seed_mass_raises_exception_on_out_of_bounds(sol):
    with pytest.raises(ValueError):
        sol[0].seed_mass = .5 * u.M_sun


def test_set_seed_mass_raises_exception_on_nan(sol):
    with pytest.raises(ValueError):
        sol[0].seed_mass = np.nan
