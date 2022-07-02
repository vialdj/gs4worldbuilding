from typing import Callable, Optional, Type, Union, List

from pytest import mark, raises, approx
from astropy import units as u
from numpy import sqrt

from gs4worldbuilding.model.bounds import (
    QuantityBounds, ScalarBounds
)
from gs4worldbuilding.terrestrial import (
    TinyIce, SmallIce, StandardIce, LargeIce,
    StandardGreenhouse, LargeGreenhouse,
    StandardOcean, LargeOcean,
    StandardAmmonia, LargeAmmonia,
    StandardGarden, LargeGarden,
    StandardChthonian, LargeChthonian,
    SmallHadean, StandardHadean,
    TinyRock, SmallRock,
    TinySulfur,
    Size, Core, Atmosphere,
    SmallIceAtmosphere, StandardIceAtmosphere, LargeIceAtmosphere,
    StandardOceanAtmosphere, LargeOceanAtmosphere,
    StandardAmmoniaAtmosphere, LargeAmmoniaAtmosphere,
    StandardGardenAtmosphere, LargeGardenAtmosphere,
    StandardGreenhouseAtmosphere, LargeGreenhouseAtmosphere
)
from gs4worldbuilding.units import d_earth, D_earth

# Tests on world derived properties

"""
def test_get_climate(standard_garden):
    lower = standard_garden.climate
    upper = np.inf
    for item in list(Climate):
        if item > lower:
            upper = item
    assert (standard_garden.temperature >= lower and
            standard_garden.temperature <= upper)


def test_get_pressure_category(standard_ocean):
    lower = standard_ocean.atmosphere.pressure_category
    upper = np.inf
    for item in list(terrestrial.Pressure):
        if item > lower:
            upper = item
    assert (standard_ocean.atmosphere.pressure >= lower and
            standard_ocean.atmosphere.pressure <= upper)
"""

# Tests on concrete world instances


@mark.parametrize('terrestrial_type, temperature_bounds', [
    (TinyIce, QuantityBounds(80 * u.K, 140 * u.K)),
    (SmallIce, QuantityBounds(80 * u.K, 140 * u.K)),
    (StandardIce, QuantityBounds(80 * u.K, 230 * u.K)),
    (LargeIce, QuantityBounds(80 * u.K, 230 * u.K)),
    (StandardGreenhouse, QuantityBounds(500 * u.K, 950 * u.K)),
    (LargeGreenhouse, QuantityBounds(500 * u.K, 950 * u.K)),
    (StandardOcean, QuantityBounds(250 * u.K, 340 * u.K)),
    (LargeOcean, QuantityBounds(250 * u.K, 340 * u.K)),
    (StandardAmmonia, QuantityBounds(140 * u.K, 215 * u.K)),
    (LargeAmmonia, QuantityBounds(140 * u.K, 215 * u.K)),
    (StandardGarden, QuantityBounds(250 * u.K, 340 * u.K)),
    (LargeGarden, QuantityBounds(250 * u.K, 340 * u.K)),
    (StandardChthonian, QuantityBounds(500 * u.K, 950 * u.K)),
    (LargeChthonian, QuantityBounds(500 * u.K, 950 * u.K)),
    (SmallHadean, QuantityBounds(50 * u.K, 80 * u.K)),
    (StandardHadean, QuantityBounds(50 * u.K, 80 * u.K)),
    (TinyRock, QuantityBounds(140 * u.K, 500 * u.K)),
    (SmallRock, QuantityBounds(140 * u.K, 500 * u.K)),
    (TinySulfur, QuantityBounds(80 * u.K, 140 * u.K))
])
def test_temperature(terrestrial_type: Callable,
                     temperature_bounds: QuantityBounds):
    '''tests that the terrestrial temperature property is ranged in
temperature bounds'''
    terrestrial = terrestrial_type()
    assert (terrestrial.temperature >= temperature_bounds.lower and
            terrestrial.temperature <= temperature_bounds.upper)
    with raises(ValueError):
        terrestrial.temperature = temperature_bounds.lower - (1 * u.K)
    with raises(ValueError):
        terrestrial.temperature = temperature_bounds.upper + (1 * u.K)
    terrestrial.temperature = temperature_bounds.scale(.5)
    assert terrestrial.temperature == temperature_bounds.scale(.5)


