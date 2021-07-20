import gui.value_widget as gui_vwidgets

from worldgen.model import Model, RandomizableModel

from enum import Enum

import PyQt5.QtWidgets as qt_widgets
import PyQt5.QtCore as qt_core

import numpy as np


class ModelWidget(qt_widgets.QGroupBox):
    """the Model Widget class"""

    def __init__(self, parent, model):
        super(ModelWidget, self).__init__(parent)

        self.model = model
        self.prop_widgets = {}

        self.setTitle(model.__class__.__name__)
        self.setLayout(qt_widgets.QVBoxLayout())
        self.update()
        if isinstance(model, RandomizableModel) and not model.locked:
            button = qt_widgets.QPushButton("Randomize")
            button.clicked.connect(self.randomize)
            self.layout().addWidget(button)
        self.layout().setContentsMargins(2, 1, 2, 1)

    def update(self):
        self.setTitle(self.model.__class__.__name__)
        props = list(self.prop_widgets.keys())
        for prop, value in self.model:
            if not prop.endswith('_range') and not (value is None or (isinstance(value, (float, np.float64)) and np.isnan(value))):
                if prop in self.prop_widgets:
                    self.prop_widgets[prop].update()
                    props.remove(prop)
                else:
                    self.prop_widgets[prop] = PropertyWidget(self, self.model, prop)
                    self.layout().addWidget(self.prop_widgets[prop])
            elif prop in self.prop_widgets:
                self.layout().removeWidget(self.prop_widgets[prop])
                self.prop_widgets[prop].deleteLater()
                del self.prop_widgets[prop]
                props.remove(prop)
        for prop in props:
            self.layout().removeWidget(self.prop_widgets[prop])
            self.prop_widgets[prop].deleteLater()
            del self.prop_widgets[prop]

    def value_changed(self):
        self.parent().value_changed()

    def randomize(self):
        getattr(self.model, 'randomize')()
        if isinstance(self.parent(), PropertyWidget):
            self.value_changed()
        else:
            self.update()


class PropertyWidget(qt_widgets.QWidget):
    """the Property Widget class"""

    def __init__(self, parent, model, prop):
        super(PropertyWidget, self).__init__(parent)

        self.model = model
        self.prop = prop
        self.value = getattr(model, prop)
        self.value_type = type(getattr(model, prop))

        layout = qt_widgets.QGridLayout()
        name_widget = qt_widgets.QLabel(prop)
        name_widget.setToolTip(eval('type(model).{}.__doc__'.format(prop)))
        layout.addWidget(name_widget, 0, 0)
        if issubclass(self.value_type, Model):
            self.value_widget = ModelWidget(self, self.value)
        else:
            self.value_widget = self.__make_value_widget()
        layout.addWidget(self.value_widget, 0, 1, qt_core.Qt.AlignRight)
        if getattr(model, 'random_{}'.format(prop), None) is not None:
            button_widget = qt_widgets.QPushButton("Randomize")
            button_widget.clicked.connect(self.randomize)
            layout.addWidget(button_widget, 0, 2)
        layout.setContentsMargins(2, 1, 2, 1)
        self.setLayout(layout)

    def __make_value_widget(self):
        if (self.value_type is bool):
            return gui_vwidgets.BoolWidget(self, self.model, self.prop)
        elif (self.value_type in [float, np.float64]):
            return gui_vwidgets.DoubleWidget(self, self.model, self.prop)
        elif issubclass(self.value_type, Enum):
            return gui_vwidgets.EnumWidget(self, self.model, self.prop)
        return qt_widgets.QLabel(str(self.value))

    def value_changed(self):
        self.parent().update()

    def randomize(self):
        getattr(self.model, 'random_{}'.format(self.prop))()
        self.value_changed()

    def update(self):
        self.value = getattr(self.model, self.prop)
        if isinstance(self.value_widget, gui_vwidgets.ValueWidget) or isinstance(self.value_widget, ModelWidget):
            self.value_widget.update()
        else:
            self.value_widget.setText(str(self.value))
