import pytest
import numpy as np

from .context import worldgen
from worldgen.world import World, LargeAmmonia, AsteroidBelt


@pytest.fixture
def asteroid_belt():
    # returns an AsteroidBelt instance
    return AsteroidBelt()


@pytest.fixture
def large_ammonia():
    # returns a LargeAmmonia instance
    return LargeAmmonia()


def test_set_density_raises_exception_on_attribute_error(asteroid_belt):
    with pytest.raises(AttributeError):
        asteroid_belt.density = np.nan


def test_set_temperature_raises_exception_on_value_error(asteroid_belt):
    with pytest.raises(ValueError):
        asteroid_belt.temperature = np.nan


def test_set_hydrosphere_raises_exception_on_attribute_error(asteroid_belt):
    with pytest.raises(AttributeError):
        asteroid_belt.hydrosphere = np.nan


def test_set_volatile_mass_raises_exception_on_attribute_error(asteroid_belt):
    with pytest.raises(AttributeError):
        asteroid_belt.diameter = np.nan


def test_set_diameter_raises_exception_on_attribute_error(asteroid_belt):
    with pytest.raises(AttributeError):
        asteroid_belt.volatile_mass = np.nan


def test_get_size_is_None(asteroid_belt):
    assert asteroid_belt.size is None


def test_get_size_is_valid(large_ammonia):
    assert large_ammonia.size == World.Size.LARGE


def test_get_core_is_None(asteroid_belt):
    assert asteroid_belt.core is None


def test_get_core_is_valid(large_ammonia):
    assert large_ammonia.core == World.Core.ICY_CORE


def test_get_hydrosphere_is_nan(asteroid_belt):
    assert np.isnan(asteroid_belt.hydrosphere)


def test_get_hydrosphere_is_valid(large_ammonia):
    assert (large_ammonia.hydrosphere >= .2 and
            large_ammonia.hydrosphere <= 1)


def test_get_diameter_is_nan(asteroid_belt):
    assert np.isnan(asteroid_belt.diameter)


def test_get_atmosphere_is_None(asteroid_belt):
    assert asteroid_belt.atmosphere is None


def test_get_atmosphere_is_valid(large_ammonia):
    assert large_ammonia.atmosphere == ['He', 'NH3', 'CH4']


def test_get_pressure_factor_is_nan(asteroid_belt):
    assert np.isnan(asteroid_belt.pressure_factor)


def test_get_pressure_factor_is_valid(large_ammonia):
    assert large_ammonia.pressure_factor == 5


def test_get_greenhouse_factor_is_nan(asteroid_belt):
    assert np.isnan(asteroid_belt.greenhouse_factor)


def test_get_greenhouse_factor_is_valid(large_ammonia):
    assert large_ammonia.greenhouse_factor == .2


def test_get_volatile_mass_is_nan(asteroid_belt):
    assert np.isnan(asteroid_belt.volatile_mass)


def test_get_volatile_mass_is_valid(large_ammonia):
    assert (large_ammonia.volatile_mass >= .3 and
            large_ammonia.volatile_mass <= 1.8)


def test_get_absorption_is_valid(asteroid_belt):
    assert asteroid_belt.absorption == .97


def test_get_gravity_is_nan(asteroid_belt):
    assert np.isnan(asteroid_belt.gravity)


def test_get_mass_is_nan(asteroid_belt):
    assert np.isnan(asteroid_belt.mass)


def test_get_pressure_is_nan(asteroid_belt):
    assert np.isnan(asteroid_belt.pressure)


def test_get_temperature_is_valid(asteroid_belt):
    assert (asteroid_belt.temperature >= 140 and
            asteroid_belt.temperature <= 500)


def test_get_blackbody_temperature_is_valid(asteroid_belt):
    assert (asteroid_belt.blackbody_temperature == asteroid_belt.temperature /
            .97)


def test_get_climate_is_valid(asteroid_belt):
    lower = asteroid_belt.climate.value
    upper = np.inf
    for item in World.Climate:
        if item.value > lower:
            upper = item.value
    assert (asteroid_belt.temperature >= lower and
            asteroid_belt.temperature <= upper)


def test_get_pressure_category_is_None(asteroid_belt):
    assert asteroid_belt.pressure_category is None


def test_get_pressure_category_is_valid(large_ammonia):
    lower = large_ammonia.pressure_category.value
    upper = np.inf
    for item in World.Atmosphere:
        if item.value > lower:
            upper = item.value
    assert (large_ammonia.pressure >= lower and
            large_ammonia.pressure <= upper)
