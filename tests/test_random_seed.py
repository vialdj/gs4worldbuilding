
import gs4worldbuilding as gs4wb
import pytest


@pytest.fixture
def builder():
    # returns a gs4wb builder
    return gs4wb.Builder()

@pytest.fixture
def system_42(builder):
    # returns a StarSystem built with the 42 seed
    return builder.build_star_system(42)


def test_seeds_42_42(builder, system_42):
    assert (system_42 == builder.build_star_system(42))


def test_seeds_84_42(builder, system_42):
    assert (system_42 != builder.build_star_system(84))
