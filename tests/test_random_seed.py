import gs4worldbuilding as gs4wb


def test_seeded_worlds_are_equal():
    '''tests that two seeded worlds with the same value are equal'''
    a_world = gs4wb.Builder().build_world(42)
    b_world = gs4wb.Builder().build_world(42)

    assert a_world == b_world


def test_seeded_worlds_are_different():
    '''tests that two seeded worlds with a different value are not equal'''
    a_world = gs4wb.Builder().build_world(42)
    b_world = gs4wb.Builder().build_world(84)

    assert a_world != b_world


def test_seeded_starsystems_are_equal():
    '''tests that two seeded star systems with the same value are equal'''
    a_system = gs4wb.Builder().build_star_system(42)
    b_system = gs4wb.Builder().build_star_system(42)

    assert a_system == b_system


def test_seeded_starsystems_are_different():
    '''tests that two seeded star systems with a different value are
not equal'''
    a_system = gs4wb.Builder().build_star_system(42)
    b_system = gs4wb.Builder().build_star_system(84)

    assert a_system != b_system
