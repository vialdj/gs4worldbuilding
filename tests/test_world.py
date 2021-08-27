import worldgen as w

from worldgen.world.marginal_atmosphere import Marginal

import pytest
import numpy as np


@pytest.fixture
def asteroid_belt():
    # returns an AsteroidBelt instance
    return w.AsteroidBelt()


@pytest.fixture
def large_ammonia():
    # returns a LargeAmmonia instance
    return w.LargeAmmonia()


@pytest.fixture
def large_greenhouse():
    # returns a LargeGreenhouse instance
    return w.LargeGreenhouse()


@pytest.fixture
def large_garden():
    # returns a LargeGarden instance
    return w.LargeGarden()


@pytest.fixture
def large_ice():
    # returns a LargeIce instance
    return w.LargeIce()


@pytest.fixture
def large_ocean():
    # returns a LargeOcean instance
    return w.LargeOcean()


@pytest.fixture
def large_ice():
    # returns a LargeIce instance
    return w.LargeIce()


@pytest.fixture
def standard_garden():
    # returns a StandardGarden instance
    return w.StandardGarden()


@pytest.fixture
def standard_greenhouse():
    # returns a StandardGreenhouse instance
    return w.StandardGreenhouse()


@pytest.fixture
def standard_ammonia():
    # returns a StandardAmmonia instance
    return w.StandardAmmonia()


def test_set_density_raises_exception_on_no_range(asteroid_belt):
    with pytest.raises(AttributeError):
        asteroid_belt.density = np.nan


def test_set_temperature_raises_exception_on_nan(asteroid_belt):
    with pytest.raises(ValueError):
        asteroid_belt.temperature = np.nan


def test_set_temperature_raises_exception_on_out_of_range(asteroid_belt):
    with pytest.raises(ValueError):
        asteroid_belt.temperature = 100


def test_set_hydrosphere_raises_exception_on_no_range(asteroid_belt):
    with pytest.raises(AttributeError):
        asteroid_belt.hydrosphere = np.nan


def test_set_volatile_mass_raises_exception_on_no_range(asteroid_belt):
    with pytest.raises(AttributeError):
        asteroid_belt.diameter = np.nan


def test_set_diameter_raises_exception_on_no_range(asteroid_belt):
    with pytest.raises(AttributeError):
        asteroid_belt.volatile_mass = np.nan


def test_set_marginal_chlorine_or_fluorine(standard_garden):
    standard_garden.atmosphere.make_marginal(w.chlorine_or_fluorine)
    assert issubclass(type(standard_garden.atmosphere), Marginal)
    assert (standard_garden.atmosphere.toxicity ==
            w.Model.Range(w.Atmosphere.Toxicity.HIGH,
                          w.Atmosphere.Toxicity.LETHAL))
    assert standard_garden.atmosphere.corrosive


def test_set_marginal_high_carbon_dioxyde(standard_garden):
    standard_garden.atmosphere.make_marginal(w.high_carbon_dioxide)
    assert issubclass(type(standard_garden.atmosphere), Marginal)
    assert (standard_garden.atmosphere.toxicity ==
            w.Model.Range(None, w.Atmosphere.Toxicity.MILD))
    assert (standard_garden.atmosphere.pressure_category ==
            w.Atmosphere.Pressure.VERY_DENSE)


def test_set_marginal_high_oxygen(standard_garden):
    categories = sorted(list(w.Atmosphere.Pressure),  key=lambda x: x.value)
    p_id = categories.index(standard_garden.atmosphere.pressure_category)
    standard_garden.atmosphere.make_marginal(w.high_oxygen)
    assert issubclass(type(standard_garden.atmosphere), Marginal)
    assert (standard_garden.atmosphere.toxicity ==
            w.Model.Range(None, w.Atmosphere.Toxicity.MILD))
    m_p_id = categories.index(standard_garden.atmosphere.pressure_category)
    assert (m_p_id in [p_id + 1, len(categories) - 1])


