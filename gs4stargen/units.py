from astropy import units as u, constants as c
from .constants import v_earth

Ga = u.def_unit('Ga', 10 ** 9 * u.a)
d_earth = u.def_unit('d_earth', (c.M_earth / v_earth).to(u.g / u.cm ** 3))
D_earth = u.def_unit('D_earth', 2 * u.R_earth)
D_sun = u.def_unit('D_sun', 2 * u.R_sun)
D_jup = u.def_unit('D_jup', 2 * u.R_jup)
G_earth = u.def_unit('G_earth', u.G * (u.M_earth / u.R_earth ** 2))
