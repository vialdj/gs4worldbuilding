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
        self.p_widgets = {}

        self.setTitle(model.__class__.__name__)
        self.setLayout(qt.QVBoxLayout())
        for prop, value in self.model:
            if not (value is None or (type(value) in [float, float64] and isnan(value))) and not prop.endswith('_range'):
                self.p_widgets[prop] = PropertyWidget(self, self.model, prop, value, write=getattr(type(self.model), prop).fset is not None)
                self.layout().addWidget(self.p_widgets[prop])
        self.layout().setContentsMargins(2, 1, 2, 1)

    def update(self):
        for prop, p_widget in self.p_widgets.items():
            p_widget.update(getattr(self.model, prop))


class PropertyWidget(qt.QWidget):
    """the Property Widget class"""

    def __init__(self, parent, model, prop, value, write):
        super(PropertyWidget, self).__init__(parent)

        self.model = model
        self.prop = prop

        layout = qt.QHBoxLayout()
        layout.addWidget(qt.QLabel(prop))
        if issubclass(type(value), Model):
            self.widget = ModelWidget(value)
        else:
            self.widget = self.__make_value_widget(model, prop, value, write, getattr(model, '{}_range'.format(prop), None))
        layout.addWidget(self.widget)
        layout.setContentsMargins(2, 1, 2, 1)
        self.setLayout(layout)

    def __make_value_widget(self, model, prop, value, write, range):
        if (type(value) is bool):
            return BoolWidget(self, model, prop, value, write, range)
        elif (type(value) in [float, float64]):
            return DoubleWidget(self, model, prop, value, write, range)
        elif issubclass(type(value), Enum):
            return EnumWidget(self, model, prop, value, write, range)
        return qt.QLabel(str(value))

    def value_changed(self):
        self.parent().update()

    def update(self, value):
        if isinstance(self.widget, BoolWidget) or isinstance(self.widget, DoubleWidget) or isinstance(self.widget, EnumWidget):
            self.widget.update(value)
        elif isinstance(self.widget, ModelWidget):
            self.widget.update()
        else:
            self.widget.setText(str(value))


class ValueWidget(qt.QWidget):
    """the value widget class"""

    def __init__(self, parent, model, prop, value, write, range):
        super(ValueWidget, self).__init__(parent)

        self.value = value
        self.write = write
        self.range = range
        self.model = model
        self.prop = prop

    def value_changed(self, value):
        setattr(self.model, self.prop, value)
        self.parent().value_changed()


class EnumWidget(ValueWidget):
    """the enum value widget class"""

    def __init__(self, parent, model, prop, value, write, range):
        super(EnumWidget, self).__init__(parent, model, prop, value, write, range)
        layout = qt.QHBoxLayout()
        if write:
            self.widget = qt.QComboBox()
            enums = filter(lambda e: e.value >= range.min and e.value <= range.max, [enum for enum in type(value)]) if range else [enum for enum in type(value)]
            names = [enum.name for enum in enums]
            self.widget.addItems(names)
            self.update(value)
            self.widget.currentIndexChanged.connect(self.value_changed)
        else:
            self.widget = qt.QLabel(value.name)
        layout.addWidget(self.widget)
        layout.setContentsMargins(2, 1, 2, 1)
        self.setLayout(layout)

    def update(self, value):
        if self.write:
            names = [self.widget.itemText(i) for i in range(self.widget.count())]
            self.widget.setCurrentIndex(names.index(value.name))
        else:
            self.widget.setText(value.name)


class DoubleWidget(ValueWidget):
    """the double value widget Class"""

    def __init__(self, parent, model, prop, value, write, range):
        super(DoubleWidget, self).__init__(parent, model, prop, value, write, range)
        layout = qt.QVBoxLayout()
        if write:
            self.label = qt.QLabel('{:.2f}'.format(value))
            layout.addWidget(self.label)
            self.widget = DoubleSlider(Qt.Horizontal)
            self.widget.setRange(range.min, range.max)
            self.update(value)
            self.widget.sliderReleased.connect(self.value_changed)
        else:
            self.widget = qt.QLabel('{:.2f}'.format(value))
        layout.addWidget(self.widget)
        layout.setContentsMargins(2, 1, 2, 1)
        self.setLayout(layout)

    def value_changed(self):
        setattr(self.model, self.prop, self.widget.value())
        self.parent().value_changed()

    def update(self, value):
        if self.write:
            self.label.setText('{:.2f}'.format(value))
            self.widget.setValue(value)
        else:
            self.widget.setText('{:.2f}'.format(value))


class BoolWidget(ValueWidget):
    """the bool value widget class"""

    def __init__(self, parent, model, prop, value, write, range):
        super(BoolWidget, self).__init__(parent, model, prop, value, write, range)
        layout = qt.QHBoxLayout()
        if write:
            self.widget = qt.QCheckBox()
            self.update(value)
            self.widget.stateChanged.connect(self.value_changed)
        else:
            self.widget = qt.QLabel(str(value))
        layout.addWidget(self.widget)
        layout.setContentsMargins(2, 1, 2, 1)
        self.setLayout(layout)

    def update(self, value):
        if self.write:
            self.widget.setChecked(value)
        else:
            self.widget.setText(str(value))


class DoubleSlider(qt.QSlider):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.decimals = 2
        self._max_int = 10 ** self.decimals

        super().setMinimum(0)
        super().setMaximum(self._max_int)

        self._min_value = 0.0
        self._max_value = 1.0

    @property
    def _value_range(self):
        return self._max_value - self._min_value

    def value(self):
        return float(super().value()) / self._max_int * self._value_range + self._min_value

    def setValue(self, value):
        super().setValue(int((value - self._min_value) / self._value_range * self._max_int))

    def setRange(self, min, max):
        self._min_value = min
        self._max_value = max

    def minimum(self):
        return self._min_value

    def maximum(self):
        return self._max_value