def test_set_marginal_low_oxygen(standard_garden):
    categories = sorted(list(w.Atmosphere.Pressure), key=lambda x: x.value)
    p_id = categories.index(standard_garden.atmosphere.pressure_category)
    standard_garden.atmosphere.make_marginal(w.low_oxygen)
    assert issubclass(type(standard_garden.atmosphere), Marginal)
    m_p_id = categories.index(standard_garden.atmosphere.pressure_category)
    assert (m_p_id in [p_id - 1, 0])


def test_set_marginal_nitrogen_compounds(standard_garden):
    standard_garden.atmosphere.make_marginal(w.nitrogen_compounds)
    assert issubclass(type(standard_garden.atmosphere), Marginal)
    assert (standard_garden.atmosphere.toxicity ==
            w.Atmosphere.Range(w.Atmosphere.Toxicity.MILD,
                             w.Atmosphere.Toxicity.HIGH))


def test_set_marginal_sulfur_compounds(standard_garden):
    standard_garden.atmosphere.make_marginal(w.sulfur_compounds)
    assert issubclass(type(standard_garden.atmosphere), Marginal)
    assert (standard_garden.atmosphere.toxicity ==
            w.Atmosphere.Range(w.Atmosphere.Toxicity.MILD,
                             w.Atmosphere.Toxicity.HIGH))


def test_set_marginal_organic_toxins(standard_garden):
    standard_garden.atmosphere.make_marginal(w.organic_toxins)
    assert issubclass(type(standard_garden.atmosphere), Marginal)
    assert (standard_garden.atmosphere.toxicity ==
            w.Atmosphere.Range(w.Atmosphere.Toxicity.MILD,
                             w.Atmosphere.Toxicity.LETHAL))


def test_set_marginal_pollutants(standard_garden):
    standard_garden.atmosphere.make_marginal(w.pollutants)
    assert issubclass(type(standard_garden.atmosphere), Marginal)
    assert (standard_garden.atmosphere.toxicity == w.Atmosphere.Toxicity.MILD)


def test_get_size_is_None(asteroid_belt):
    assert asteroid_belt.size is None


def test_get_size(large_ammonia):
    assert large_ammonia.size == w.World.Size.LARGE


def test_get_core_is_None(asteroid_belt):
    assert asteroid_belt.core is None


def test_get_core(large_ammonia):
    assert large_ammonia.core == w.World.Core.ICY_CORE


def test_get_hydrosphere_is_nan(asteroid_belt):
    assert np.isnan(asteroid_belt.hydrosphere)


def test_get_hydrosphere(large_ammonia):
    assert (large_ammonia.hydrosphere >= .2 and
            large_ammonia.hydrosphere <= 1)


def test_get_diameter_is_nan(asteroid_belt):
    assert np.isnan(asteroid_belt.diameter)


def test_get_atmosphere_is_None(asteroid_belt):
    assert asteroid_belt.atmosphere is None


def test_get_atmosphere(large_ammonia):
    assert large_ammonia.atmosphere.composition == ['He', 'NH3', 'CH4']
    assert large_ammonia.atmosphere.toxicity == w.Atmosphere.Toxicity.LETHAL
    assert large_ammonia.atmosphere.suffocating is True
    assert large_ammonia.atmosphere.corrosive is True


def test_get_atmosphere(large_greenhouse):
    assert ((large_greenhouse.hydrosphere < .1 and
             large_greenhouse.atmosphere.composition == ['CO2']) or
            (large_greenhouse.hydrosphere >= .1 and
             large_greenhouse.atmosphere.composition == ['N2', 'H2O', 'O2']))
    assert large_greenhouse.atmosphere.toxicity == w.Atmosphere.Toxicity.LETHAL
    assert large_greenhouse.atmosphere.suffocating is True
    assert large_greenhouse.atmosphere.corrosive is True


