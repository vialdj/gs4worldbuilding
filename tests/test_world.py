import worldgen.world as w
from worldgen import units
from worldgen.model.bounds import ValueBounds

from worldgen.world.marginal_atmosphere import Marginal

import pytest
import numpy as np
from astropy import units as u

@pytest.fixture
def asteroid_belt():
    # returns an AsteroidBelt instance
    return w.AsteroidBelt()


@pytest.fixture
def standard_garden():
    # returns a StandardGarden instance
    return w.StandardGarden()


@pytest.fixture
def large_garden():
    # returns a LargeGarden instance
    return w.LargeGarden()


@pytest.fixture
def standard_greenhouse():
    # returns a StandardGreenhouse instance
    return w.StandardGreenhouse()


@pytest.fixture
def large_greenhouse():
    # returns a LargeGreenhouse instance
    return w.LargeGreenhouse()


@pytest.fixture
def standard_ammonia():
    # returns a StandardAmmonia instance
    return w.StandardAmmonia()


@pytest.fixture
def large_ammonia():
    # returns a LargeAmmonia instance
    return w.LargeAmmonia()


@pytest.fixture
def standard_ocean():
    # returns a StandardOcean instance
    return w.StandardOcean()


@pytest.fixture
def large_ocean():
    # returns a LargeOcean instance
    return w.LargeOcean()


@pytest.fixture
def tiny_ice():
    # returns a TinyIce instance
    return w.TinyIce()


@pytest.fixture
def small_ice():
    # returns a SmallIce instance
    return w.SmallIce()


@pytest.fixture
def standard_ice():
    # returns a StandardIce instance
    return w.StandardIce()


@pytest.fixture
def large_ice():
    # returns a LargeIce instance
    return w.LargeIce()


@pytest.fixture
def standard_chthonian():
    # returns a StandardChthonian instance
    return w.StandardChthonian()


@pytest.fixture
def large_chthonian():
    # returns a LargeChthonian instance
    return w.LargeChthonian()


@pytest.fixture
def small_hadean():
    # returns a SmallHadean instance
    return w.SmallHadean()


@pytest.fixture
def standard_hadean():
    # returns a StandardHadean instance
    return w.StandardHadean()


@pytest.fixture
def tiny_rock():
    # returns a TinyRock instance
    return w.TinyRock()


@pytest.fixture
def small_rock():
    # returns a SmallRock instance
    return w.SmallRock()


@pytest.fixture
def tiny_sulfur():
    # returns a TinySulfur instance
    return w.TinySulfur()


# Tests on exceptions raises

def test_set_density_raises_exception_on_no_bounds(asteroid_belt):
    with pytest.raises(AttributeError):
        asteroid_belt.density = np.nan


def test_set_temperature_raises_exception_on_nan(asteroid_belt):
    with pytest.raises(ValueError):
        asteroid_belt.temperature = np.nan


def test_set_temperature_raises_exception_on_out_of_bounds(asteroid_belt):
    with pytest.raises(ValueError):
        asteroid_belt.temperature = 100 * u.K


def test_set_hydrosphere_raises_exception_on_no_bounds(asteroid_belt):
    with pytest.raises(AttributeError):
        asteroid_belt.hydrosphere = np.nan


def test_set_volatile_mass_raises_exception_on_no_bounds(asteroid_belt):
    with pytest.raises(AttributeError):
        asteroid_belt.diameter = 1 * units.D_earth


def test_set_diameter_raises_exception_on_no_bounds(asteroid_belt):
    with pytest.raises(AttributeError):
        asteroid_belt.volatile_mass = np.nan

# Tests on world derived properties

def test_get_blackbody_temperature(standard_garden):
    assert (standard_garden.blackbody_temperature == standard_garden.temperature /
            standard_garden.blackbody_correction)


def test_get_climate(standard_garden):
    lower = standard_garden.climate
    upper = np.inf
    for item in w.World.Climate:
        if item > lower:
            upper = item
    assert (standard_garden.temperature >= lower and
            standard_garden.temperature <= upper)


