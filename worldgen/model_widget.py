from worldgen.model import Model

from enum import Enum

import PyQt5.QtWidgets as qt
from PyQt5.QtCore import Qt, QLocale
import PyQt5.QtGui as qtgui
from numpy import float64, isnan, format_float_scientific

QLocale.setDefault(QLocale(QLocale.C))


class ModelWidget(qt.QGroupBox):
    """the Model Widget class"""

    def __init__(self, model):
        super(ModelWidget, self).__init__()

        self.model = model

        self.setTitle(model.__class__.__name__)
        self.setLayout(qt.QVBoxLayout())
        self.update()

    def update(self):
        for prop, value in self.model:
            if not (value is None or (type(value) in [float, float64] and isnan(value))) and not prop.endswith('_range'):
                self.layout().addWidget(PropertyWidget(self, self.model, prop, value, write=getattr(type(self.model), prop).fset is not None))
        self.layout().setContentsMargins(2, 1, 2, 1)


class PropertyWidget(qt.QWidget):
    """the Property Widget class"""

    def __init__(self, parent, model, prop, value, write):
        super(PropertyWidget, self).__init__(parent)

        self.model = model
        self.prop = prop

        layout = qt.QHBoxLayout()
        layout.addWidget(qt.QLabel(prop))
        if issubclass(type(value), Model):
            widget = ModelWidget(value)
        else:
            widget = self.__make_value_widget(value, write, getattr(model, '{}_range'.format(prop), None))
        layout.addWidget(widget)
        layout.setContentsMargins(2, 1, 2, 1)
        self.setLayout(layout)

    def __make_value_widget(self, value, write, range):
        if (type(value) is bool):
            return BoolWidget(self, value, write, range)
        elif (type(value) in [float, float64]):
            return DoubleWidget(self, value, write, range)
        elif issubclass(type(value), Enum):
            return EnumWidget(self, value, write, range)
        return qt.QLabel(str(value))

    def value_changed(self, value):
        setattr(type(self.model), self.prop, value)
        self.parent().update()


class EnumWidget(qt.QWidget):
    """the enum value widget class"""

    def __init__(self, parent, value, write, range):
        super(EnumWidget, self).__init__(parent)
        layout = qt.QHBoxLayout()
        if write:
            widget = qt.QComboBox()
            enums = filter(lambda e: e.value >= range.min and e.value <= range.max, [enum for enum in type(value)]) if range else [enum for enum in type(value)]
            names = [enum.name for enum in enums]
            widget.addItems(names)
            widget.setCurrentIndex(names.index(value.name))
            widget.currentIndexChanged.connect(parent.value_changed)
        else:
            widget = qt.QLabel(value.name)
        layout.addWidget(widget)
        layout.setContentsMargins(2, 1, 2, 1)
        self.setLayout(layout)


class DoubleWidget(qt.QWidget):
    """the double value widget Class"""

    def __init__(self, parent, value, write, range):
        super(DoubleWidget, self).__init__(parent)
        layout = qt.QHBoxLayout()
        if write:
            widget = qt.QLineEdit(str(value))
            widget.setAlignment(Qt.AlignRight)
            self.validator = qtgui.QDoubleValidator()
            if range:
                self.validator.setRange(range.min, range.max, 2)
            widget.setValidator(self.validator)
            widget.editingFinished.connect(parent.value_changed)
        else:
            widget = qt.QLabel('{:.2f}'.format(value))
        layout.addWidget(widget)
        layout.setContentsMargins(2, 1, 2, 1)
        self.setLayout(layout)


class BoolWidget(qt.QWidget):
    """the bool value widget class"""

    def __init__(self, parent, value, write, range):
        super(BoolWidget, self).__init__(parent)
        layout = qt.QHBoxLayout()
        if write:
            widget = qt.QCheckBox()
            widget.setChecked(value)
            widget.stateChanged.connect(parent.value_changed)
        else:
            widget = qt.QLabel(str(value))
        layout.addWidget(widget)
        layout.setContentsMargins(2, 1, 2, 1)
        self.setLayout(layout)
