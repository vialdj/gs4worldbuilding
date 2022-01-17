from astropy import constants as c
import numpy as np

v_earth = c.Constant(
    'v_earth',
    'Earth volume',
    (4 / 3) * np.pi * c.R_earth ** 3,
    'm3',
    0,
    ''
)
