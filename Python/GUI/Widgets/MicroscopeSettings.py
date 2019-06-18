# -*- coding: utf-8 -*-
"""
This widget allows to control the settings of the DM6000 microscope that we need through Micro-Manager interaction

Created on Wed Apr  3 12:06:42 2019

@author: William Magrini @ Bordeaux Imaging Center
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import Modules.MM as MM
import data

class Ui_MicroscopeSettings(QtWidgets.QWidget):
    
    #Initialization of the class
    def setupUi(self, Form):
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 410, 271))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.labelMicroscopeSettings = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.labelMicroscopeSettings.setObjectName("labelMicroscopeSettings")
        self.labelMicroscopeSettings.setText("Microscope Settings")
        self.verticalLayout.addWidget(self.labelMicroscopeSettings)
        
        self.tabWidgetMethod = QtWidgets.QTabWidget(self.verticalLayoutWidget)
        self.tabWidgetMethod.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidgetMethod.setObjectName("tabWidgetMethod")
        
        
        self.FLUO = QtWidgets.QWidget()
        self.FLUO.setObjectName("FLUO")
        
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.FLUO)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(20, 50, 371, 111))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        
        self.labelShutterIL = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.labelShutterIL.setObjectName("labelShutterIL")
        self.labelShutterIL.setText("Shutter")
        self.gridLayout_2.addWidget(self.labelShutterIL, 0, 0, 1, 1)
        
        self.buttonShutterIL = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.buttonShutterIL.setMinimumSize(QtCore.QSize(200, 0))
        self.buttonShutterIL.setObjectName("buttonShutterIL")
        self.buttonShutterIL.setCheckable(True)
        self.buttonShutterIL.setText("IL-Shutter")
        self.gridLayout_2.addWidget(self.buttonShutterIL, 0, 1, 1, 1)
        
        self.LabelFilter = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.LabelFilter.setObjectName("LabelFilter")
        self.LabelFilter.setText("Filter")
        self.gridLayout_2.addWidget(self.LabelFilter, 1, 0, 1, 1)
        
        self.comboFilter = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        self.comboFilter.setMinimumSize(QtCore.QSize(200, 0))
        self.comboFilter.setObjectName("comboFilter")
        self.gridLayout_2.addWidget(self.comboFilter, 1, 1, 1, 1)
        
        self.labelShutterILState = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.labelShutterILState.setObjectName("labelShutterILState")
        self.labelShutterILState.setText("Closed")
        self.gridLayout_2.addWidget(self.labelShutterILState, 0, 2, 1, 1)
        
        self.tabWidgetMethod.addTab(self.FLUO, "")
        
        
        self.TLBF = QtWidgets.QWidget()
        self.TLBF.setObjectName("TLBF")
        
        self.gridLayoutWidget = QtWidgets.QWidget(self.TLBF)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(12, 10, 371, 201))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        
        self.sliderApertureBF = QtWidgets.QSlider(self.gridLayoutWidget)
        self.sliderApertureBF.setStyleSheet("color: rgb(170, 170, 255);")
        self.sliderApertureBF.setSingleStep(0)
        self.sliderApertureBF.setProperty("value", 0)
        self.sliderApertureBF.setOrientation(QtCore.Qt.Horizontal)
        self.sliderApertureBF.setObjectName("sliderApertureBF")
        self.gridLayout.addWidget(self.sliderApertureBF, 1, 1, 1, 1)
        
        self.spinBoxFieldBF = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBoxFieldBF.setMinimumSize(QtCore.QSize(70, 0))
        self.spinBoxFieldBF.setObjectName("spinBoxFieldBF")
        self.gridLayout.addWidget(self.spinBoxFieldBF, 2, 2, 1, 1)
        
        self.labelShutterBF = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelShutterBF.setObjectName("labelShutterBF")
        self.labelShutterBF.setText("Shutter")
        self.gridLayout.addWidget(self.labelShutterBF, 3, 0, 1, 1)
        
        self.buttonShutterBF = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.buttonShutterBF.setObjectName("buttonShutterBF")
        self.buttonShutterBF.setCheckable(True)
        self.buttonShutterBF.setText("TL-Shutter")
        self.gridLayout.addWidget(self.buttonShutterBF, 3, 1, 1, 1)
        
        self.labelApertureBF = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelApertureBF.setObjectName("labelApertureBF")
        self.labelApertureBF.setText("Aperture")
        self.gridLayout.addWidget(self.labelApertureBF, 1, 0, 1, 1)
        
        self.sliderIntensityBF = QtWidgets.QSlider(self.gridLayoutWidget)
        self.sliderIntensityBF.setOrientation(QtCore.Qt.Horizontal)
        self.sliderIntensityBF.setObjectName("sliderIntensityBF")
        self.gridLayout.addWidget(self.sliderIntensityBF, 0, 1, 1, 1)
        
        self.labelIntensityBF = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelIntensityBF.setObjectName("labelIntensityBF")
        self.labelIntensityBF.setText("Intensity")
        self.gridLayout.addWidget(self.labelIntensityBF, 0, 0, 1, 1)
        
        self.spinBoxApertureBF = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBoxApertureBF.setMinimumSize(QtCore.QSize(70, 0))
        self.spinBoxApertureBF.setObjectName("spinBoxApertureBF")
        self.gridLayout.addWidget(self.spinBoxApertureBF, 1, 2, 1, 1)
        
        self.labelLight = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelLight.setObjectName("labelLight")
        self.labelLight.setText("Light")
        self.gridLayout.addWidget(self.labelLight, 4, 0, 1, 1)
        
        self.labelFieldBF = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelFieldBF.setObjectName("labelFieldBF")
        self.labelFieldBF.setText("Field")
        self.gridLayout.addWidget(self.labelFieldBF, 2, 0, 1, 1)
        
        self.sliderFieldBF = QtWidgets.QSlider(self.gridLayoutWidget)
        self.sliderFieldBF.setOrientation(QtCore.Qt.Horizontal)
        self.sliderFieldBF.setObjectName("sliderFieldBF")
        self.gridLayout.addWidget(self.sliderFieldBF, 2, 1, 1, 1)
        
        self.spinBoxIntensityBF = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBoxIntensityBF.setEnabled(True)
        self.spinBoxIntensityBF.setMinimumSize(QtCore.QSize(70, 0))
        self.spinBoxIntensityBF.setObjectName("spinBoxIntensityBF")
        self.gridLayout.addWidget(self.spinBoxIntensityBF, 0, 2, 1, 1)
        
        self.buttonLightState = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.buttonLightState.setObjectName("buttonLightState")
        self.buttonLightState.setCheckable(True)
        self.buttonLightState.setChecked(True)
        self.buttonLightState.setText("State")
        self.gridLayout.addWidget(self.buttonLightState, 4, 1, 1, 1)
        
        self.labelLightState = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelLightState.setObjectName("labelLightState")
        self.labelLightState.setText("Off")
        self.gridLayout.addWidget(self.labelLightState, 4, 2, 1, 1)
        
        self.labelShutterBFState = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelShutterBFState.setObjectName("labelShutterBFState")
        self.labelShutterBFState.setText("Closed")
        self.gridLayout.addWidget(self.labelShutterBFState, 3, 2, 1, 1)
        
        self.tabWidgetMethod.addTab(self.TLBF, "")
        
        self.tabWidgetMethod.setTabText(self.tabWidgetMethod.indexOf(self.FLUO), "FLUO")
        self.tabWidgetMethod.setTabText(self.tabWidgetMethod.indexOf(self.TLBF), "TL BF")
        
        self.verticalLayout.addWidget(self.tabWidgetMethod)
        
        #Initialization of the settings
        self.initFilters()
        self.initMethod()
        self.initShutterTL()
        self.initShutterIL()
        self.initBFLightState()
        self.initIntensity(data.limitsIntensity, MM.getPropertyValue('Transmitted Light', 'Level'))
        self.initAperture(data.limitsAperture, MM.getPropertyValue('TL-ApertureDiaphragm', 'Position'))
        self.initFieldBF(data.limitsField, MM.getPropertyValue('TL-FieldDiaphragm', 'Position'))
        
    ###### DM6000 functions ######
    def initFilters(self):
        """Initializes the combo box values for the filters and sets the initial filter to the empty filter.
        """
        for el in data.filters.keys():
            self.comboFilter.addItem(el)
        self.comboFilter.setCurrentIndex(data.filters[MM.getPropertyValue('IL-Turret', 'Label')])
        self.comboFilter.currentIndexChanged['int'].connect(self.setFilter)
        
    def initMethod(self):
        """Initializes the method to BF
        """
        currentMethod = MM.getPropertyValue('Scope', 'Method')
        self.tabWidgetMethod.setCurrentIndex(data.methods[currentMethod])
        self.tabWidgetMethod.currentChanged['int'].connect(self.setMethod)
        
    def initIntensity(self, limits, value):
        """Sets the lower and upper limits for the BF intensity and initializes to the current value
        :type limits: [str, str]
        :type value: str
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
        """Sets the lower and upper limits for the BF aperture diaphragm and initializes to the current value
        :type limits: [str, str]
        :type value: str
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
        """Sets the lower and upper limits for the BF field diaphragm and initializes to the current value
        :type limits: [str, str]
        :type value: str
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
        """Initializes the BF light state to on
        """
        MM.setPropertyValue('Transmitted Light', 'State', '1')
        self.labelLightState.setText('On')
        self.buttonLightState.clicked.connect(self.setBFLightState)
        
    def initShutterTL(self):
        """Initializes the TL shutter state to closed
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
        """Initializes the IL shutter state to closed
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
        """Sets the method
        """
        tabIndex = self.tabWidgetMethod.currentIndex()
        MM.setPropertyValue('Scope', 'Method', self.tabWidgetMethod.tabText(tabIndex))
        if self.tabWidgetMethod.tabText(tabIndex)=='FLUO':
            self.comboFilter.setCurrentIndex(0)
        
    def setFilter(self):
        """Sets the filter
        """
        MM.setPropertyValue('IL-Turret', 'Label', self.comboFilter.currentText())
        
    def setShutterTL(self):
        """Sets the opening of the TL shutter
        """
        if self.buttonShutterBF.isChecked():
            MM.setPropertyValue('TL-Shutter', 'State', '1')
            self.labelShutterBFState.setText('Opened')
        else:
            MM.setPropertyValue('TL-Shutter', 'State', '0')
            self.labelShutterBFState.setText('Closed')
            
    def setShutterIL(self):
        """Sets the opening of the IL shutter
        """
        if self.buttonShutterIL.isChecked():
            MM.setPropertyValue('IL-Shutter', 'State', '1')
            self.labelShutterILState.setText('Opened')
        else:
            MM.setPropertyValue('IL-Shutter', 'State', '0')
            self.labelShutterILState.setText('Closed')
            
    def setBFLightState(self):
        """Sets the BF light on or off
        """
        if self.buttonLightState.isChecked():
            MM.setPropertyValue('Transmitted Light', 'State', '1')
        else:
            MM.setPropertyValue('Transmitted Light', 'State', '0')
        
    def setIntensityBF(self):
        """Sets the Intensity of the BF light
        """
        MM.setPropertyValue('Transmitted Light', 'Level', self.sliderIntensityBF.value())
        
    def setApertureBF(self):
        """Sets the opening of the BF aperture diaphragm
        """
        MM.setPropertyValue('TL-ApertureDiaphragm', 'Position', self.sliderApertureBF.value())
        
    def setFieldBF(self):
        """Sets the opening of the BF field diaphragm
        """
        MM.setPropertyValue('TL-FieldDiaphragm', 'Position', self.sliderFieldBF.value())

    def startAcq(self):
        """Automatically opens the shutter before acquisition starts
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
        """Automatically shuts the shutter before acquisition starts
        """
        if MM.getPropertyValue('Scope', 'Method') == 'FLUO':
            self.buttonShutterIL.setChecked(False)
            MM.setPropertyValue('IL-Shutter', 'State', '0')
            self.labelShutterILState.setText('Closed')
        else:
            self.buttonShutterBF.setChecked(False)
            MM.setPropertyValue('TL-Shutter', 'State', '0')
            self.labelShutterBFState.setText('Closed')
