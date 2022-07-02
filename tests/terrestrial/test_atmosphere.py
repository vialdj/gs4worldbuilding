from pickle import TRUE
from typing import Type, Callable, Union, List, Literal
from pytest import mark, raises

from gs4worldbuilding.model.bounds import EnumBounds
from gs4worldbuilding.terrestrial import (
    Atmosphere, Toxicity,
    SmallIce, SmallIceAtmosphere,
    StandardIce, StandardIceAtmosphere,
    LargeIce, LargeIceAtmosphere,
    StandardOcean, StandardOceanAtmosphere,
    LargeOcean, LargeOceanAtmosphere,
    StandardAmmonia, StandardAmmoniaAtmosphere,
    LargeAmmonia, LargeAmmoniaAtmosphere,
    StandardGarden, StandardGardenAtmosphere,
    LargeGarden, LargeGardenAtmosphere,
    StandardGreenhouse, StandardGreenhouseAtmosphere,
    LargeGreenhouse, LargeGreenhouseAtmosphere
)
from gs4worldbuilding.terrestrial.marginal_atmosphere import (
    MarginalCandidate,
    MarginalMixin,
    chlorine_or_fluorine,
    high_carbon_dioxide,
    high_oxygen,
    inert_gases,
    low_oxygen,
    nitrogen_compounds,
    organic_toxins,
    pollutants,
    sulfur_compounds
)


def get_atmosphere(terrestrial_type: Callable,
                   atmosphere_type: Type[Atmosphere],
                   remove_marginal: bool = True) -> Atmosphere:
    '''get the atmosphere for a given terrestrial'''
    terrestrial = terrestrial_type()
    atmosphere = terrestrial.atmosphere
    assert isinstance(atmosphere, atmosphere_type)
    if isinstance(atmosphere, MarginalCandidate) and remove_marginal:
        atmosphere.remove_marginal()
    return atmosphere


@mark.parametrize('terrestrial_type, atmosphere_type, toxicity', [
    (SmallIce, SmallIceAtmosphere, EnumBounds(Toxicity.MILD, Toxicity.HIGH)),
    (StandardIce, StandardIceAtmosphere,
     EnumBounds(Toxicity.NONE, Toxicity.MILD)),
    (LargeIce, LargeIceAtmosphere, Toxicity.HIGH),
    (StandardOcean, StandardOceanAtmosphere,
     EnumBounds(Toxicity.NONE, Toxicity.MILD)),
    (LargeOcean, LargeOceanAtmosphere, Toxicity.HIGH),
    (StandardAmmonia, StandardAmmoniaAtmosphere, Toxicity.LETHAL),
    (LargeAmmonia, LargeAmmoniaAtmosphere, Toxicity.LETHAL),
    (StandardGarden, StandardGardenAtmosphere, Toxicity.NONE),
    (LargeGarden, LargeGardenAtmosphere, Toxicity.NONE),
    (StandardGreenhouse, StandardGreenhouseAtmosphere, Toxicity.LETHAL),
    (LargeGreenhouse, LargeGreenhouseAtmosphere, Toxicity.LETHAL)
])
def test_toxicity(terrestrial_type: Callable,
                  atmosphere_type: Type[Atmosphere],
                  toxicity: Union[Toxicity, EnumBounds]):
    '''tests the read-only atmosphere toxicity property value'''
    atmosphere = get_atmosphere(terrestrial_type, atmosphere_type)
    if isinstance(toxicity, EnumBounds):
        assert (atmosphere.toxicity >= toxicity.lower and
                atmosphere.toxicity <= toxicity.upper)
    else:
        assert atmosphere.toxicity == toxicity
    with raises(AttributeError):
        atmosphere.toxicity = Toxicity.NONE


@mark.parametrize('terrestrial_type, atmosphere_type, composition', [
    (SmallIce, SmallIceAtmosphere, ['N2', 'CH4']),
    (StandardIce, StandardIceAtmosphere, ['CO2', 'N2']),
    (LargeIce, LargeIceAtmosphere, ['He', 'N2']),
    (StandardOcean, StandardOceanAtmosphere, ['CO2', 'N2']),
    (LargeOcean, LargeOceanAtmosphere, ['He', 'N2']),
    (StandardAmmonia, StandardAmmoniaAtmosphere, ['N2', 'NH3', 'CH4']),
    (LargeAmmonia, LargeAmmoniaAtmosphere, ['He', 'NH3', 'CH4']),
    (StandardGarden, StandardGardenAtmosphere, ['N2', 'O2']),
    (LargeGarden, LargeGardenAtmosphere, ['N2', 'O2', 'He', 'Ne', 'Ar',
                                          'Kr', 'Xe'])
])
def test_composition(terrestrial_type: Callable,
                     atmosphere_type: Type[Atmosphere],
                     composition: List[str]):
    '''tests the read-only atmosphere composition property value'''
    atmosphere = get_atmosphere(terrestrial_type, atmosphere_type)
    assert atmosphere.composition == composition
    with raises(AttributeError):
        atmosphere.composition = ['N2', 'O2', 'CO2']


