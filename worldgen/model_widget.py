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
        self.setTitle(model.__class__.__name__)
        layout = qt.QVBoxLayout()
        for prop, value in model:
            if not (value is None or (type(value) in [float, float64] and isnan(value))) and not prop.endswith('_range'):
                layout.addWidget(PropertyWidget(model, prop, value, write=getattr(type(model), prop).fset is not None))
        layout.setContentsMargins(2, 1, 2, 1)
        self.setLayout(layout)


class PropertyWidget(qt.QWidget):
    """the Property Widget class"""

    def __init__(self, model, prop, value, write):
        super(PropertyWidget, self).__init__()

        layout = qt.QHBoxLayout()
        layout.addWidget(qt.QLabel(prop))
        if issubclass(type(value), Model):
            widget = ModelWidget(value)
        else:
            widget = self.__make_value_widget(value, write, getattr(model, '{}_range'.format(prop), None))
        layout.addWidget(widget)
        layout.setContentsMargins(2, 1, 2, 1)
        self.setLayout(layout)

    @staticmethod
    def __make_value_widget(value, write, range):
        if (type(value) is bool):
            return BoolWidget(value, write, range)
        elif (type(value) in [float, float64]):
            return DoubleWidget(value, write, range)
        elif issubclass(type(value), Enum):
            return EnumWidget(value, write, range)
        return qt.QLabel(str(value))


class DoubleWidget(qt.QWidget):
    """the double value widget Class"""

    def __init__(self, value, write, range):
        super(DoubleWidget, self).__init__()
        layout = qt.QHBoxLayout()
        if write:
            widget = qt.QLineEdit(str(value))
            widget.setAlignment(Qt.AlignRight)
            validator = qtgui.QDoubleValidator()
            if range:
                validator.setRange(range.min, range.max, 2)
            widget.setValidator(validator)
        else:
            widget = qt.QLabel('{:.2f}'.format(value))
        layout.addWidget(widget)
        layout.setContentsMargins(2, 1, 2, 1)
        self.setLayout(layout)


class EnumWidget(qt.QWidget):
    """the enum value widget class"""

    def __init__(self, value, write, range):
        super(EnumWidget, self).__init__()
        layout = qt.QHBoxLayout()
        if write:
            widget = qt.QComboBox()
            names = [enum.name for enum in type(value)]
            widget.addItems(names)
            widget.setCurrentIndex(names.index(value.name))
        else:
            widget = qt.QLabel(value.name)
        layout.addWidget(widget)
        layout.setContentsMargins(2, 1, 2, 1)
        self.setLayout(layout)


class BoolWidget(qt.QWidget):
    """the bool value widget class"""

    def __init__(self, value, write, range):
        super(BoolWidget, self).__init__()        
        layout = qt.QHBoxLayout()
        if write:
            widget = qt.QCheckBox()
            widget.setChecked(value)
        else:
            widget = qt.QLabel(str(value))
        layout.addWidget(widget)
        layout.setContentsMargins(2, 1, 2, 1)
        self.setLayout(layout)