def test_get_pressure_category(standard_ocean):
    lower = standard_ocean.atmosphere.pressure_category
    upper = np.inf
    for item in w.Atmosphere.Pressure:
        if item > lower:
            upper = item
    assert (standard_ocean.atmosphere.pressure >= lower and
            standard_ocean.atmosphere.pressure <= upper)


# Tests on concrete world instances

def test_asteroid_belt(asteroid_belt):
    assert asteroid_belt.absorption == .97
    assert (asteroid_belt.temperature >= 140 * u.K and
            asteroid_belt.temperature <= 500 * u.K)
    assert asteroid_belt.atmosphere is None
    assert np.isnan(asteroid_belt.mass)
    assert np.isnan(asteroid_belt.gravity)
    assert np.isnan(asteroid_belt.volatile_mass)
    assert np.isnan(asteroid_belt.diameter)
    assert np.isnan(asteroid_belt.hydrosphere)
    assert np.isnan(asteroid_belt.greenhouse_factor)
    assert np.isnan(asteroid_belt.pressure_factor)
    assert asteroid_belt.core is None
    assert asteroid_belt.size is None


def test_tiny_ice(tiny_ice):
    assert tiny_ice.absorption == .86
    assert (tiny_ice.temperature >= 80 * u.K and
            tiny_ice.temperature <= 140 * u.K)
    assert tiny_ice.atmosphere is None
    assert np.isnan(tiny_ice.greenhouse_factor)
    assert np.isnan(tiny_ice.pressure_factor)
    assert np.isnan(tiny_ice.hydrosphere)
    assert np.isnan(tiny_ice.hydrosphere)
    assert tiny_ice.core is w.World.Core.ICY_CORE
    assert tiny_ice.size is w.World.Size.TINY
    assert (tiny_ice.density >= .3 * units.d_earth and
            tiny_ice.density <= .7 * units.d_earth)


def test_small_ice(small_ice):
    assert small_ice.absorption == .93
    assert (small_ice.temperature >= 80 * u.K and
            small_ice.temperature <= 140 * u.K)
    assert small_ice.atmosphere.toxicity in [w.Atmosphere.Toxicity.MILD,
                                             w.Atmosphere.Toxicity.HIGH]
    assert small_ice.atmosphere.composition == ['N2', 'CH4']
    assert small_ice.atmosphere.suffocating is True
    assert small_ice.atmosphere.corrosive is False
    assert small_ice.atmosphere.breathable is False
    assert (small_ice.hydrosphere >= .3 and
            small_ice.hydrosphere <= .8)
    assert small_ice.greenhouse_factor == .10
    assert small_ice.pressure_factor == 10
    assert small_ice.core is w.World.Core.ICY_CORE
    assert small_ice.size is w.World.Size.SMALL
    assert (small_ice.density >= .3 * units.d_earth and
            small_ice.density <= .7 * units.d_earth)


def test_standard_ice(standard_ice):
    assert standard_ice.absorption == .86
    assert (standard_ice.temperature >= 80 * u.K and
            standard_ice.temperature <= 230 * u.K)
    assert standard_ice.atmosphere.toxicity in [None,
                                                w.Atmosphere.Toxicity.MILD]
    assert standard_ice.atmosphere.composition == ['CO2', 'N2']
    assert standard_ice.atmosphere.suffocating is True
    assert standard_ice.atmosphere.corrosive is False
    assert standard_ice.atmosphere.breathable is False
    assert (standard_ice.hydrosphere >= 0 and
            standard_ice.hydrosphere <= .2)
    assert standard_ice.greenhouse_factor == .20
    assert standard_ice.pressure_factor == 1
    assert standard_ice.core is w.World.Core.LARGE_IRON_CORE
    assert standard_ice.size is w.World.Size.STANDARD
    assert (standard_ice.density >= .8 * units.d_earth and
            standard_ice.density <= 1.2 * units.d_earth)


