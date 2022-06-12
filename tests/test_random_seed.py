import pytest

import gs4worldbuilding as gs4wb


@pytest.fixture
def system_42():
    # returns a StarSystem built with the 42 seed
    return gs4wb.Builder().build_star_system(42)


def test_seeds_42_42(system_42):
    assert system_42 == gs4wb.Builder().build_star_system(42)


def test_seeds_84_42(system_42):
    assert system_42 != gs4wb.Builder().build_star_system(84)
