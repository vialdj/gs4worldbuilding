import pytest
import numpy as np

from .context import worldgen
from worldgen.world import World, AsteroidBelt


@pytest.fixture
def asteroid_belt():
    # returns an AsteroidBelt instance
    return AsteroidBelt()


def test_set_density_raises_exception_on_attribute_error(asteroid_belt):
    with pytest.raises(AttributeError):
        asteroid_belt.density = .0


def test_set_temperature_raises_exception_on_value_error(asteroid_belt):
    with pytest.raises(ValueError):
        asteroid_belt.temperature = .0


def test_set_hydrosphere_raises_exception_on_attribute_error(asteroid_belt):
    with pytest.raises(AttributeError):
        asteroid_belt.hydrosphere = .0


def test_set_volatile_mass_raises_exception_on_attribute_error(asteroid_belt):
    with pytest.raises(AttributeError):
        asteroid_belt.diameter = .0


def test_set_diameter_raises_exception_on_attribute_error(asteroid_belt):
    with pytest.raises(AttributeError):
        asteroid_belt.volatile_mass = .0


def test_get_core_is_None(asteroid_belt):
    assert asteroid_belt.core is None


def test_get_hydrosphere_is_nan(asteroid_belt):
    assert np.isnan(asteroid_belt.hydrosphere)


def test_get_diameter_is_nan(asteroid_belt):
    assert np.isnan(asteroid_belt.diameter)


def test_get_pressure_factor_is_nan(asteroid_belt):
    assert np.isnan(asteroid_belt.pressure_factor)


def test_get_greenhouse_factor_is_nan(asteroid_belt):
    assert np.isnan(asteroid_belt.greenhouse_factor)


def test_get_volatile_mass_is_nan(asteroid_belt):
    assert np.isnan(asteroid_belt.volatile_mass)


def test_get_absorption_equals_class_variable(asteroid_belt):
    assert asteroid_belt.absorption == AsteroidBelt._absorption


def test_get_gravity_is_nan(asteroid_belt):
    assert np.isnan(asteroid_belt.gravity)


def test_get_mass_is_nan(asteroid_belt):
    assert np.isnan(asteroid_belt.mass)


def test_get_pressure_is_nan(asteroid_belt):
    assert np.isnan(asteroid_belt.pressure)


def test_get_temperature_is_valid(asteroid_belt):
    assert (asteroid_belt.temperature >= AsteroidBelt._temperature_range.min and
            asteroid_belt.temperature <= AsteroidBelt._temperature_range.max)


def test_get_blackbody_temperature_is_valid(asteroid_belt):
    assert (asteroid_belt.blackbody_temperature == asteroid_belt.temperature /
            AsteroidBelt._absorption)


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