def test_large_ice(large_ice):
    assert large_ice.absorption == .86
    assert (large_ice.temperature >= 80 * u.K and
            large_ice.temperature <= 230 * u.K)
    assert large_ice.atmosphere.toxicity == w.Atmosphere.Toxicity.HIGH
    assert large_ice.atmosphere.composition == ['He', 'N2']
    assert large_ice.atmosphere.suffocating is True
    assert large_ice.atmosphere.corrosive is False
    assert large_ice.atmosphere.breathable is False
    assert (large_ice.hydrosphere >= 0 and
            large_ice.hydrosphere <= .2)
    assert large_ice.greenhouse_factor == .20
    assert large_ice.pressure_factor == 5
    assert large_ice.core is w.World.Core.LARGE_IRON_CORE
    assert large_ice.size is w.World.Size.LARGE
    assert (large_ice.density >= .8 * units.d_earth and
            large_ice.density <= 1.2 * units.d_earth)


def test_standard_greenhouse(standard_greenhouse):
    assert standard_greenhouse.absorption == .77
    assert (standard_greenhouse.temperature >= 500 * u.K and
            standard_greenhouse.temperature <= 950 * u.K)
    assert (standard_greenhouse.atmosphere.toxicity ==
            w.Atmosphere.Toxicity.LETHAL)
    assert ((standard_greenhouse.hydrosphere < .1 and
             standard_greenhouse.atmosphere.composition == ['CO2']) or
            (standard_greenhouse.hydrosphere >= .1 and
             (standard_greenhouse.atmosphere.composition ==
              ['N2', 'H2O', 'O2'])))
    assert standard_greenhouse.atmosphere.suffocating is True
    assert standard_greenhouse.atmosphere.corrosive is True
    assert standard_greenhouse.atmosphere.breathable is False
    assert (standard_greenhouse.hydrosphere >= 0 and
            standard_greenhouse.hydrosphere <= .5)
    assert standard_greenhouse.greenhouse_factor == 2
    assert standard_greenhouse.pressure_factor == 100
    assert standard_greenhouse.core is w.World.Core.LARGE_IRON_CORE
    assert standard_greenhouse.size is w.World.Size.STANDARD
    assert (standard_greenhouse.density >= .8 * units.d_earth and
            standard_greenhouse.density <= 1.2 * units.d_earth)


def test_large_greenhouse(large_greenhouse):
    assert large_greenhouse.absorption == .77
    assert (large_greenhouse.temperature >= 500 * u.K and
            large_greenhouse.temperature <= 950 * u.K)
    assert (large_greenhouse.atmosphere.toxicity ==
            w.Atmosphere.Toxicity.LETHAL)
    assert ((large_greenhouse.hydrosphere < .1 and
             large_greenhouse.atmosphere.composition == ['CO2']) or
            (large_greenhouse.hydrosphere >= .1 and
             large_greenhouse.atmosphere.composition == ['N2', 'H2O', 'O2']))
    assert large_greenhouse.atmosphere.toxicity == w.Atmosphere.Toxicity.LETHAL
    assert large_greenhouse.atmosphere.suffocating is True
    assert large_greenhouse.atmosphere.corrosive is True
    assert large_greenhouse.atmosphere.breathable is False
    assert (large_greenhouse.hydrosphere >= 0 and
            large_greenhouse.hydrosphere <= .5)
    assert large_greenhouse.greenhouse_factor == 2
    assert large_greenhouse.pressure_factor == 500
    assert large_greenhouse.core is w.World.Core.LARGE_IRON_CORE
    assert large_greenhouse.size is w.World.Size.LARGE
    assert (large_greenhouse.density >= .8 * units.d_earth and
            large_greenhouse.density <= 1.2 * units.d_earth)


