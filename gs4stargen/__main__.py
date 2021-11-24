from gs4stargen import Builder


def main():
    builder = Builder()
    world = builder.build_star_system()

    print(world)


if __name__ == '__main__':
    main()