@mark.parametrize('terrestrial_type, atmosphere_type', [
    (StandardGreenhouse, StandardGreenhouseAtmosphere),
    (LargeGreenhouse, LargeGreenhouseAtmosphere)
])
def test_greenhouse_composition(terrestrial_type: Callable,
                                atmosphere_type: Type[Atmosphere]):
    '''tests the read-only greenhouse atmosphere composition property value'''
    terrestrial = terrestrial_type()
    atmosphere = terrestrial.atmosphere
    assert isinstance(atmosphere, atmosphere_type)
    assert atmosphere.composition in [['CO2'], ['N2', 'H2O', 'O2']]
    terrestrial.hydrographic_coverage = .05
    assert atmosphere.composition == ['CO2']
    terrestrial.hydrographic_coverage = .15
    assert atmosphere.composition == ['N2', 'H2O', 'O2']


@mark.parametrize('terrestrial_type, atmosphere_type, suffocating', [
    (SmallIce, SmallIceAtmosphere, True),
    (StandardIce, StandardIceAtmosphere, True),
    (LargeIce, LargeIceAtmosphere, True),
    (StandardOcean, StandardOceanAtmosphere, True),
    (LargeOcean, LargeOceanAtmosphere, True),
    (StandardAmmonia, StandardAmmoniaAtmosphere, True),
    (LargeAmmonia, LargeAmmoniaAtmosphere, True),
    (StandardGarden, StandardGardenAtmosphere, False),
    (LargeGarden, LargeGardenAtmosphere, False),
    (StandardGreenhouse, StandardGreenhouseAtmosphere, True),
    (LargeGreenhouse, LargeGreenhouseAtmosphere, True)

])
def test_suffocating(terrestrial_type: Callable,
                     atmosphere_type: Type[Atmosphere],
                     suffocating: bool):
    '''tests the read-only atmosphere suffocating property value'''
    atmosphere = get_atmosphere(terrestrial_type, atmosphere_type)
    assert atmosphere.suffocating == suffocating
    with raises(AttributeError):
        atmosphere.suffocating = False


@mark.parametrize('terrestrial_type, atmosphere_type, corrosive', [
    (SmallIce, SmallIceAtmosphere, False),
    (StandardIce, StandardIceAtmosphere, False),
    (LargeIce, LargeIceAtmosphere, False),
    (StandardOcean, StandardOceanAtmosphere, False),
    (LargeOcean, LargeOceanAtmosphere, False),
    (StandardAmmonia, StandardAmmoniaAtmosphere, True),
    (LargeAmmonia, LargeAmmoniaAtmosphere, True),
    (StandardGarden, StandardGardenAtmosphere, False),
    (LargeGarden, LargeGardenAtmosphere, False),
    (StandardGreenhouse, StandardGreenhouseAtmosphere, True),
    (LargeGreenhouse, LargeGreenhouseAtmosphere, True)
])
def test_corrosive(terrestrial_type: Callable,
                   atmosphere_type: Type[Atmosphere],
                   corrosive: bool):
    '''tests the read-only atmosphere corrosive property value'''
    atmosphere = get_atmosphere(terrestrial_type, atmosphere_type)
    assert atmosphere.corrosive == corrosive
    with raises(AttributeError):
        atmosphere.corrosive = False


@mark.parametrize('terrestrial_type, atmosphere_type, breathable', [
    (SmallIce, SmallIceAtmosphere, False),
    (StandardIce, StandardIceAtmosphere, False),
    (LargeIce, LargeIceAtmosphere, False),
    (StandardOcean, StandardOceanAtmosphere, False),
    (LargeOcean, LargeOceanAtmosphere, False),
    (StandardAmmonia, StandardAmmoniaAtmosphere, False),
    (LargeAmmonia, LargeAmmoniaAtmosphere, False),
    (StandardGarden, StandardGardenAtmosphere, True),
    (LargeGarden, LargeGardenAtmosphere, True),
    (StandardGreenhouse, StandardGreenhouseAtmosphere, False),
    (LargeGreenhouse, LargeGreenhouseAtmosphere, False)
])
def test_breathable(terrestrial_type: Callable,
                    atmosphere_type: Type[Atmosphere],
                    breathable: bool):
    '''tests the read-only atmosphere breathable property value'''
    atmosphere = get_atmosphere(terrestrial_type, atmosphere_type)
    assert atmosphere.breathable == breathable
    with raises(AttributeError):
        atmosphere.breathable = False


@mark.parametrize('terrestrial_type, atmosphere_type', [
    (StandardGarden, StandardGardenAtmosphere),
    (LargeGarden, LargeGardenAtmosphere)
])
@mark.parametrize('marginal_type, toxicity, corrosive', [
    (chlorine_or_fluorine, Toxicity.HIGH, False),
    (high_carbon_dioxide, Toxicity.MILD, False),
    (high_oxygen, Toxicity.MILD, False),
    (low_oxygen, Toxicity.NONE, False),
    (nitrogen_compounds, Toxicity.MILD, False),
    (sulfur_compounds, Toxicity.MILD, False),
    (organic_toxins, Toxicity.MILD, False),
    (pollutants, Toxicity.MILD, False),
    (inert_gases, Toxicity.NONE, False)
])
def test_apply_marginal_modifier(terrestrial_type: Callable,
                                 atmosphere_type: Type[Atmosphere],
                                 marginal_type: Callable, toxicity: Toxicity,
                                 corrosive: bool):
    '''Asserts that the atmosphere displays the correct properties after
being made marginal'''
    atmosphere = get_atmosphere(terrestrial_type, atmosphere_type)
    assert isinstance(atmosphere, MarginalCandidate)
    atmosphere.make_marginal(marginal_type)
    assert isinstance(atmosphere, MarginalMixin)
    assert isinstance(atmosphere.base, atmosphere_type)
    assert atmosphere.toxicity == toxicity
    assert atmosphere.corrosive == corrosive
