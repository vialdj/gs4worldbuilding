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
                self.p_widgets[prop] = PropertyWidget(self, self.model, prop)
                self.layout().addWidget(self.p_widgets[prop])
        self.layout().setContentsMargins(2, 1, 2, 1)

    def update(self):
        for prop, p_widget in self.p_widgets.items():
            p_widget.update(getattr(self.model, prop))


class PropertyWidget(qt.QWidget):
    """the Property Widget class"""

    def __init__(self, parent, model, prop):
        super(PropertyWidget, self).__init__(parent)

        self.model = model
        self.prop = prop

        layout = qt.QHBoxLayout()
        layout.addWidget(qt.QLabel(prop))
        value = getattr(model, prop)
        if issubclass(type(value), Model):
            self.widget = ModelWidget(value)
        else:
            self.widget = self.__make_value_widget(model, prop, value)
        layout.addWidget(self.widget)
        layout.setContentsMargins(2, 1, 2, 1)
        self.setLayout(layout)

    def __make_value_widget(self, model, prop, value):
        if (type(value) is bool):
            return BoolWidget(self, model, prop)
        elif (type(value) in [float, float64]):
            return DoubleWidget(self, model, prop)
        elif issubclass(type(value), Enum):
            return EnumWidget(self, model, prop)
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

    def __init__(self, parent, model, prop):
        super(ValueWidget, self).__init__(parent)

        self.value = getattr(model, prop)
        self.write = getattr(type(model), prop).fset is not None
        self.range = getattr(model, '{}_range'.format(prop), None)
        self.model = model
        self.prop = prop

    def value_changed(self, value):
        setattr(self.model, self.prop, value)
        self.parent().value_changed()


class EnumWidget(ValueWidget):
    """the enum value widget class"""

    def __init__(self, parent, model, prop):
        super(EnumWidget, self).__init__(parent, model, prop)
        layout = qt.QHBoxLayout()
        if self.write:
            self.widget = qt.QComboBox()
            enums = filter(lambda e: e.value >= self.range.min and e.value <= self.range.max, [enum for enum in type(self.value)]) if self.range else [enum for enum in type(self.value)]
            self.names = [enum.name for enum in enums]
            self.widget.addItems(self.names)
            self.update(self.value)
            self.widget.currentIndexChanged.connect(self.value_changed)
        else:
            self.widget = qt.QLabel(self.value.name)
        layout.addWidget(self.widget)
        layout.setContentsMargins(2, 1, 2, 1)
        self.setLayout(layout)

    def value_changed(self):
        value = type(self.value)[self.names[self.widget.currentIndex()]]
        setattr(self.model, self.prop, value)
        self.parent().value_changed()

    def update(self, value):
        if self.write:
            names = [self.widget.itemText(i) for i in range(self.widget.count())]
            self.widget.setCurrentIndex(names.index(value.name))
        else:
            self.widget.setText(value.name)


class DoubleWidget(ValueWidget):
    """the double value widget Class"""

    def __init__(self, parent, model, prop):
        super(DoubleWidget, self).__init__(parent, model, prop)
        layout = qt.QVBoxLayout()
        if self.write:
            self.label = qt.QLabel('{:.2f}'.format(self.value))
            layout.addWidget(self.label)
            self.widget = DoubleSlider(Qt.Horizontal)
            self.widget.setRange(self.range.min, self.range.max)
            self.update(self.value)
            self.widget.sliderReleased.connect(self.value_changed)
        else:
            self.widget = qt.QLabel('{:.2f}'.format(self.value))
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

    def __init__(self, parent, model, prop):
        super(BoolWidget, self).__init__(parent, model, prop)
        layout = qt.QHBoxLayout()
        if self.write:
            self.widget = qt.QCheckBox()
            self.update(self.value)
            self.widget.stateChanged.connect(self.value_changed)
        else:
            self.widget = qt.QLabel(str(self.value))
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
