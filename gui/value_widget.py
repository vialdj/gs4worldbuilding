import PyQt5.QtWidgets as qt_widgets
import PyQt5.QtCore as qt_core

import numpy as np

qt_core.QLocale.setDefault(qt_core.QLocale(qt_core.QLocale.C))


class ValueWidget(qt_widgets.QWidget):
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
        layout = qt_widgets.QHBoxLayout()
        if self.writable:
            self.widget = qt_widgets.QComboBox()
            enums = filter(lambda e: e.value >= self.range.min and e.value <= self.range.max, [enum for enum in type(self.value)]) if self.range else [enum for enum in type(self.value)]
            self.names = [enum.name for enum in enums]
            self.widget.addItems(self.names)
            self.update()
            self.widget.currentIndexChanged.connect(self.value_changed)
        else:
            self.widget = qt_widgets.QLabel(str(self.value))
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
            self.widget.setText(str(self.value))


class DoubleWidget(ValueWidget):
    """the double value widget Class"""

    def __init__(self, parent, model, prop):
        super(DoubleWidget, self).__init__(parent, model, prop)
        layout = qt_widgets.QGridLayout()
        self.value_widget = qt_widgets.QLabel('{:.2f}'.format(self.value))
        if self.writable:
            layout.addWidget(self.value_widget, 0, 0, qt_core.Qt.AlignCenter)
            self.slider_widget = DoubleSlider(qt_core.Qt.Horizontal)
            self.slider_widget.setRange(self.range.min, self.range.max)
            self.slider_widget.setValue(self.value)
            self.slider_widget.valueChanged.connect(self.value_changed)
            layout.addWidget(self.slider_widget)
        else:
            layout.addWidget(self.value_widget, 0, 0, qt_core.Qt.AlignRight)
        layout.setContentsMargins(2, 1, 2, 1)
        self.setLayout(layout)

    def value_changed(self):
        setattr(self.model, self.prop, self.slider_widget.value())
        self.parent().value_changed()

    def update(self):
        super(DoubleWidget, self).update()

        self.value_widget.setText('{:.2f}'.format(self.value))
        if self.writable:
            self.slider_widget.setRange(self.range.min, self.range.max)
            self.slider_widget.setValue(self.value)


class BoolWidget(ValueWidget):
    """the bool value widget class"""

    def __init__(self, parent, model, prop):
        super(BoolWidget, self).__init__(parent, model, prop)
        layout = qt_widgets.QHBoxLayout()
        if self.writable:
            self.widget = qt_widgets.QCheckBox()
            self.update()
            self.widget.stateChanged.connect(self.value_changed)
        else:
            self.widget = qt_widgets.QLabel(str(self.value))
        layout.addWidget(self.widget)
        layout.setContentsMargins(2, 1, 2, 1)
        self.setLayout(layout)

    def update(self):
        super(BoolWidget, self).update()

        if self.writable:
            self.widget.setChecked(self.value)
        else:
            self.widget.setText(str(self.value))


class DoubleSlider(qt_widgets.QSlider):

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
