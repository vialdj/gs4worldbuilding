from worldgen.model import Model, RandomizableModel

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
        if isinstance(model, RandomizableModel):
            button = qt.QPushButton("Randomize")
            button.clicked.connect(self.randomize)
            self.layout().addWidget(button)
        self.layout().setContentsMargins(2, 1, 2, 1)

    def update(self):
        for p_widget in self.p_widgets.values():
            p_widget.update()

    def randomize(self):
        getattr(self.model, 'randomize')()
        self.update()


class PropertyWidget(qt.QWidget):
    """the Property Widget class"""

    def __init__(self, parent, model, prop):
        super(PropertyWidget, self).__init__(parent)

        self.model = model
        self.prop = prop
        self.value = getattr(model, prop)
        self.value_type = type(getattr(model, prop))

        layout = qt.QHBoxLayout()
        layout.addWidget(qt.QLabel(prop))
        if issubclass(self.value_type, Model):
            self.widget = ModelWidget(self.value)
        else:
            self.widget = self.__make_value_widget()
        layout.addWidget(self.widget)
        if getattr(model, 'random_{}'.format(prop), None) is not None:
            button = qt.QPushButton("Randomize")
            button.clicked.connect(self.randomize)
            layout.addWidget(button)
        layout.setContentsMargins(2, 1, 2, 1)
        self.setLayout(layout)

    def __make_value_widget(self):
        if (self.value_type is bool):
            return BoolWidget(self, self.model, self.prop)
        elif (self.value_type in [float, float64]):
            return DoubleWidget(self, self.model, self.prop)
        elif issubclass(self.value_type, Enum):
            return EnumWidget(self, self.model, self.prop)
        return qt.QLabel(str(self.value))

    def value_changed(self):
        self.parent().update()

    def randomize(self):
        getattr(self.model, 'random_{}'.format(self.prop))()
        self.value_changed()

    def update(self):
        self.value = getattr(self.model, self.prop)
        if isinstance(self.widget, ValueWidget) or isinstance(self.widget, ModelWidget):
            self.widget.update()
        else:
            self.widget.setText(str(self.value))


class ValueWidget(qt.QWidget):
    """the value widget class"""

    def __init__(self, parent, model, prop):
        super(ValueWidget, self).__init__(parent)

        self.value = getattr(model, prop)
        self.writable = getattr(type(model), prop).fset is not None
        self.range = getattr(model, '{}_range'.format(prop), None)
        self.model = model
        self.prop = prop

    def value_changed(self, value):
        setattr(self.model, self.prop, value)
        self.parent().value_changed()

    def update(self):
        self.value = getattr(self.model, self.prop)
        self.writable = getattr(type(self.model), self.prop).fset is not None
        self.range = getattr(self.model, '{}_range'.format(self.prop), None)


class EnumWidget(ValueWidget):
    """the enum value widget class"""

    def __init__(self, parent, model, prop):
        super(EnumWidget, self).__init__(parent, model, prop)
        layout = qt.QHBoxLayout()
        if self.writable:
            self.widget = qt.QComboBox()
            enums = filter(lambda e: e.value >= self.range.min and e.value <= self.range.max, [enum for enum in type(self.value)]) if self.range else [enum for enum in type(self.value)]
            self.names = [enum.name for enum in enums]
            self.widget.addItems(self.names)
            self.update()
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

    def update(self):
        super(EnumWidget, self).update()

        if self.writable:
            names = [self.widget.itemText(i) for i in range(self.widget.count())]
            self.widget.setCurrentIndex(names.index(self.value.name))
        else:
            self.widget.setText(self.value.name)


class DoubleWidget(ValueWidget):
    """the double value widget Class"""

    def __init__(self, parent, model, prop):
        super(DoubleWidget, self).__init__(parent, model, prop)
        layout = qt.QVBoxLayout()
        if self.writable:
            self.label = qt.QLabel('{:.2f}'.format(self.value))
            layout.addWidget(self.label)
            self.widget = DoubleSlider(Qt.Horizontal)
            self.update()
            self.widget.valueChanged.connect(self.value_changed)
        else:
            self.widget = qt.QLabel('{:.2f}'.format(self.value))
        layout.addWidget(self.widget)
        layout.setContentsMargins(2, 1, 2, 1)
        self.setLayout(layout)

    def value_changed(self):
        setattr(self.model, self.prop, self.widget.value())
        self.parent().value_changed()

    def update(self):
        super(DoubleWidget, self).update()

        if self.writable:
            self.label.setText('{:.2f}'.format(self.value))
            self.widget.setRange(self.range.min, self.range.max)
            self.widget.setValue(self.value)
        else:
            self.widget.setText('{:.2f}'.format(self.value))


class BoolWidget(ValueWidget):
    """the bool value widget class"""

    def __init__(self, parent, model, prop):
        super(BoolWidget, self).__init__(parent, model, prop)
        layout = qt.QHBoxLayout()
        if self.writable:
            self.widget = qt.QCheckBox()
            self.update()
            self.widget.stateChanged.connect(self.value_changed)
        else:
            self.widget = qt.QLabel(str(self.value))
        layout.addWidget(self.widget)
        layout.setContentsMargins(2, 1, 2, 1)
        self.setLayout(layout)

    def update(self):
        super(BoolWidget, self).update()

        if self.writable:
            self.widget.setChecked(self.value)
        else:
            self.widget.setText(str(self.value))


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