@mark.parametrize('terrestrial_type, blackbody_correction', [
    (TinyIce, .86),
    (StandardChthonian, .97), (LargeChthonian, .97),
    (SmallHadean, .67), (StandardHadean, .67),
    (TinyRock, .97), (SmallRock, .96),
    (TinySulfur, .77)
])
def test_airless_blackbody_correction(terrestrial_type: Callable,
                                      blackbody_correction: float):
    '''tests the read-only blackbody_correction property value'''
    terrestrial = terrestrial_type()
    assert terrestrial.blackbody_correction == blackbody_correction
    with raises(AttributeError):
        terrestrial.blackbody_correction = .5


@mark.parametrize('terrestrial_type, blackbody_correction_bounds', [
    (SmallIce, ScalarBounds(.93 * (1 + .3 * .1), .93 * (1 + 1.8 * .1))),
    (StandardIce, ScalarBounds(.86 * (1 + .3 * .2), .86 * (1 + 1.8 * .2))),
    (LargeIce, ScalarBounds(.86 * (1 + .3 * .2), .86 * (1 + 1.8 * .2))),
    (StandardGreenhouse, ScalarBounds(.77 * (1 + .3 * 2),
                                      .77 * (1 + 1.8 * 2))),
    (LargeGreenhouse, ScalarBounds(.77 * (1 + .3 * 2), .77 * (1 + 1.8 * 2))),
    (StandardAmmonia, ScalarBounds(.84 * (1 + .3 * .2), .84 * (1 + 1.8 * .2))),
    (LargeAmmonia, ScalarBounds(.84 * (1 + .3 * .2), .84 * (1 + 1.8 * .2))),
])
def test_blackbody_correction(terrestrial_type: Callable,
                              blackbody_correction_bounds: ScalarBounds):
    '''tests that the terrestrial volatile mass dependent blackbody_correction
property is ranged in applicable bounds'''
    terrestrial = terrestrial_type()
    assert (terrestrial.blackbody_correction >=
            blackbody_correction_bounds.lower and
            terrestrial.blackbody_correction <=
            blackbody_correction_bounds.upper)
    with raises(AttributeError):
        terrestrial.blackbody_correction = .5
    terrestrial.volatile_mass = terrestrial.volatile_mass_bounds.lower
    assert (terrestrial.blackbody_correction ==
            blackbody_correction_bounds.lower)
    terrestrial.volatile_mass = terrestrial.volatile_mass_bounds.upper
    assert (terrestrial.blackbody_correction ==
            blackbody_correction_bounds.upper)


@mark.parametrize('terrestrial_type, blackbody_correction_bounds', [
    (StandardOcean, ScalarBounds(.84 * (1 + .3 * .16), .92 * (1 + 1.8 * .16))),
    (LargeOcean, ScalarBounds(.84 * (1 + .3 * .16), .915 * (1 + 1.8 * .16))),
    (StandardGarden, ScalarBounds(.84 * (1 + .3 * .16),
                                  .92 * (1 + 1.8 * .16))),
    (LargeGarden, ScalarBounds(.84 * (1 + .3 * .16), .915 * (1 + 1.8 * .16))),
])
def test_blackbody_correction_ocean_garden(terrestrial_type: Callable,
                                           blackbody_correction_bounds: ScalarBounds):
    '''tests that the terrestrial hydrographic coverage and volatile mass dependent
blackbody_correction property is ranged in applicable bounds'''
    terrestrial = terrestrial_type()
    assert (terrestrial.blackbody_correction >=
            blackbody_correction_bounds.lower and
            terrestrial.blackbody_correction <=
            blackbody_correction_bounds.upper)
    with raises(AttributeError):
        terrestrial.blackbody_correction = .5
    # assert blackbody correction is not solely dependent on volatile mass
    terrestrial.hydrographic_coverage = (terrestrial
                                         .hydrographic_coverage_bounds
                                         .scale(.5))
    terrestrial.volatile_mass = terrestrial.volatile_mass_bounds.lower
    assert (terrestrial.blackbody_correction !=
            approx(blackbody_correction_bounds.lower))
    terrestrial.volatile_mass = terrestrial.volatile_mass_bounds.lower
    assert (terrestrial.blackbody_correction !=
            approx(blackbody_correction_bounds.upper))
    # assert blackbody correction is not solely dependent on
    # hydrographic coverage
    terrestrial.volatile_mass = terrestrial.volatile_mass_bounds.scale(.5)
    terrestrial.hydrographic_coverage = (terrestrial
                                         .hydrographic_coverage_bounds
                                         .lower)
    assert (terrestrial.blackbody_correction !=
            approx(blackbody_correction_bounds.lower))
    terrestrial.hydrographic_coverage = (terrestrial
                                         .hydrographic_coverage_bounds
                                         .lower)
    assert (terrestrial.blackbody_correction !=
            approx(blackbody_correction_bounds.upper))
    # assert dependency on both hydrographic_coverage and volatile_mass
    terrestrial.volatile_mass = terrestrial.volatile_mass_bounds.lower
    terrestrial.hydrographic_coverage = (terrestrial
                                         .hydrographic_coverage_bounds
                                         .upper)
    assert (terrestrial.blackbody_correction ==
            approx(blackbody_correction_bounds.lower))
    terrestrial.volatile_mass = terrestrial.volatile_mass_bounds.upper
    terrestrial.hydrographic_coverage = (terrestrial
                                         .hydrographic_coverage_bounds
                                         .lower)
    assert (terrestrial.blackbody_correction ==
            approx(blackbody_correction_bounds.upper))


