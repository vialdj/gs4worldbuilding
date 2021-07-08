from worldgen.model import Model

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from numpy import isnan


class ModelWidget(QWidget):
    """the Model Widget class"""

    def __init__(self, model):
        super(ModelWidget, self).__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(model.__class__.__name__))
        for prop, value in model:
            layout.addWidget(PropertyWidget(model, prop, value, write=getattr(type(model), prop).fset is not None))
        self.setLayout(layout)


class PropertyWidget(QWidget):
    """the Property Widget class"""

    def __init__(self, model, prop, value, write=False):
        super(PropertyWidget, self).__init__()

        layout = QHBoxLayout()
        label = QLabel(prop)
        layout.addWidget(label)

        if value is not None:
            if issubclass(type(value), Model):
                layout.addWidget(ModelWidget(value))
            else:
                layout.addWidget(QLabel(str(value)))
        else:
            label.setEnabled(False)
        self.setLayout(layout)