def test_standard_ocean(standard_ocean):
    assert ((standard_ocean.hydrosphere < .2 and
             standard_ocean.absorption >= .95) or
            (standard_ocean.hydrosphere < .5 and
             standard_ocean.absorption >= .92) or
            (standard_ocean.hydrosphere < .90 and
             standard_ocean.absorption >= .88) or
            standard_ocean.absorption >= .84)
    assert (standard_ocean.temperature >= 250 * u.K and
            standard_ocean.temperature <= 340 * u.K)
    assert standard_ocean.atmosphere.toxicity in [None,
                                                  w.Atmosphere.Toxicity.MILD]
    assert standard_ocean.atmosphere.composition == ['CO2', 'N2']
    assert standard_ocean.atmosphere.suffocating is True
    assert standard_ocean.atmosphere.corrosive is False
    assert standard_ocean.atmosphere.breathable is False
    assert (standard_ocean.hydrosphere >= .5 and
            standard_ocean.hydrosphere <= 1)
    assert standard_ocean.greenhouse_factor == .16
    assert standard_ocean.pressure_factor == 1
    assert standard_ocean.core is w.World.Core.LARGE_IRON_CORE
    assert standard_ocean.size is w.World.Size.STANDARD
    assert (standard_ocean.density >= .8 * units.d_earth and
            standard_ocean.density <= 1.2 * units.d_earth)


def test_large_ocean(large_ocean):
    assert ((large_ocean.hydrosphere < .2 and
             large_ocean.absorption >= .95) or
            (large_ocean.hydrosphere < .5 and
             large_ocean.absorption >= .92) or
            (large_ocean.hydrosphere < .90 and
             large_ocean.absorption >= .88) or
            large_ocean.absorption >= .84)
    assert (large_ocean.temperature >= 250 * u.K and
            large_ocean.temperature <= 340 * u.K)
    assert large_ocean.atmosphere.toxicity == w.Atmosphere.Toxicity.HIGH
    assert large_ocean.atmosphere.composition == ['He', 'N2']
    assert large_ocean.atmosphere.suffocating is True
    assert large_ocean.atmosphere.corrosive is False
    assert large_ocean.atmosphere.breathable is False
    assert (large_ocean.hydrosphere >= .7 and
            large_ocean.hydrosphere <= 1)
    assert large_ocean.greenhouse_factor == .16
    assert large_ocean.pressure_factor == 5
    assert large_ocean.core is w.World.Core.LARGE_IRON_CORE
    assert large_ocean.size is w.World.Size.LARGE
    assert (large_ocean.density >= .8 * units.d_earth and
            large_ocean.density <= 1.2 * units.d_earth)


def test_standard_ammonia(standard_ammonia):
    assert standard_ammonia.absorption == .84
    assert (standard_ammonia.temperature >= 140 * u.K and
            standard_ammonia.temperature <= 215 * u.K)
    assert standard_ammonia.atmosphere.toxicity == w.Atmosphere.Toxicity.LETHAL
    assert standard_ammonia.atmosphere.composition == ['N2', 'NH3', 'CH4']
    assert standard_ammonia.atmosphere.suffocating is True
    assert standard_ammonia.atmosphere.corrosive is True
    assert standard_ammonia.atmosphere.breathable is False
    assert (standard_ammonia.hydrosphere >= .2 and
            standard_ammonia.hydrosphere <= 1)
    assert standard_ammonia.greenhouse_factor == .2
    assert standard_ammonia.pressure_factor == 1
    assert standard_ammonia.core is w.World.Core.ICY_CORE
    assert standard_ammonia.size is w.World.Size.STANDARD
    assert (standard_ammonia.density >= .3 * units.d_earth and
            standard_ammonia.density <= .7 * units.d_earth)