@mark.parametrize('terrestrial_type, absorption', [
    (TinyIce, .86), (SmallIce, .93), (StandardIce, .86), (LargeIce, .86),
    (StandardGreenhouse, .77), (LargeGreenhouse, .77),
    (StandardAmmonia, .84), (LargeAmmonia, .84),
    (StandardChthonian, .97), (LargeChthonian, .97),
    (SmallHadean, .67), (StandardHadean, .67),
    (TinyRock, .97), (SmallRock, .96),
    (TinySulfur, .77)
])
def test_absorption(terrestrial_type: Callable,
                    absorption: float):
    '''tests the read-only terrestrial absorption property value'''
    terrestrial = terrestrial_type()
    assert terrestrial.absorption == absorption
    with raises(AttributeError):
        terrestrial.absorption = .5


@mark.parametrize('terrestrial_type', [
    StandardOcean, LargeOcean,
    StandardGarden, LargeGarden
])
def test_ocean_garden_absorption(terrestrial_type: Callable):
    '''tests the read-only ocean or garden absorption property value'''
    terrestrial = terrestrial_type()
    assert ((terrestrial.hydrographic_coverage <= .90 and
             terrestrial.absorption >= .88) or
            terrestrial.absorption >= .84)
    with raises(AttributeError):
        terrestrial.absorption = .5
    terrestrial.hydrographic_coverage = .90
    assert terrestrial.absorption == approx(.88)
    terrestrial.hydrographic_coverage = 1
    assert terrestrial.absorption == approx(.84)


@mark.parametrize('terrestrial_type, size', [
    (TinyIce, Size.TINY), (SmallIce, Size.SMALL),
    (StandardIce, Size.STANDARD), (LargeIce, Size.LARGE),
    (StandardGreenhouse, Size.STANDARD), (LargeGreenhouse, Size.LARGE),
    (StandardOcean, Size.STANDARD), (LargeOcean, Size.LARGE),
    (StandardAmmonia, Size.STANDARD), (LargeAmmonia, Size.LARGE),
    (StandardGarden, Size.STANDARD), (LargeGarden, Size.LARGE),
    (StandardChthonian, Size.STANDARD), (LargeChthonian, Size.LARGE),
    (SmallHadean, Size.SMALL), (StandardHadean, Size.STANDARD),
    (TinyRock, Size.TINY), (SmallRock, Size.SMALL),
    (TinySulfur, Size.TINY)
])
def test_size(terrestrial_type: Callable,
              size: Size):
    '''tests the read-only terrestrial size property value'''
    terrestrial = terrestrial_type()
    assert terrestrial.size == size
    with raises(AttributeError):
        terrestrial.size = Size.STANDARD


