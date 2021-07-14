from ..worldgen import Builder
from gui import ModelWidget

from PyQt5.QtWidgets import QApplication


def main():
    wgen = Builder()

    app = QApplication([])
    widget = ModelWidget(None, wgen.world)

    widget.show()
    app.exec_()


if __name__ == '__main__':
    main()
