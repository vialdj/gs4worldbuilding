from gs4worldbuilding import Builder
from gs4worldbuilding.planet import InplacePlanet

from astropy import units as u

def main():
    builder = Builder()
    system = builder.build_star_system()

    for star in system._stars:
        for world in star._worlds:
            if issubclass(type(world), InplacePlanet):
                print('t:{}, re:{}, re_bounds:{}, r:{:.2f}, p:{:.2f}'.format(world.tide_locked, world.resonant, world.resonant_bounds, world.rotation, world._orbit.period.to(u.h)))
    #print(world)


if __name__ == '__main__':
    main()