@mark.parametrize('terrestrial_type, core', [
    (TinyIce, Core.ICY_CORE), (SmallIce, Core.ICY_CORE),
    (StandardIce, Core.LARGE_IRON_CORE), (LargeIce, Core.LARGE_IRON_CORE),
    (StandardGreenhouse, Core.LARGE_IRON_CORE),
    (LargeGreenhouse, Core.LARGE_IRON_CORE),
    (StandardOcean, Core.LARGE_IRON_CORE), (LargeOcean, Core.LARGE_IRON_CORE),
    (StandardAmmonia, Core.ICY_CORE), (LargeAmmonia, Core.ICY_CORE),
    (StandardGarden, Core.LARGE_IRON_CORE),
    (LargeGarden, Core.LARGE_IRON_CORE),
    (StandardChthonian, Core.LARGE_IRON_CORE),
    (LargeChthonian, Core.LARGE_IRON_CORE),
    (SmallHadean, Core.ICY_CORE), (StandardHadean, Core.ICY_CORE),
    (TinyRock, Core.SMALL_IRON_CORE), (SmallRock, Core.SMALL_IRON_CORE),
    (TinySulfur, Core.ICY_CORE)
])
def test_core(terrestrial_type: Callable,
              core: Core):
    '''tests the read-only terrestrial core property value'''
    terrestrial = terrestrial_type()
    assert terrestrial.core == core
    with raises(AttributeError):
        terrestrial.core = Core.LARGE_IRON_CORE


@mark.parametrize('terrestrial_type, atmosphere_type', [
    (TinyIce, None), (SmallIce, SmallIceAtmosphere),
    (StandardIce, StandardIceAtmosphere), (LargeIce, LargeIceAtmosphere),
    (StandardOcean, StandardOceanAtmosphere),
    (LargeOcean, LargeOceanAtmosphere),
    (StandardAmmonia, StandardAmmoniaAtmosphere),
    (LargeAmmonia, LargeAmmoniaAtmosphere),
    (StandardGarden, StandardGardenAtmosphere),
    (LargeGarden, LargeGardenAtmosphere),
    (StandardChthonian, None), (LargeChthonian, None),
    (SmallHadean, None), (StandardHadean, None),
    (TinyRock, None), (SmallRock, None),
    (TinySulfur, None),
    (StandardGreenhouse, StandardGreenhouseAtmosphere),
    (LargeGreenhouse, LargeGreenhouseAtmosphere)
])
def test_atmosphere(terrestrial_type: Callable,
                    atmosphere_type: Optional[Type[Atmosphere]]):
    '''tests the read-only terrestrial atmosphere related properties values'''
    terrestrial = terrestrial_type()
    if atmosphere_type:
        assert isinstance(terrestrial.atmosphere, atmosphere_type)
    else:
        assert terrestrial.atmosphere is None
    with raises(AttributeError):
        terrestrial.atmosphere = None


@mark.parametrize('terrestrial_type, pressure_factor', [
    (TinyIce, None), (SmallIce, 10), (StandardIce, 1), (LargeIce, 5),
    (StandardOcean, 1), (LargeOcean, 5),
    (StandardAmmonia, 1), (LargeAmmonia, 5),
    (StandardGarden, 1), (LargeGarden, 5),
    (StandardChthonian, None), (LargeChthonian, None),
    (SmallHadean, None), (StandardHadean, None),
    (TinyRock, None), (SmallRock, None),
    (TinySulfur, None),
    (StandardGreenhouse, 100), (LargeGreenhouse, 500)
])
def test_pressure_factor(terrestrial_type: Callable,
                         pressure_factor: float):
    '''tests the read-only terrestrial pressure_factor property value'''
    terrestrial = terrestrial_type()
    assert terrestrial.pressure_factor == pressure_factor
    with raises(AttributeError):
        terrestrial.pressure_factor = .5


@mark.parametrize('terrestrial_type', [
    TinyIce, SmallIce, StandardIce, LargeIce,
    StandardOcean, LargeOcean,
    StandardAmmonia, LargeAmmonia,
    StandardGarden, LargeGarden,
    StandardChthonian, LargeChthonian,
    SmallHadean, StandardHadean,
    TinyRock, SmallRock,
    TinySulfur,
    StandardGreenhouse, LargeGreenhouse
])
def test_blackbody_temperature(terrestrial_type: Callable):
    '''tests the read-only terrestrial blackbody temperature property value'''
    terrestrial = terrestrial_type()
    assert (terrestrial.blackbody_temperature ==
            terrestrial.temperature / terrestrial.blackbody_correction)
    with raises(AttributeError):
        terrestrial.blackbody_temperature = 150 * u.K


