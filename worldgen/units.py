from astropy import units as u, constants as c
from .constants import v_earth

Ga = u.def_unit('Ga', 10 ** 9 * u.a)
d_earth = u.def_unit('d_earth', (c.M_earth / v_earth).to(u.g / u.cm ** 3))
