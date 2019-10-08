# -*- coding: utf-8 -*-
"""
This widget allows to control the settings of the DM6000 microscope that we need through Micro-Manager interaction.

Created on Wed Apr  3 12:06:42 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtWidgets
import Modules.MM as MM
import data


class Ui_MicroscopeSettings(QtWidgets.QWidget):
    
    # Initialization of the class
    def __init__(self):
        super(Ui_MicroscopeSettings, self).__init__()

        self.setStyleSheet("QPushButton:disabled{background-color:rgb(120, 120, 120);}\n"
                           "QPushButton:checked{background-color:rgb(170, 15, 15);}")

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        
        self.labelMicroscopeSettings = QtWidgets.QLabel("Microscope Settings")
        
        self.tabWidgetMethod = QtWidgets.QTabWidget()
        self.tabWidgetMethod.setTabPosition(QtWidgets.QTabWidget.North)
        
        self.FLUO = QtWidgets.QWidget()

        self.gridLayoutFLUO = QtWidgets.QGridLayout(self.FLUO)
        self.gridLayoutFLUO.setSpacing(10)
        self.gridLayoutFLUO.setContentsMargins(10, 10, 10, 10)
        
        self.labelShutterIL = QtWidgets.QLabel("Shutter")
        
        self.buttonShutterIL = QtWidgets.QPushButton("IL-Shutter")
        self.buttonShutterIL.setMinimumSize(QtCore.QSize(200, 0))
        self.buttonShutterIL.setCheckable(True)
        
        self.LabelFilter = QtWidgets.QLabel("Filter")
        
        self.comboFilter = QtWidgets.QComboBox()
        self.comboFilter.setMinimumSize(QtCore.QSize(200, 0))
        
        self.labelShutterILState = QtWidgets.QLabel("Closed")
        
        self.tabWidgetMethod.addTab(self.FLUO, "")

        self.gridLayoutFLUO.addWidget(self.labelShutterIL, 0, 0, 1, 1)
        self.gridLayoutFLUO.addWidget(self.buttonShutterIL, 0, 1, 1, 1)
        self.gridLayoutFLUO.addWidget(self.LabelFilter, 1, 0, 1, 1)
        self.gridLayoutFLUO.addWidget(self.comboFilter, 1, 1, 1, 1)
        self.gridLayoutFLUO.addWidget(self.labelShutterILState, 0, 2, 1, 1)

        self.TLBF = QtWidgets.QWidget()

        self.gridLayoutBF = QtWidgets.QGridLayout(self.TLBF)
        self.gridLayoutBF.setVerticalSpacing(20)
        self.gridLayoutBF.setContentsMargins(10, 10, 10, 10)

        self.labelIntensityBF = QtWidgets.QLabel("Intensity")

        self.sliderIntensityBF = QtWidgets.QSlider()
        self.sliderIntensityBF.setOrientation(QtCore.Qt.Horizontal)

        self.spinBoxIntensityBF = QtWidgets.QSpinBox()
        self.spinBoxIntensityBF.setEnabled(True)
        self.spinBoxIntensityBF.setMinimumSize(QtCore.QSize(70, 0))

        self.labelApertureBF = QtWidgets.QLabel("Aperture")

        self.sliderApertureBF = QtWidgets.QSlider()
        self.sliderApertureBF.setOrientation(QtCore.Qt.Horizontal)

        self.spinBoxApertureBF = QtWidgets.QSpinBox()
        self.spinBoxApertureBF.setMinimumSize(QtCore.QSize(70, 0))

        self.labelFieldBF = QtWidgets.QLabel("Field")

        self.sliderFieldBF = QtWidgets.QSlider()
        self.sliderFieldBF.setOrientation(QtCore.Qt.Horizontal)
        
        self.spinBoxFieldBF = QtWidgets.QSpinBox()
        self.spinBoxFieldBF.setMinimumSize(QtCore.QSize(70, 0))
        
        self.labelShutterBF = QtWidgets.QLabel("Shutter")
        
        self.buttonShutterBF = QtWidgets.QPushButton("TL-Shutter")
        self.buttonShutterBF.setCheckable(True)

        self.labelShutterBFState = QtWidgets.QLabel("Closed")
        
        self.labelLight = QtWidgets.QLabel("Light")
        
        self.buttonLightState = QtWidgets.QPushButton("State")
        self.buttonLightState.setCheckable(True)
        self.buttonLightState.setChecked(True)
        
        self.labelLightState = QtWidgets.QLabel("Off")
        
        self.tabWidgetMethod.addTab(self.TLBF, "")

        self.gridLayoutBF.addWidget(self.labelIntensityBF, 0, 0, 1, 1)
        self.gridLayoutBF.addWidget(self.sliderIntensityBF, 0, 1, 1, 1)
        self.gridLayoutBF.addWidget(self.spinBoxIntensityBF, 0, 2, 1, 1)
        self.gridLayoutBF.addWidget(self.labelApertureBF, 1, 0, 1, 1)
        self.gridLayoutBF.addWidget(self.sliderApertureBF, 1, 1, 1, 1)
        self.gridLayoutBF.addWidget(self.spinBoxApertureBF, 1, 2, 1, 1)
        self.gridLayoutBF.addWidget(self.labelFieldBF, 2, 0, 1, 1)
        self.gridLayoutBF.addWidget(self.sliderFieldBF, 2, 1, 1, 1)
        self.gridLayoutBF.addWidget(self.spinBoxFieldBF, 2, 2, 1, 1)
        self.gridLayoutBF.addWidget(self.labelShutterBF, 3, 0, 1, 1)
        self.gridLayoutBF.addWidget(self.buttonShutterBF, 3, 1, 1, 1)
        self.gridLayoutBF.addWidget(self.labelShutterBFState, 3, 2, 1, 1)
        self.gridLayoutBF.addWidget(self.labelLight, 4, 0, 1, 1)
        self.gridLayoutBF.addWidget(self.buttonLightState, 4, 1, 1, 1)
        self.gridLayoutBF.addWidget(self.labelLightState, 4, 2, 1, 1)
        
        self.tabWidgetMethod.setTabText(self.tabWidgetMethod.indexOf(self.FLUO), "FLUO")
        self.tabWidgetMethod.setTabText(self.tabWidgetMethod.indexOf(self.TLBF), "TL BF")

        self.mainLayout.addWidget(self.labelMicroscopeSettings)
        self.mainLayout.addWidget(self.tabWidgetMethod)
        
        # Initialization of the settings
        self.initFilters()
        self.initMethod()
        self.initShutterTL()
        self.initShutterIL()
        self.initBFLightState()
        self.initIntensity(data.limitsIntensity, MM.getPropertyValue('Transmitted Light', 'Level'))
        self.initAperture(data.limitsAperture, MM.getPropertyValue('TL-ApertureDiaphragm', 'Position'))
        self.initFieldBF(data.limitsField, MM.getPropertyValue('TL-FieldDiaphragm', 'Position'))
        
    # DM6000 functions
    def initFilters(self):
        """
        Initializes the combo box values for the filters and sets the initial filter to the empty filter.
        """
        for el in data.filters.keys():
            self.comboFilter.addItem(el)
        self.comboFilter.setCurrentIndex(data.filters[MM.getPropertyValue('IL-Turret', 'Label')])
        self.comboFilter.currentIndexChanged['int'].connect(self.setFilter)
        
    def initMethod(self):
        """
        Initializes the method to the one which is selected on the microscope.
        """
        currentMethod = MM.getPropertyValue('Scope', 'Method')
        self.tabWidgetMethod.setCurrentIndex(data.methods[currentMethod])
        self.tabWidgetMethod.currentChanged['int'].connect(self.setMethod)
        
    def initIntensity(self, limits, value):
        """
        Sets the lower and upper limits for the BF intensity and initializes to the current value.
        :param limits: [str, str]
        :param value: str
        """
        self.sliderIntensityBF.setMinimum(limits[0])
        self.sliderIntensityBF.setMaximum(limits[1])
        self.sliderIntensityBF.setValue(int(value))
        self.spinBoxIntensityBF.setMinimum(limits[0])
        self.spinBoxIntensityBF.setMaximum(limits[1])
        self.spinBoxIntensityBF.setValue(int(value))
        self.sliderIntensityBF.sliderMoved['int'].connect(self.setIntensityBF)
        self.sliderIntensityBF.valueChanged['int'].connect(self.spinBoxIntensityBF.setValue)
        self.spinBoxIntensityBF.valueChanged['int'].connect(self.sliderIntensityBF.setValue)
        
    def initAperture(self, limits, value):
        """Sets the lower and upper limits for the BF aperture diaphragm and initializes to the current value.
        :param limits: [str, str]
        :param value: str
        """
        self.sliderApertureBF.setMinimum(limits[0])
        self.sliderApertureBF.setMaximum(limits[1])
        self.sliderApertureBF.setValue(int(value))
        self.spinBoxApertureBF.setMinimum(limits[0])
        self.spinBoxApertureBF.setMaximum(limits[1])
        self.spinBoxApertureBF.setValue(int(value))
        self.sliderApertureBF.sliderMoved['int'].connect(self.setApertureBF)
        self.sliderApertureBF.sliderMoved['int'].connect(self.spinBoxApertureBF.setValue)
        self.spinBoxApertureBF.valueChanged['int'].connect(self.sliderApertureBF.setValue)
        
    def initFieldBF(self, limits, value):
        """Sets the lower and upper limits for the BF field diaphragm and initializes to the current value.
        :param limits: [str, str]
        :param value: str
        """
        self.sliderFieldBF.setMinimum(limits[0])
        self.sliderFieldBF.setMaximum(limits[1])
        self.sliderFieldBF.setValue(int(value))
        self.spinBoxFieldBF.setMinimum(limits[0])
        self.spinBoxFieldBF.setMaximum(limits[1])
        self.spinBoxFieldBF.setValue(int(value))
        self.sliderFieldBF.sliderMoved['int'].connect(self.setFieldBF)
        self.spinBoxFieldBF.valueChanged['int'].connect(self.sliderFieldBF.setValue)
        self.sliderFieldBF.sliderMoved['int'].connect(self.spinBoxFieldBF.setValue)
        
    def initBFLightState(self):
        """
        Initializes the BF light state to on.
        """
        MM.setPropertyValue('Transmitted Light', 'State', '1')
        self.labelLightState.setText('On')
        self.buttonLightState.clicked.connect(self.setBFLightState)
        
    def initShutterTL(self):
        """
        Initializes the TL shutter state to closed.
        """
        currentValue = MM.getPropertyValue('TL-Shutter', 'State')
        MM.setPropertyValue('TL-Shutter', 'State', currentValue)
        if currentValue == '0':
            self.buttonShutterBF.setChecked(False)
            self.labelShutterBFState.setText('Closed')
        else:
            self.buttonShutterBF.setChecked(True)
            self.labelShutterBFState.setText('Open')
        self.buttonShutterBF.clicked.connect(self.setShutterTL)
        
    def initShutterIL(self):
        """
        Initializes the IL shutter state to closed.
        """
        currentValue = MM.getPropertyValue('IL-Shutter', 'State')
        MM.setPropertyValue('IL-Shutter', 'State', currentValue)
        if currentValue == '0':
            self.buttonShutterIL.setChecked(False)
            self.labelShutterILState.setText('Closed')
        else:
            self.buttonShutterIL.setChecked(True)
            self.labelShutterILState.setText('Open')
        self.buttonShutterIL.clicked.connect(self.setShutterIL)
        
    def setMethod(self):
        """
        Sets the method.
        """
        tabIndex = self.tabWidgetMethod.currentIndex()
        MM.setPropertyValue('Scope', 'Method', self.tabWidgetMethod.tabText(tabIndex))
        if self.tabWidgetMethod.tabText(tabIndex)=='FLUO':
            self.comboFilter.setCurrentIndex(0)
        
    def setFilter(self):
        """
        Sets the filter.
        """
        MM.setPropertyValue('IL-Turret', 'Label', self.comboFilter.currentText())
        
    def setShutterTL(self):
        """
        Sets the opening of the TL shutter.
        """
        if self.buttonShutterBF.isChecked():
            MM.setPropertyValue('TL-Shutter', 'State', '1')
            self.labelShutterBFState.setText('Opened')
        else:
            MM.setPropertyValue('TL-Shutter', 'State', '0')
            self.labelShutterBFState.setText('Closed')
            
    def setShutterIL(self):
        """
        Sets the opening of the IL shutter.
        """
        if self.buttonShutterIL.isChecked():
            MM.setPropertyValue('IL-Shutter', 'State', '1')
            self.labelShutterILState.setText('Opened')
        else:
            MM.setPropertyValue('IL-Shutter', 'State', '0')
            self.labelShutterILState.setText('Closed')
            
    def setBFLightState(self):
        """
        Sets the BF light on or off.
        """
        if self.buttonLightState.isChecked():
            MM.setPropertyValue('Transmitted Light', 'State', '1')
        else:
            MM.setPropertyValue('Transmitted Light', 'State', '0')
        
    def setIntensityBF(self):
        """
        Sets the Intensity of the BF light.
        """
        MM.setPropertyValue('Transmitted Light', 'Level', self.sliderIntensityBF.value())
        
    def setApertureBF(self):
        """
        Sets the opening of the BF aperture diaphragm.
        """
        MM.setPropertyValue('TL-ApertureDiaphragm', 'Position', self.sliderApertureBF.value())
        
    def setFieldBF(self):
        """
        Sets the opening of the BF field diaphragm.
        """
        MM.setPropertyValue('TL-FieldDiaphragm', 'Position', self.sliderFieldBF.value())

    def startAcq(self):
        """
        Automatically opens the shutter before acquisition starts.
        """
        if MM.getPropertyValue('Scope', 'Method') == 'FLUO':
            if self.buttonShutterIL.isChecked() == False:
                self.buttonShutterIL.setChecked(True)
                MM.setPropertyValue('IL-Shutter', 'State', '1')
                self.labelShutterILState.setText('Opened')
        else:
            if self.buttonShutterBF.isChecked() == False:
                self.buttonShutterBF.setChecked(True)
                MM.setPropertyValue('TL-Shutter', 'State', '1')
                self.labelShutterBFState.setText('Opened')

    def stopAcq(self):
        """
        Automatically shuts the shutter before acquisition starts.
        """
        if MM.getPropertyValue('Scope', 'Method') == 'FLUO':
            self.buttonShutterIL.setChecked(False)
            MM.setPropertyValue('IL-Shutter', 'State', '0')
            self.labelShutterILState.setText('Closed')
        else:
            self.buttonShutterBF.setChecked(False)
            MM.setPropertyValue('TL-Shutter', 'State', '0')
            self.labelShutterBFState.setText('Closed')