@mark.parametrize('terrestrial_type, greenhouse_factor', [
    (TinyIce, None), (SmallIce, .10), (StandardIce, .20), (LargeIce, .20),
    (StandardOcean, .16), (LargeOcean, .16),
    (StandardAmmonia, .2), (LargeAmmonia, .2),
    (StandardGarden, .16), (LargeGarden, .16),
    (StandardChthonian, None), (LargeChthonian, None),
    (SmallHadean, None), (StandardHadean, None),
    (TinyRock, None), (SmallRock, None),
    (TinySulfur, None),
    (StandardGreenhouse, 2), (LargeGreenhouse, 2)
])
def test_greenhouse_factor(terrestrial_type: Callable,
                           greenhouse_factor: Optional[float]):
    '''tests the read-only terrestrial greenhouse_factor property value'''
    terrestrial = terrestrial_type()
    assert terrestrial.greenhouse_factor == greenhouse_factor
    with raises(AttributeError):
        terrestrial.greenhouse_factor = 1


@mark.parametrize('terrestrial_type, volatile_mass_bounds', [
    (TinyIce, None), (SmallIce, ScalarBounds(.3, 1.8)),
    (StandardIce,  ScalarBounds(.3, 1.8)), (LargeIce,  ScalarBounds(.3, 1.8)),
    (StandardOcean, ScalarBounds(.3, 1.8)),
    (LargeOcean, ScalarBounds(.3, 1.8)),
    (StandardAmmonia, ScalarBounds(.3, 1.8)),
    (LargeAmmonia, ScalarBounds(.3, 1.8)),
    (StandardGarden, ScalarBounds(.3, 1.8)),
    (LargeGarden, ScalarBounds(.3, 1.8)),
    (StandardChthonian, None), (LargeChthonian, None),
    (SmallHadean, None), (StandardHadean, None),
    (TinyRock, None), (SmallRock, None),
    (TinySulfur, None),
    (StandardGreenhouse, ScalarBounds(.3, 1.8)),
    (LargeGreenhouse, ScalarBounds(.3, 1.8))
])
def test_volatile_mass(terrestrial_type: Callable,
                       volatile_mass_bounds: Optional[ScalarBounds]):
    '''tests the terrestrial volatile_mass property value'''
    terrestrial = terrestrial_type()
    if volatile_mass_bounds:
        assert (terrestrial.volatile_mass >=
                volatile_mass_bounds.lower and
                terrestrial.volatile_mass <=
                volatile_mass_bounds.upper)
        terrestrial.volatile_mass = 1
        assert terrestrial.volatile_mass == 1
    else:
        assert terrestrial.volatile_mass is None
        with raises(AttributeError):
            terrestrial.volatile_mass = 1


@mark.parametrize('terrestrial_type, density_bounds', [
    (TinyIce, QuantityBounds(.3 * d_earth, .7 * d_earth)),
    (SmallIce, QuantityBounds(.3 * d_earth, .7 * d_earth)),
    (StandardIce, QuantityBounds(.8 * d_earth, 1.2 * d_earth)),
    (LargeIce, QuantityBounds(.8 * d_earth, 1.2 * d_earth)),
    (StandardGreenhouse, QuantityBounds(.8 * d_earth, 1.2 * d_earth)),
    (LargeGreenhouse, QuantityBounds(.8 * d_earth, 1.2 * d_earth)),
    (StandardOcean, QuantityBounds(.8 * d_earth, 1.2 * d_earth)),
    (LargeOcean, QuantityBounds(.8 * d_earth, 1.2 * d_earth)),
    (StandardAmmonia, QuantityBounds(.3 * d_earth, .7 * d_earth)),
    (LargeAmmonia, QuantityBounds(.3 * d_earth, .7 * d_earth)),
    (StandardGarden, QuantityBounds(.8 * d_earth, 1.2 * d_earth)),
    (LargeGarden, QuantityBounds(.8 * d_earth, 1.2 * d_earth)),
    (StandardChthonian, QuantityBounds(.8 * d_earth, 1.2 * d_earth)),
    (LargeChthonian, QuantityBounds(.8 * d_earth, 1.2 * d_earth)),
    (SmallHadean, QuantityBounds(.3 * d_earth, .7 * d_earth)),
    (StandardHadean, QuantityBounds(.3 * d_earth, .7 * d_earth)),
    (TinyRock, QuantityBounds(.6 * d_earth, 1 * d_earth)),
    (SmallRock, QuantityBounds(.6 * d_earth, 1 * d_earth)),
    (TinySulfur, QuantityBounds(.3 * d_earth, .7 * d_earth)),
])
def test_density(terrestrial_type: Callable,
                 density_bounds: QuantityBounds):
    '''tests that the terrestrial density property is ranged in
density bounds'''
    terrestrial = terrestrial_type()
    assert (terrestrial.density >= density_bounds.lower and
            terrestrial.density <= density_bounds.upper)
    with raises(ValueError):
        terrestrial.density = density_bounds.lower - (.1 * d_earth)
    with raises(ValueError):
        terrestrial.density = density_bounds.upper + (.1 * d_earth)
    with raises(ValueError):
        terrestrial.density = 4
    with raises(ValueError):
        terrestrial.density = 80 * u.K
    terrestrial.density = density_bounds.scale(.5)
    assert terrestrial.density == density_bounds.scale(.5)