def test_get_atmosphere(large_ice):
    assert large_ice.atmosphere.composition == ['He', 'N2']
    assert large_ice.atmosphere.toxicity == w.Atmosphere.Toxicity.HIGH
    assert large_ice.atmosphere.suffocating is True


def test_get_atmosphere(large_ocean):
    assert large_ocean.atmosphere.composition == ['He', 'N2']
    assert large_ocean.atmosphere.toxicity == w.Atmosphere.Toxicity.HIGH
    assert large_ocean.atmosphere.suffocating is True


def test_get_atmosphere(standard_greenhouse):
    assert ((standard_greenhouse.hydrosphere < .1 and
             standard_greenhouse.atmosphere.composition == ['CO2']) or
            (standard_greenhouse.hydrosphere >= .1 and
             (standard_greenhouse.atmosphere.composition ==
              ['N2', 'H2O', 'O2'])))
    assert (standard_greenhouse.atmosphere.toxicity ==
            w.Atmosphere.Toxicity.LETHAL)
    assert standard_greenhouse.atmosphere.suffocating is True
    assert standard_greenhouse.atmosphere.corrosive is True


def test_get_atmosphere(standard_ammonia):
    assert standard_ammonia.atmosphere.composition == ['N2', 'NH3', 'CH4']
    assert standard_ammonia.atmosphere.toxicity == w.Atmosphere.Toxicity.LETHAL
    assert standard_ammonia.atmosphere.suffocating is True
    assert standard_ammonia.atmosphere.corrosive is True


def test_get_pressure_factor_is_nan(asteroid_belt):
    assert np.isnan(asteroid_belt.pressure_factor)


def test_get_pressure_factor(large_ammonia):
    assert large_ammonia.pressure_factor == 5


def test_get_greenhouse_factor_is_nan(asteroid_belt):
    assert np.isnan(asteroid_belt.greenhouse_factor)


def test_get_greenhouse_factor(large_ammonia):
    assert large_ammonia.greenhouse_factor == .2


def test_get_volatile_mass_is_nan(asteroid_belt):
    assert np.isnan(asteroid_belt.volatile_mass)


def test_get_volatile_mass(large_ammonia):
    assert (large_ammonia.volatile_mass >= .3 and
            large_ammonia.volatile_mass <= 1.8)


def test_get_absorption(asteroid_belt):
    assert asteroid_belt.absorption == .97


def test_get_absorption(large_garden):
    assert ((large_garden.hydrosphere < .2 and
             large_garden.absorption >= .95) or
            (large_garden.hydrosphere < .5 and
             large_garden.absorption >= .92) or
            (large_garden.hydrosphere < .90 and
             large_garden.absorption >= .88) or
            large_garden.absorption >= .84)


def test_get_gravity_is_nan(asteroid_belt):
    assert np.isnan(asteroid_belt.gravity)


def test_get_mass_is_nan(asteroid_belt):
    assert np.isnan(asteroid_belt.mass)


def test_get_atmosphere_is_None(asteroid_belt):
    assert asteroid_belt.atmosphere is None


def test_get_temperature(asteroid_belt):
    assert (asteroid_belt.temperature >= 140 and
            asteroid_belt.temperature <= 500)


def test_get_blackbody_temperature(asteroid_belt):
    assert (asteroid_belt.blackbody_temperature == asteroid_belt.temperature /
            .97)


def test_get_climate(asteroid_belt):
    lower = asteroid_belt.climate
    upper = np.inf
    for item in w.World.Climate:
        if item > lower:
            upper = item
    assert (asteroid_belt.temperature >= lower and
            asteroid_belt.temperature <= upper)


def test_get_pressure_category(large_ammonia):
    lower = large_ammonia.atmosphere.pressure_category
    upper = np.inf
    for item in w.Atmosphere.Pressure:
        if item > lower:
            upper = item
    assert (large_ammonia.atmosphere.pressure >= lower and
            large_ammonia.atmosphere.pressure <= upper)
