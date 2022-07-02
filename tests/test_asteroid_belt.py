import astropy.units as u
from pytest import fixture

from gs4worldbuilding.asteroid_belt import AsteroidBelt

@fixture
def asteroid_belt():
    # returns an AsteroidBelt instance
    return AsteroidBelt()

def test_asteroid_belt(asteroid_belt):
    '''test asteroid properties in bounds'''
    asteroid_belt = AsteroidBelt()
    assert asteroid_belt.absorption == .97
    assert (asteroid_belt.temperature >= 140 * u.K and
            asteroid_belt.temperature <= 500 * u.K)