@mark.parametrize('terrestrial_type, hydrographic_coverage_bounds', [
    (TinyIce, None), (SmallIce, ScalarBounds(.3, .8)),
    (StandardIce, ScalarBounds(0, .2)), (LargeIce, ScalarBounds(0, .2)),
    (StandardGreenhouse, ScalarBounds(0, .5)),
    (LargeGreenhouse, ScalarBounds(0, .5)),
    (StandardOcean, ScalarBounds(.5, 1)), (LargeOcean, ScalarBounds(.7, 1)),
    (StandardAmmonia, ScalarBounds(.2, 1)),
    (LargeAmmonia, ScalarBounds(.2, 1)),
    (StandardGarden, ScalarBounds(.5, 1)), (LargeGarden, ScalarBounds(.7, 1)),
    (StandardChthonian, None), (LargeChthonian, None),
    (TinyRock, None), (SmallRock, None),
    (TinySulfur, None)
])
def test_hydrographic_coverage(terrestrial_type: Callable,
                               hydrographic_coverage_bounds: Union[
                                None, ScalarBounds
                               ]):
    '''tests that the terrestrial hydrographic coverage property
is ranged in bounds'''
    terrestrial = terrestrial_type()
    if hydrographic_coverage_bounds:
        assert (terrestrial.hydrographic_coverage >=
                hydrographic_coverage_bounds.lower and
                terrestrial.hydrographic_coverage <=
                hydrographic_coverage_bounds.upper)
        with raises(ValueError):
            terrestrial.hydrographic_coverage = (hydrographic_coverage_bounds
                                                 .lower - .1)
        with raises(ValueError):
            terrestrial.hydrographic_coverage = (hydrographic_coverage_bounds
                                                 .upper + .1)
        with raises(ValueError):
            terrestrial.hydrogrpahic_coverage = 80 * u.K
        terrestrial.hydrographic_coverage = (hydrographic_coverage_bounds
                                             .scale(.5))
        assert (terrestrial.hydrographic_coverage ==
                hydrographic_coverage_bounds.scale(.5))
    else:
        assert terrestrial.hydrographic_coverage is None
        assert terrestrial.hydrographic_coverage_bounds is None


