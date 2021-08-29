
import worldgen as w

import pytest

@pytest.fixture
def star_system():
    # returns a StarSystem instance
    return w.StarSystem()

@pytest.fixture
def star(star_system):
    # returns a Star instance
    return w.Star(star_system)


def test_set_seed_mass_raises_exception_on_out_of_range(star):
    with pytest.raises(ValueError):
        star.seed_mass = .05