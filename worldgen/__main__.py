from worldgen.world_generator import WorldGenerator
from worldgen.model_widget import ModelWidget

from PyQt5.QtWidgets import QApplication, QLabel


def main():
    wgen = WorldGenerator()

    app = QApplication([])
    widget = ModelWidget(None, wgen.world)

    widget.show()
    app.exec_()


if __name__ == '__main__':
    main()