@mark.parametrize('terrestrial_type, diameter_bounds', [
    (TinyIce, QuantityBounds(sqrt((80 / .86) / .7) * .004 * D_earth,
                             sqrt((140 / .86) / .3) * .024 * D_earth)),
    (StandardChthonian,
     QuantityBounds(sqrt((500 / .97) / 1.2) * .030 * D_earth,
                    sqrt((950 / .97) / .8) * .065 * D_earth)),
    (LargeChthonian,
     QuantityBounds(sqrt((500 / .97) / 1.2) * .065 * D_earth,
                    sqrt((950 / .97) / .8) * .091 * D_earth)),
    (SmallHadean,
     QuantityBounds(sqrt((50 / .67) / .7) * .024 * D_earth,
                    sqrt((80 / .67) / .3) * .030 * D_earth)),
    (StandardHadean,
     QuantityBounds(sqrt((50 / .67) / .7) * .030 * D_earth,
                    sqrt((80 / .67) / .3) * .065 * D_earth)),
    (TinyRock,
     QuantityBounds(sqrt(140 / .97) * .004 * D_earth,
                    sqrt((500 / .97) / .6) * .024 * D_earth)),
    (SmallRock,
     QuantityBounds(sqrt(140 / .96) * .024 * D_earth,
                    sqrt((500 / .96) / .6) * .030 * D_earth)),
    (TinySulfur,
     QuantityBounds(sqrt((80 / .77) / .7) * .004 * D_earth,
                    sqrt((140 / .77) / .3) * .024 * D_earth))
])
def test_airless_diameter(terrestrial_type: Callable,
                          diameter_bounds: QuantityBounds):
    '''tests that the temperature and density dependent diameter
property is ranged in applicable bounds'''
    terrestrial = terrestrial_type()
    assert (terrestrial.diameter >=
            diameter_bounds.lower and
            terrestrial.diameter <=
            diameter_bounds.upper)
    # assert diameter is not solely dependent on temperature
    terrestrial.density = (terrestrial.density_bounds.scale(.5))
    terrestrial.temperature = terrestrial.temperature_bounds.lower
    assert terrestrial.diameter_bounds.lower != diameter_bounds.lower
    terrestrial.temperature = terrestrial.temperature_bounds.upper
    assert terrestrial.diameter_bounds.upper != diameter_bounds.upper
    # assert diameter is not solely dependent on density
    terrestrial.temperature = terrestrial.temperature_bounds.scale(.5)
    terrestrial.density = terrestrial.density_bounds.upper
    assert terrestrial.diameter_bounds.lower != diameter_bounds.lower
    terrestrial.density = terrestrial.density_bounds.lower
    assert terrestrial.diameter_bounds.upper != diameter_bounds.upper
    # assert dependency on both temperature and density
    terrestrial.temperature = terrestrial.temperature_bounds.lower
    terrestrial.density = terrestrial.density_bounds.upper
    assert terrestrial.diameter_bounds.lower == diameter_bounds.lower
    terrestrial.temperature = terrestrial.temperature_bounds.upper
    terrestrial.density = terrestrial.density_bounds.lower
    assert terrestrial.diameter_bounds.upper == diameter_bounds.upper


@mark.parametrize('terrestrial_type, diameter_bounds', [
    (SmallIce,
     QuantityBounds(sqrt((80 / (.93 * (1 + 1.8 * .1))) / .7)
                    * .024 * D_earth,
                    sqrt((140 / (.93 * (1 + .3 * .1))) / .3)
                    * .030 * D_earth)),
    (StandardIce,
     QuantityBounds(sqrt((80 / (.86 * (1 + 1.8 * .2))) / 1.2)
                    * .030 * D_earth,
                    sqrt((230 / (.86 * (1 + .3 * .2))) / .8)
                    * .065 * D_earth)),
    (LargeIce,
     QuantityBounds(sqrt((80 / (.86 * (1 + 1.8 * .2))) / 1.2)
                    * .065 * D_earth,
                    sqrt((230 / (.86 * (1 + .3 * .2))) / .8)
                    * .091 * D_earth)),
    (StandardGreenhouse,
     QuantityBounds(sqrt((500 / (.77 * (1 + 1.8 * 2))) / 1.2)
                    * .030 * D_earth,
                    sqrt((950 / (.77 * (1 + .3 * 2))) / .8)
                    * .065 * D_earth)),
    (LargeGreenhouse,
     QuantityBounds(sqrt((500 / (.77 * (1 + 1.8 * 2))) / 1.2)
                    * .065 * D_earth,
                    sqrt((950 / (.77 * (1 + .3 * 2))) / .8)
                    * .091 * D_earth)),
    (StandardAmmonia,
     QuantityBounds(sqrt((140 / (.84 * (1 + 1.8 * .2))) / .7)
                    * .030 * D_earth,
                    sqrt((215 / (.84 * (1 + .3 * .2))) / .3)
                    * .065 * D_earth)),
    (LargeAmmonia,
     QuantityBounds(sqrt((140 / (.84 * (1 + 1.8 * .2))) / .7)
                    * .065 * D_earth,
                    sqrt((215 / (.84 * (1 + .3 * .2))) / .3)
                    * .091 * D_earth))
])
def test_diameter(terrestrial_type: Callable,
                  diameter_bounds: QuantityBounds):
    '''tests that the diameter property is also dependent on
volatile_mass and is ranged in applicable bounds'''
    terrestrial = terrestrial_type()
    assert (terrestrial.diameter >=
            diameter_bounds.lower and
            terrestrial.diameter <=
            diameter_bounds.upper)
    terrestrial.density = terrestrial.density_bounds.upper
    terrestrial.temperature = terrestrial.temperature_bounds.lower
    terrestrial.volatile_mass = terrestrial.volatile_mass_bounds.scale(.5)
    assert terrestrial.diameter_bounds.lower != diameter_bounds.lower
    terrestrial.density = terrestrial.density_bounds.upper
    terrestrial.temperature = terrestrial.temperature_bounds.lower
    terrestrial.volatile_mass = terrestrial.volatile_mass_bounds.upper
    assert terrestrial.diameter_bounds.lower == diameter_bounds.lower
    terrestrial.density = terrestrial.density_bounds.lower
    terrestrial.temperature = terrestrial.temperature_bounds.upper
    terrestrial.volatile_mass = terrestrial.volatile_mass_bounds.lower
    assert terrestrial.diameter_bounds.upper == diameter_bounds.upper
    terrestrial.diameter = terrestrial.diameter_bounds.scale(.5)
    assert terrestrial.diameter == terrestrial.diameter_bounds.scale(.5)
    with raises(ValueError);
        terrestrial.diameter = .5
    with raises(ValueError):
        terrestrial.diameter = 80 * u.K