def test_large_ammonia(large_ammonia):
    assert large_ammonia.absorption == .84
    assert (large_ammonia.temperature >= 140 * u.K and
            large_ammonia.temperature <= 215 * u.K)
    assert large_ammonia.atmosphere.toxicity == w.Atmosphere.Toxicity.LETHAL
    assert large_ammonia.atmosphere.composition == ['He', 'NH3', 'CH4']
    assert large_ammonia.atmosphere.suffocating is True
    assert large_ammonia.atmosphere.corrosive is True
    assert large_ammonia.atmosphere.breathable is False
    assert (large_ammonia.hydrosphere >= .2 and
            large_ammonia.hydrosphere <= 1)
    assert large_ammonia.greenhouse_factor == .2
    assert large_ammonia.pressure_factor == 5
    assert large_ammonia.core == w.World.Core.ICY_CORE
    assert large_ammonia.size == w.World.Size.LARGE
    assert (large_ammonia.density >= .3 * units.d_earth and
            large_ammonia.density <= .7 * units.d_earth)


def test_standard_garden(standard_garden):
    assert ((standard_garden.hydrosphere < .2 and
             standard_garden.absorption >= .95) or
            (standard_garden.hydrosphere < .5 and
             standard_garden.absorption >= .92) or
            (standard_garden.hydrosphere < .90 and
             standard_garden.absorption >= .88) or
            standard_garden.absorption >= .84)
    assert (standard_garden.temperature >= 250 * u.K and
            standard_garden.temperature <= 340 * u.K)
    standard_garden.atmosphere.remove_marginal()
    assert standard_garden.atmosphere.toxicity is None
    assert standard_garden.atmosphere.composition == ['N2', 'O2']
    assert standard_garden.atmosphere.suffocating is False
    assert standard_garden.atmosphere.corrosive is False
    assert standard_garden.atmosphere.breathable is True
    assert (standard_garden.hydrosphere >= .5 and
            standard_garden.hydrosphere <= 1)
    assert standard_garden.greenhouse_factor == .16
    assert standard_garden.pressure_factor == 1
    assert standard_garden.core == w.World.Core.LARGE_IRON_CORE
    assert standard_garden.size == w.World.Size.STANDARD
    assert (standard_garden.density >= .8 * units.d_earth and
            standard_garden.density <= 1.2 * units.d_earth)


def test_large_garden(large_garden):
    assert ((large_garden.hydrosphere < .2 and
             large_garden.absorption >= .95) or
            (large_garden.hydrosphere < .5 and
             large_garden.absorption >= .92) or
            (large_garden.hydrosphere < .90 and
             large_garden.absorption >= .88) or
            large_garden.absorption >= .84)
    assert (large_garden.temperature >= 250 * u.K and
            large_garden.temperature <= 340 * u.K)
    large_garden.atmosphere.remove_marginal()
    assert large_garden.atmosphere.toxicity is None
    assert large_garden.atmosphere.composition == ['N2', 'O2', 'He', 'Ne',
                                                   'Ar', 'Kr', 'Xe']
    assert large_garden.atmosphere.suffocating is False
    assert large_garden.atmosphere.corrosive is False
    assert large_garden.atmosphere.breathable is True
    assert (large_garden.hydrosphere >= .7 and
            large_garden.hydrosphere <= 1)
    assert large_garden.greenhouse_factor == .16
    assert large_garden.pressure_factor == 5
    assert large_garden.core == w.World.Core.LARGE_IRON_CORE
    assert large_garden.size == w.World.Size.LARGE
    assert (large_garden.density >= .8 * units.d_earth and
            large_garden.density <= 1.2 * units.d_earth)


def test_standard_chthonian(standard_chthonian):
    assert standard_chthonian.absorption == .97
    assert (standard_chthonian.temperature >= 500 * u.K and
            standard_chthonian.temperature <= 950 * u.K)
    assert standard_chthonian.atmosphere is None
    assert np.isnan(standard_chthonian.greenhouse_factor)
    assert np.isnan(standard_chthonian.pressure_factor)
    assert np.isnan(standard_chthonian.hydrosphere)
    assert standard_chthonian.core == w.World.Core.LARGE_IRON_CORE
    assert standard_chthonian.size == w.World.Size.STANDARD
    assert (standard_chthonian.density >= .8 * units.d_earth and
            standard_chthonian.density <= 1.2 * units.d_earth)


