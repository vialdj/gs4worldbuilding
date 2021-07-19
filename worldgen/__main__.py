from worldgen import Builder


def main():
    builder = Builder()
    world = builder.build_world()

    print(world)


if __name__ == '__main__':
    main()