@mark.parametrize('terrestrial_type, diameter_bounds', [
    (StandardOcean,
     QuantityBounds(sqrt((250 / (.92 * (1 + 1.8 * .16))) / 1.2)
                    * .030 * D_earth,
                    sqrt((340 / (.84 * (1 + .3 * .16))) / .8)
                    * .065 * D_earth)),
    (LargeOcean,
     QuantityBounds(sqrt((250 / (.915 * (1 + 1.8 * .16))) / 1.2)
                    * .065 * D_earth,
                    sqrt((340 / (.84 * (1 + .3 * .16))) / .8)
                    * .091 * D_earth)),
    (StandardGarden,
     QuantityBounds(sqrt((250 / (.92 * (1 + 1.8 * .16))) / 1.2)
                    * .030 * D_earth,
                    sqrt((340 / (.84 * (1 + .3 * .16))) / .8)
                    * .065 * D_earth)),
    (LargeGarden,
     QuantityBounds(sqrt((250 / (.915 * (1 + 1.8 * .16))) / 1.2)
                    * .065 * D_earth,
                    sqrt((340 / (.84 * (1 + .3 * .16))) / .8)
                    * .091 * D_earth)),
])
def test_diameter_ocean_garden(terrestrial_type: Callable,
                  diameter_bounds: QuantityBounds):
    '''tests that the diameter property is also dependent on
hydrographic_coverage and is ranged in applicable bounds'''
    terrestrial = terrestrial_type()
    assert (terrestrial.diameter >=
            diameter_bounds.lower and
            terrestrial.diameter <=
            diameter_bounds.upper)
    terrestrial.density = terrestrial.density_bounds.upper
    terrestrial.temperature = terrestrial.temperature_bounds.lower
    terrestrial.volatile_mass = terrestrial.volatile_mass_bounds.upper
    terrestrial.hydrographic_coverage = (terrestrial
                                         .hydrographic_coverage_bounds
                                         .scale(.5))
    assert (terrestrial.diameter_bounds.lower.value !=
            approx(diameter_bounds.lower.value))
    terrestrial.density = terrestrial.density_bounds.upper
    terrestrial.temperature = terrestrial.temperature_bounds.lower
    terrestrial.volatile_mass = terrestrial.volatile_mass_bounds.upper
    terrestrial.hydrographic_coverage = (terrestrial
                                         .hydrographic_coverage_bounds
                                         .lower)
    assert (terrestrial.diameter_bounds.lower.value ==
            approx(diameter_bounds.lower.value))
    terrestrial.density = terrestrial.density_bounds.lower
    terrestrial.temperature = terrestrial.temperature_bounds.upper
    terrestrial.volatile_mass = terrestrial.volatile_mass_bounds.lower
    terrestrial.hydrographic_coverage = (terrestrial
                                         .hydrographic_coverage_bounds
                                         .upper)
    assert (terrestrial.diameter_bounds.upper.value ==
            approx(diameter_bounds.upper.value))