def test_large_chthonian(large_chthonian):
    assert large_chthonian.absorption == .97
    assert (large_chthonian.temperature >= 500 * u.K and
            large_chthonian.temperature <= 950 * u.K)
    assert large_chthonian.atmosphere is None
    assert np.isnan(large_chthonian.greenhouse_factor)
    assert np.isnan(large_chthonian.pressure_factor)
    assert np.isnan(large_chthonian.hydrosphere)
    assert large_chthonian.core == w.World.Core.LARGE_IRON_CORE
    assert large_chthonian.size == w.World.Size.LARGE
    assert (large_chthonian.density >= .8 * units.d_earth and
            large_chthonian.density <= 1.2 * units.d_earth)


def test_small_hadean(small_hadean):
    assert small_hadean.absorption == .67
    assert (small_hadean.temperature >= 50 * u.K and
            small_hadean.temperature <= 80 * u.K)
    assert small_hadean.atmosphere is None
    assert np.isnan(small_hadean.greenhouse_factor)
    assert np.isnan(small_hadean.pressure_factor)
    assert np.isnan(small_hadean.hydrosphere)
    assert small_hadean.core == w.World.Core.ICY_CORE
    assert small_hadean.size == w.World.Size.SMALL
    assert (small_hadean.density >= .3 * units.d_earth and
            small_hadean.density <= .7 * units.d_earth)


def test_standard_hadean(standard_hadean):
    assert standard_hadean.absorption == .67
    assert (standard_hadean.temperature >= 50 * u.K and
            standard_hadean.temperature <= 80 * u.K)
    assert standard_hadean.atmosphere is None
    assert np.isnan(standard_hadean.greenhouse_factor)
    assert np.isnan(standard_hadean.pressure_factor)
    assert np.isnan(standard_hadean.hydrosphere)
    assert standard_hadean.core == w.World.Core.ICY_CORE
    assert standard_hadean.size == w.World.Size.STANDARD
    assert (standard_hadean.density >= .3 * units.d_earth and
            standard_hadean.density <= .7 * units.d_earth)


def test_tiny_rock(tiny_rock):
    assert tiny_rock.absorption == .97
    assert (tiny_rock.temperature >= 140 * u.K and
            tiny_rock.temperature <= 500 * u.K)
    assert tiny_rock.atmosphere is None
    assert np.isnan(tiny_rock.greenhouse_factor)
    assert np.isnan(tiny_rock.pressure_factor)
    assert np.isnan(tiny_rock.hydrosphere)
    assert tiny_rock.core == w.World.Core.SMALL_IRON_CORE
    assert tiny_rock.size == w.World.Size.TINY
    assert (tiny_rock.density >= .6 * units.d_earth and
            tiny_rock.density <= 1 * units.d_earth)


def test_small_rock(small_rock):
    assert small_rock.absorption == .96
    assert (small_rock.temperature >= 140 * u.K and
            small_rock.temperature <= 500 * u.K)
    assert small_rock.atmosphere is None
    assert np.isnan(small_rock.greenhouse_factor)
    assert np.isnan(small_rock.pressure_factor)
    assert np.isnan(small_rock.hydrosphere)
    assert small_rock.core == w.World.Core.SMALL_IRON_CORE
    assert small_rock.size == w.World.Size.SMALL
    assert (small_rock.density >= .6 * units.d_earth and
            small_rock.density <= 1 * units.d_earth)


def test_tiny_sulfur(tiny_sulfur):
    assert tiny_sulfur.absorption == .77
    assert (tiny_sulfur.temperature >= 80 * u.K and
            tiny_sulfur.temperature <= 140 * u.K)
    assert tiny_sulfur.atmosphere is None
    assert np.isnan(tiny_sulfur.greenhouse_factor)
    assert np.isnan(tiny_sulfur.pressure_factor)
    assert np.isnan(tiny_sulfur.hydrosphere)
    assert tiny_sulfur.core == w.World.Core.ICY_CORE
    assert tiny_sulfur.size == w.World.Size.TINY
    assert (tiny_sulfur.density >= .3 * units.d_earth and
            tiny_sulfur.density <= .7 * units.d_earth)


