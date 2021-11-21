
from worldgen import Builder

import matplotlib.pyplot as plt
from PyAstronomy import pyasl
import numpy as np


def main():
    builder = Builder()
    system = builder.build_star_system()

    plt.legend(loc="upper right")
    plt.title('Orbital Simulation')

    t = np.linspace(0, 1, 200)

    orbit_pos = {}

    for i in range(0, len(system._stars)):
        component = getattr(system, chr(ord('A') + i))

        if component.forbidden_zone:
            pos = 0, 0
            if i > 0:
                orbit = pyasl.KeplerEllipse(a=component.orbit.radius.value,
                                            per=1,
                                            e=component.orbit.eccentricity,
                                            Omega=0, i=0)
                orbit_pos[component] = orbit.xyzPos(t)
                pos = orbit_pos[component][0, 0], orbit_pos[component][0, 1]

            outer_FZ = pyasl.KeplerEllipse(a=component.forbidden_zone.max.value,
                                           per=1, e=0, Omega=0, i=0)
            outer_FZ_pos = outer_FZ.xyzPos(t)

            plt.fill(pos[0] + outer_FZ_pos[::, 0], pos[1] + outer_FZ_pos[::, 1],
                     'red', alpha=.2)

    for i in range(0, len(system._stars)):
        component = getattr(system, chr(ord('A') + i))

        pos = 0, 0

        if i > 0:
            pos = orbit_pos[component][0, 0], orbit_pos[component][0, 1]

            plt.plot(orbit_pos[component][::, 0], orbit_pos[component][::, 1],
                     '-', color='black', label='%s orbit' % chr(ord('A') + i))

        if component.forbidden_zone:
            inner_FZ = pyasl.KeplerEllipse(a=component.forbidden_zone.min.value,
                                           per=1, e=0, Omega=0, i=0)
            inner_FZ_pos = inner_FZ.xyzPos(t)

            plt.fill(pos[0] + inner_FZ_pos[::, 0], pos[1] + inner_FZ_pos[::, 1],
                     'white')

        snow_line = pyasl.KeplerEllipse(a=component.snow_line.value, per=1, e=0,
                                        Omega=0, i=0)
        inner_limit = pyasl.KeplerEllipse(a=component.limits.min.value,
                                          per=1, e=0, Omega=0, i=0)
        outer_limit = pyasl.KeplerEllipse(a=component.limits.max.value,
                                          per=1, e=0, Omega=0, i=0)
        snow_line_pos = snow_line.xyzPos(t)
        inner_limit_pos = inner_limit.xyzPos(t)
        outer_limit_pos = outer_limit.xyzPos(t)

        plt.plot(pos[0] + snow_line_pos[::, 0], pos[1] + snow_line_pos[::, 1],
                 '--', label='%s snow_line' % chr(ord('A') + i), color='blue')
        plt.plot(pos[0] + inner_limit_pos[::, 0],
                 pos[1] + inner_limit_pos[::, 1], '--',
                 label='%s inner limit' % chr(ord('A') + i), color='black')
        plt.plot(pos[0] + outer_limit_pos[::, 0], pos[1] +
                 outer_limit_pos[::, 1], '--',
                 label='%s outer limit' % chr(ord('A') + i), color='black')
        plt.plot(pos[0], pos[1], '*', markersize=12, label=chr(ord('A') + i))

        for j in range(len(component._worlds)):
            world = getattr(component, chr(ord('b') + j))
            p_orbit = pyasl.KeplerEllipse(a=world.orbit.radius.value, per=1,
                                          e=world.orbit.radius.value, Omega=0, i=0)
            p_orbit_pos = p_orbit.xyzPos(t)
            plt.plot(pos[0] + p_orbit_pos[::, 0],
                     pos[1] + p_orbit_pos[::, 1], '-')
            plt.plot(pos[0] + p_orbit_pos[0, 0], pos[1] + p_orbit_pos[0, 1],
                     'o', markersize=9)

    plt.show()


if __name__ == '__main__':
    main()
