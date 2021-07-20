from .model_widget import ModelWidget

from worldgen import Builder

from PyQt5.QtWidgets import QApplication


def main():

    builder = Builder()
    world = builder.build_world()

    app = QApplication([])
    widget = ModelWidget(None, world)

    widget.show()
    app.exec_()


if __name__ == '__main__':
    main()