# Tests on marginal atmosphere modifiers

def test_set_marginal_chlorine_or_fluorine(standard_garden):
    standard_garden.atmosphere.make_marginal(w.chlorine_or_fluorine)
    assert issubclass(type(standard_garden.atmosphere), Marginal)
    assert (standard_garden.atmosphere.toxicity == ValueBounds(
                w.Atmosphere.Toxicity.HIGH,
                w.Atmosphere.Toxicity.LETHAL))
    assert standard_garden.atmosphere.corrosive


def test_set_marginal_high_carbon_dioxyde(standard_garden):
    standard_garden.atmosphere.make_marginal(w.high_carbon_dioxide)
    assert issubclass(type(standard_garden.atmosphere), Marginal)
    assert (standard_garden.atmosphere.toxicity == ValueBounds(
                w.Atmosphere.Toxicity.NONE,
                w.Atmosphere.Toxicity.MILD))
    assert (standard_garden.atmosphere.pressure_category ==
            w.Atmosphere.Pressure.VERY_DENSE)


def test_set_marginal_high_oxygen(standard_garden):
    categories = sorted(list(w.Atmosphere.Pressure), key=lambda x: x.value)
    standard_garden.atmosphere.make_marginal(w.high_oxygen)
    assert issubclass(type(standard_garden.atmosphere), Marginal)
    assert (standard_garden.atmosphere.toxicity == ValueBounds(
                w.Atmosphere.Toxicity.NONE,
                w.Atmosphere.Toxicity.MILD
            ))
    p_id = categories.index(standard_garden.atmosphere.base.pressure_category)
    m_p_id = categories.index(standard_garden.atmosphere.pressure_category)
    assert (m_p_id in [p_id + 1, len(categories) - 1])


def test_set_marginal_low_oxygen(standard_garden):
    categories = sorted(list(w.Atmosphere.Pressure), key=lambda x: x.value)
    standard_garden.atmosphere.make_marginal(w.low_oxygen)
    assert issubclass(type(standard_garden.atmosphere), Marginal)
    p_id = categories.index(standard_garden.atmosphere.base.pressure_category)
    m_p_id = categories.index(standard_garden.atmosphere.pressure_category)
    assert (m_p_id in [p_id - 1, 0])


def test_set_marginal_nitrogen_compounds(standard_garden):
    standard_garden.atmosphere.make_marginal(w.nitrogen_compounds)
    assert issubclass(type(standard_garden.atmosphere), Marginal)
    assert (standard_garden.atmosphere.toxicity == ValueBounds(
                w.Atmosphere.Toxicity.MILD,
                w.Atmosphere.Toxicity.HIGH
           ))


def test_set_marginal_sulfur_compounds(standard_garden):
    standard_garden.atmosphere.make_marginal(w.sulfur_compounds)
    assert issubclass(type(standard_garden.atmosphere), Marginal)
    assert (standard_garden.atmosphere.toxicity == ValueBounds(
                w.Atmosphere.Toxicity.MILD,
                w.Atmosphere.Toxicity.HIGH
           ))


def test_set_marginal_organic_toxins(standard_garden):
    standard_garden.atmosphere.make_marginal(w.organic_toxins)
    assert issubclass(type(standard_garden.atmosphere), Marginal)
    assert (standard_garden.atmosphere.toxicity == ValueBounds(
                w.Atmosphere.Toxicity.MILD,
                w.Atmosphere.Toxicity.LETHAL
            ))


def test_set_marginal_pollutants(standard_garden):
    standard_garden.atmosphere.make_marginal(w.pollutants)
    assert issubclass(type(standard_garden.atmosphere), Marginal)
    assert (standard_garden.atmosphere.toxicity == w.Atmosphere.Toxicity.MILD)
