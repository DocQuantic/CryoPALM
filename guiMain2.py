# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guiMain.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(2350, 1295)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        MainWindow.setPalette(palette)
        MainWindow.setStyleSheet("background-color:rgb(64, 64, 64);\n"
"color:rgb(255, 255, 255);\n"
"QPushButton::hover{background-color:rgb(10,10,10);}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(550, 20, 800, 800))
        self.graphicsView.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.graphicsView.setObjectName("graphicsView")
        self.groupBoxLasersSettings = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxLasersSettings.setGeometry(QtCore.QRect(1440, 80, 441, 331))
        font = QtGui.QFont()
        font.setFamily("Berlin Sans FB")
        font.setPointSize(12)
        self.groupBoxLasersSettings.setFont(font)
        self.groupBoxLasersSettings.setObjectName("groupBoxLasersSettings")
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.groupBoxLasersSettings)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(19, 29, 231, 281))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayoutLasersSetting = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayoutLasersSetting.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutLasersSetting.setObjectName("gridLayoutLasersSetting")
        self.label488 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label488.setObjectName("label488")
        self.gridLayoutLasersSetting.addWidget(self.label488, 0, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.slider405 = QtWidgets.QSlider(self.gridLayoutWidget_4)
        self.slider405.setMinimumSize(QtCore.QSize(40, 0))
        self.slider405.setAutoFillBackground(False)
        self.slider405.setStyleSheet("background-color: rgb(85, 0, 255);\n"
"border-color: rgb(0, 0, 0);")
        self.slider405.setMaximum(255)
        self.slider405.setOrientation(QtCore.Qt.Vertical)
        self.slider405.setInvertedAppearance(False)
        self.slider405.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.slider405.setTickInterval(10)
        self.slider405.setObjectName("slider405")
        self.gridLayoutLasersSetting.addWidget(self.slider405, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.slider561 = QtWidgets.QSlider(self.gridLayoutWidget_4)
        self.slider561.setMinimumSize(QtCore.QSize(40, 0))
        self.slider561.setAutoFillBackground(False)
        self.slider561.setStyleSheet("background-color: rgb(0, 255, 0);\n"
"border-color: rgb(0, 0, 0);")
        self.slider561.setMaximum(255)
        self.slider561.setOrientation(QtCore.Qt.Vertical)
        self.slider561.setInvertedAppearance(False)
        self.slider561.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.slider561.setTickInterval(10)
        self.slider561.setObjectName("slider561")
        self.gridLayoutLasersSetting.addWidget(self.slider561, 1, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.label405 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label405.setObjectName("label405")
        self.gridLayoutLasersSetting.addWidget(self.label405, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.label561 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label561.setObjectName("label561")
        self.gridLayoutLasersSetting.addWidget(self.label561, 0, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.slider488 = QtWidgets.QSlider(self.gridLayoutWidget_4)
        self.slider488.setMinimumSize(QtCore.QSize(40, 0))
        self.slider488.setAutoFillBackground(False)
        self.slider488.setStyleSheet("background-color: rgb(85, 255, 255);\n"
"border-color: rgb(0, 0, 0);")
        self.slider488.setMaximum(255)
        self.slider488.setOrientation(QtCore.Qt.Vertical)
        self.slider488.setInvertedAppearance(False)
        self.slider488.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.slider488.setTickInterval(10)
        self.slider488.setObjectName("slider488")
        self.gridLayoutLasersSetting.addWidget(self.slider488, 1, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.spinBox405 = QtWidgets.QSpinBox(self.gridLayoutWidget_4)
        self.spinBox405.setObjectName("spinBox405")
        self.gridLayoutLasersSetting.addWidget(self.spinBox405, 2, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.spinBox488 = QtWidgets.QSpinBox(self.gridLayoutWidget_4)
        self.spinBox488.setObjectName("spinBox488")
        self.gridLayoutLasersSetting.addWidget(self.spinBox488, 2, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.spinBox561 = QtWidgets.QSpinBox(self.gridLayoutWidget_4)
        self.spinBox561.setObjectName("spinBox561")
        self.gridLayoutLasersSetting.addWidget(self.spinBox561, 2, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.pushButtonBlank = QtWidgets.QPushButton(self.groupBoxLasersSettings)
        self.pushButtonBlank.setGeometry(QtCore.QRect(290, 30, 111, 51))
        self.pushButtonBlank.setObjectName("pushButtonBlank")
        self.groupBoxAF = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxAF.setGeometry(QtCore.QRect(60, 1020, 401, 221))
        font = QtGui.QFont()
        font.setFamily("Berlin Sans FB")
        font.setPointSize(12)
        self.groupBoxAF.setFont(font)
        self.groupBoxAF.setObjectName("groupBoxAF")
        self.pushButtonFindFocus = QtWidgets.QPushButton(self.groupBoxAF)
        self.pushButtonFindFocus.setGeometry(QtCore.QRect(250, 40, 101, 51))
        self.pushButtonFindFocus.setObjectName("pushButtonFindFocus")
        self.gridLayoutWidget_5 = QtWidgets.QWidget(self.groupBoxAF)
        self.gridLayoutWidget_5.setGeometry(QtCore.QRect(20, 40, 191, 141))
        self.gridLayoutWidget_5.setObjectName("gridLayoutWidget_5")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.gridLayoutWidget_5)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.labelStepNumber = QtWidgets.QLabel(self.gridLayoutWidget_5)
        self.labelStepNumber.setObjectName("labelStepNumber")
        self.gridLayout_4.addWidget(self.labelStepNumber, 1, 0, 1, 1)
        self.spinBoxStepNumber = QtWidgets.QSpinBox(self.gridLayoutWidget_5)
        self.spinBoxStepNumber.setObjectName("spinBoxStepNumber")
        self.gridLayout_4.addWidget(self.spinBoxStepNumber, 1, 1, 1, 1)
        self.spinBoxZRange = QtWidgets.QSpinBox(self.gridLayoutWidget_5)
        self.spinBoxZRange.setObjectName("spinBoxZRange")
        self.gridLayout_4.addWidget(self.spinBoxZRange, 0, 1, 1, 1)
        self.labelZRange = QtWidgets.QLabel(self.gridLayoutWidget_5)
        self.labelZRange.setObjectName("labelZRange")
        self.gridLayout_4.addWidget(self.labelZRange, 0, 0, 1, 1)
        self.spinBoxStepSize = QtWidgets.QSpinBox(self.gridLayoutWidget_5)
        self.spinBoxStepSize.setObjectName("spinBoxStepSize")
        self.gridLayout_4.addWidget(self.spinBoxStepSize, 2, 1, 1, 1)
        self.labelStepSize = QtWidgets.QLabel(self.gridLayoutWidget_5)
        self.labelStepSize.setObjectName("labelStepSize")
        self.gridLayout_4.addWidget(self.labelStepSize, 2, 0, 1, 1)
        self.pushZoom = QtWidgets.QPushButton(self.centralwidget)
        self.pushZoom.setGeometry(QtCore.QRect(840, 830, 71, 31))
        self.pushZoom.setObjectName("pushZoom")
        self.pushButtonSetROI = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSetROI.setGeometry(QtCore.QRect(920, 830, 71, 31))
        self.pushButtonSetROI.setObjectName("pushButtonSetROI")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(540, 900, 891, 130))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.spinBoxMin = QtWidgets.QSpinBox(self.verticalLayoutWidget_3)
        self.spinBoxMin.setMinimumSize(QtCore.QSize(70, 0))
        self.spinBoxMin.setObjectName("spinBoxMin")
        self.horizontalLayout_2.addWidget(self.spinBoxMin)
        self.verticalLayoutSliders = QtWidgets.QVBoxLayout()
        self.verticalLayoutSliders.setObjectName("verticalLayoutSliders")
        self.labelMinimum = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.labelMinimum.setAlignment(QtCore.Qt.AlignCenter)
        self.labelMinimum.setObjectName("labelMinimum")
        self.verticalLayoutSliders.addWidget(self.labelMinimum)
        self.horizontalSliderMinimum = QtWidgets.QSlider(self.verticalLayoutWidget_3)
        self.horizontalSliderMinimum.setMaximum(65535)
        self.horizontalSliderMinimum.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderMinimum.setObjectName("horizontalSliderMinimum")
        self.verticalLayoutSliders.addWidget(self.horizontalSliderMinimum)
        self.labelMaximum = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.labelMaximum.setAlignment(QtCore.Qt.AlignCenter)
        self.labelMaximum.setObjectName("labelMaximum")
        self.verticalLayoutSliders.addWidget(self.labelMaximum)
        self.horizontalSliderMaximum = QtWidgets.QSlider(self.verticalLayoutWidget_3)
        self.horizontalSliderMaximum.setMaximum(65535)
        self.horizontalSliderMaximum.setProperty("value", 65535)
        self.horizontalSliderMaximum.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderMaximum.setObjectName("horizontalSliderMaximum")
        self.verticalLayoutSliders.addWidget(self.horizontalSliderMaximum)
        self.horizontalLayout_2.addLayout(self.verticalLayoutSliders)
        self.spinBoxMax = QtWidgets.QSpinBox(self.verticalLayoutWidget_3)
        self.spinBoxMax.setMinimumSize(QtCore.QSize(70, 0))
        self.spinBoxMax.setObjectName("spinBoxMax")
        self.horizontalLayout_2.addWidget(self.spinBoxMax)
        self.pushButtonAuto = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.pushButtonAuto.setObjectName("pushButtonAuto")
        self.horizontalLayout_2.addWidget(self.pushButtonAuto)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(60, 50, 411, 941))
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.verticalLayoutExperimentControl = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayoutExperimentControl.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutExperimentControl.setObjectName("verticalLayoutExperimentControl")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelMicroscopeSettings = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        font = QtGui.QFont()
        font.setFamily("Berlin Sans FB")
        font.setPointSize(14)
        self.labelMicroscopeSettings.setFont(font)
        self.labelMicroscopeSettings.setObjectName("labelMicroscopeSettings")
        self.verticalLayout.addWidget(self.labelMicroscopeSettings)
        self.tabWidgetMethod = QtWidgets.QTabWidget(self.verticalLayoutWidget_6)
        self.tabWidgetMethod.setMaximumSize(QtCore.QSize(16777215, 250))
        font = QtGui.QFont()
        font.setFamily("Berlin Sans FB")
        font.setPointSize(12)
        self.tabWidgetMethod.setFont(font)
        self.tabWidgetMethod.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidgetMethod.setObjectName("tabWidgetMethod")
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
        font = QtGui.QFont()
        font.setPointSize(12)
        self.spinBoxFieldBF.setFont(font)
        self.spinBoxFieldBF.setObjectName("spinBoxFieldBF")
        self.gridLayout.addWidget(self.spinBoxFieldBF, 2, 2, 1, 1)
        self.labelShutterBF = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelShutterBF.setFont(font)
        self.labelShutterBF.setObjectName("labelShutterBF")
        self.gridLayout.addWidget(self.labelShutterBF, 3, 0, 1, 1)
        self.buttonShutterBF = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.buttonShutterBF.setFont(font)
        self.buttonShutterBF.setObjectName("buttonShutterBF")
        self.gridLayout.addWidget(self.buttonShutterBF, 3, 1, 1, 1)
        self.labelApertureBF = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelApertureBF.setFont(font)
        self.labelApertureBF.setObjectName("labelApertureBF")
        self.gridLayout.addWidget(self.labelApertureBF, 1, 0, 1, 1)
        self.sliderIntensityBF = QtWidgets.QSlider(self.gridLayoutWidget)
        self.sliderIntensityBF.setOrientation(QtCore.Qt.Horizontal)
        self.sliderIntensityBF.setObjectName("sliderIntensityBF")
        self.gridLayout.addWidget(self.sliderIntensityBF, 0, 1, 1, 1)
        self.labelIntensityBF = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelIntensityBF.setFont(font)
        self.labelIntensityBF.setObjectName("labelIntensityBF")
        self.gridLayout.addWidget(self.labelIntensityBF, 0, 0, 1, 1)
        self.spinBoxApertureBF = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBoxApertureBF.setMinimumSize(QtCore.QSize(70, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.spinBoxApertureBF.setFont(font)
        self.spinBoxApertureBF.setObjectName("spinBoxApertureBF")
        self.gridLayout.addWidget(self.spinBoxApertureBF, 1, 2, 1, 1)
        self.labelLight = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelLight.setFont(font)
        self.labelLight.setObjectName("labelLight")
        self.gridLayout.addWidget(self.labelLight, 4, 0, 1, 1)
        self.labelFieldBF = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelFieldBF.setFont(font)
        self.labelFieldBF.setObjectName("labelFieldBF")
        self.gridLayout.addWidget(self.labelFieldBF, 2, 0, 1, 1)
        self.sliderFieldBF = QtWidgets.QSlider(self.gridLayoutWidget)
        self.sliderFieldBF.setOrientation(QtCore.Qt.Horizontal)
        self.sliderFieldBF.setObjectName("sliderFieldBF")
        self.gridLayout.addWidget(self.sliderFieldBF, 2, 1, 1, 1)
        self.spinBoxIntensityBF = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBoxIntensityBF.setEnabled(True)
        self.spinBoxIntensityBF.setMinimumSize(QtCore.QSize(70, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.spinBoxIntensityBF.setFont(font)
        self.spinBoxIntensityBF.setObjectName("spinBoxIntensityBF")
        self.gridLayout.addWidget(self.spinBoxIntensityBF, 0, 2, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 4, 1, 1, 1)
        self.labelLightState = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelLightState.setObjectName("labelLightState")
        self.gridLayout.addWidget(self.labelLightState, 4, 2, 1, 1)
        self.labelShutterBFState = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelShutterBFState.setObjectName("labelShutterBFState")
        self.gridLayout.addWidget(self.labelShutterBFState, 3, 2, 1, 1)
        self.tabWidgetMethod.addTab(self.TLBF, "")
        self.FLUO = QtWidgets.QWidget()
        self.FLUO.setObjectName("FLUO")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.FLUO)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(20, 50, 371, 111))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.labelShutterIL = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelShutterIL.setFont(font)
        self.labelShutterIL.setObjectName("labelShutterIL")
        self.gridLayout_2.addWidget(self.labelShutterIL, 0, 0, 1, 1)
        self.buttonShuterIL = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.buttonShuterIL.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.buttonShuterIL.setFont(font)
        self.buttonShuterIL.setObjectName("buttonShuterIL")
        self.gridLayout_2.addWidget(self.buttonShuterIL, 0, 1, 1, 1)
        self.LabelFilter = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.LabelFilter.setFont(font)
        self.LabelFilter.setObjectName("LabelFilter")
        self.gridLayout_2.addWidget(self.LabelFilter, 1, 0, 1, 1)
        self.comboFilter = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        self.comboFilter.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboFilter.setFont(font)
        self.comboFilter.setObjectName("comboFilter")
        self.gridLayout_2.addWidget(self.comboFilter, 1, 1, 1, 1)
        self.labelShutterILState = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.labelShutterILState.setObjectName("labelShutterILState")
        self.gridLayout_2.addWidget(self.labelShutterILState, 0, 2, 1, 1)
        self.tabWidgetMethod.addTab(self.FLUO, "")
        self.verticalLayout.addWidget(self.tabWidgetMethod)
        self.verticalLayoutExperimentControl.addLayout(self.verticalLayout)
        self.groupBoxCameraSettings = QtWidgets.QGroupBox(self.verticalLayoutWidget_6)
        self.groupBoxCameraSettings.setMinimumSize(QtCore.QSize(0, 250))
        font = QtGui.QFont()
        font.setFamily("Berlin Sans FB")
        font.setPointSize(12)
        self.groupBoxCameraSettings.setFont(font)
        self.groupBoxCameraSettings.setStyleSheet("")
        self.groupBoxCameraSettings.setObjectName("groupBoxCameraSettings")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.groupBoxCameraSettings)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(19, 29, 361, 181))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.spinBoxExposure = QtWidgets.QSpinBox(self.gridLayoutWidget_3)
        self.spinBoxExposure.setMinimumSize(QtCore.QSize(70, 0))
        self.spinBoxExposure.setObjectName("spinBoxExposure")
        self.gridLayout_3.addWidget(self.spinBoxExposure, 1, 2, 1, 1)
        self.sliderExposure = QtWidgets.QSlider(self.gridLayoutWidget_3)
        self.sliderExposure.setOrientation(QtCore.Qt.Horizontal)
        self.sliderExposure.setObjectName("sliderExposure")
        self.gridLayout_3.addWidget(self.sliderExposure, 1, 1, 1, 1)
        self.labelExposure = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.labelExposure.setObjectName("labelExposure")
        self.gridLayout_3.addWidget(self.labelExposure, 1, 0, 1, 1)
        self.labelImageFormat = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.labelImageFormat.setObjectName("labelImageFormat")
        self.gridLayout_3.addWidget(self.labelImageFormat, 0, 0, 1, 1)
        self.comboImageFormat = QtWidgets.QComboBox(self.gridLayoutWidget_3)
        self.comboImageFormat.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.comboImageFormat.setObjectName("comboImageFormat")
        self.gridLayout_3.addWidget(self.comboImageFormat, 0, 1, 1, 1)
        self.verticalLayoutExperimentControl.addWidget(self.groupBoxCameraSettings)
        self.verticalLayout_AcquisitionControl = QtWidgets.QVBoxLayout()
        self.verticalLayout_AcquisitionControl.setObjectName("verticalLayout_AcquisitionControl")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.buttonAcquire = QtWidgets.QPushButton(self.verticalLayoutWidget_6)
        self.buttonAcquire.setMinimumSize(QtCore.QSize(0, 50))
        self.buttonAcquire.setObjectName("buttonAcquire")
        self.horizontalLayout.addWidget(self.buttonAcquire)
        self.buttonSnap = QtWidgets.QPushButton(self.verticalLayoutWidget_6)
        self.buttonSnap.setMinimumSize(QtCore.QSize(0, 50))
        self.buttonSnap.setStyleSheet("color: rgb(255, 255, 255);\n"
"border-left-color: rgb(255, 255, 255);\n"
"background-color: rgb(100, 100, 100);")
        self.buttonSnap.setObjectName("buttonSnap")
        self.horizontalLayout.addWidget(self.buttonSnap)
        self.buttonStop = QtWidgets.QPushButton(self.verticalLayoutWidget_6)
        self.buttonStop.setEnabled(False)
        self.buttonStop.setMinimumSize(QtCore.QSize(0, 50))
        self.buttonStop.setStyleSheet("")
        self.buttonStop.setObjectName("buttonStop")
        self.horizontalLayout.addWidget(self.buttonStop)
        self.verticalLayout_AcquisitionControl.addLayout(self.horizontalLayout)
        self.buttonSave = QtWidgets.QPushButton(self.verticalLayoutWidget_6)
        self.buttonSave.setMinimumSize(QtCore.QSize(120, 50))
        self.buttonSave.setMaximumSize(QtCore.QSize(150, 16777215))
        self.buttonSave.setObjectName("buttonSave")
        self.verticalLayout_AcquisitionControl.addWidget(self.buttonSave, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayoutExperimentControl.addLayout(self.verticalLayout_AcquisitionControl)
        self.groupBoxPALMAcquisition = QtWidgets.QGroupBox(self.verticalLayoutWidget_6)
        self.groupBoxPALMAcquisition.setMinimumSize(QtCore.QSize(0, 280))
        font = QtGui.QFont()
        font.setFamily("Berlin Sans FB")
        font.setPointSize(12)
        self.groupBoxPALMAcquisition.setFont(font)
        self.groupBoxPALMAcquisition.setObjectName("groupBoxPALMAcquisition")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.groupBoxPALMAcquisition)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(20, 30, 371, 241))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.layoutPALM = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.layoutPALM.setContentsMargins(0, 0, 0, 0)
        self.layoutPALM.setSpacing(20)
        self.layoutPALM.setObjectName("layoutPALM")
        self.horizontalLayoutPALM = QtWidgets.QHBoxLayout()
        self.horizontalLayoutPALM.setObjectName("horizontalLayoutPALM")
        self.labelImageNumber = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.labelImageNumber.setObjectName("labelImageNumber")
        self.horizontalLayoutPALM.addWidget(self.labelImageNumber)
        self.spinBoxImageNumber = QtWidgets.QSpinBox(self.verticalLayoutWidget_4)
        self.spinBoxImageNumber.setObjectName("spinBoxImageNumber")
        self.horizontalLayoutPALM.addWidget(self.spinBoxImageNumber)
        self.pushButtonAcquirePALMSingle = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.pushButtonAcquirePALMSingle.setObjectName("pushButtonAcquirePALMSingle")
        self.horizontalLayoutPALM.addWidget(self.pushButtonAcquirePALMSingle)
        self.layoutPALM.addLayout(self.horizontalLayoutPALM)
        self.verticalLayoutPALMCLEM = QtWidgets.QVBoxLayout()
        self.verticalLayoutPALMCLEM.setSpacing(6)
        self.verticalLayoutPALMCLEM.setObjectName("verticalLayoutPALMCLEM")
        self.labelFile = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.labelFile.setObjectName("labelFile")
        self.verticalLayoutPALMCLEM.addWidget(self.labelFile)
        self.filePath = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        self.filePath.setObjectName("filePath")
        self.verticalLayoutPALMCLEM.addWidget(self.filePath)
        self.pushButtonBrowse = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.pushButtonBrowse.setObjectName("pushButtonBrowse")
        self.verticalLayoutPALMCLEM.addWidget(self.pushButtonBrowse)
        self.pushButtonAcquirePALMSequence = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.pushButtonAcquirePALMSequence.setEnabled(True)
        self.pushButtonAcquirePALMSequence.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButtonAcquirePALMSequence.setMaximumSize(QtCore.QSize(200, 16777215))
        self.pushButtonAcquirePALMSequence.setObjectName("pushButtonAcquirePALMSequence")
        self.verticalLayoutPALMCLEM.addWidget(self.pushButtonAcquirePALMSequence, 0, QtCore.Qt.AlignHCenter)
        self.layoutPALM.addLayout(self.verticalLayoutPALMCLEM)
        self.horizontalLayoutProgress = QtWidgets.QHBoxLayout()
        self.horizontalLayoutProgress.setObjectName("horizontalLayoutProgress")
        self.labelProgress = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.labelProgress.setObjectName("labelProgress")
        self.horizontalLayoutProgress.addWidget(self.labelProgress)
        self.layoutPALM.addLayout(self.horizontalLayoutProgress)
        self.verticalLayoutExperimentControl.addWidget(self.groupBoxPALMAcquisition)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 2350, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionLasers_Control = QtWidgets.QAction(MainWindow)
        self.actionLasers_Control.setObjectName("actionLasers_Control")
        self.actionAutoFocus = QtWidgets.QAction(MainWindow)
        self.actionAutoFocus.setObjectName("actionAutoFocus")
        self.menuFile.addAction(self.actionExit)
        self.menuTools.addAction(self.actionLasers_Control)
        self.menuTools.addAction(self.actionAutoFocus)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidgetMethod.setCurrentIndex(0)
        self.sliderFieldBF.sliderMoved['int'].connect(self.spinBoxFieldBF.setValue)
        self.spinBoxApertureBF.valueChanged['int'].connect(self.sliderApertureBF.setValue)
        self.spinBoxIntensityBF.valueChanged['int'].connect(self.sliderIntensityBF.setValue)
        self.spinBoxFieldBF.valueChanged['int'].connect(self.sliderFieldBF.setValue)
        self.sliderIntensityBF.valueChanged['int'].connect(self.spinBoxIntensityBF.setValue)
        self.sliderApertureBF.sliderMoved['int'].connect(self.spinBoxApertureBF.setValue)
        self.spinBoxExposure.valueChanged['int'].connect(self.sliderExposure.setValue)
        self.sliderExposure.valueChanged['int'].connect(self.spinBoxExposure.setValue)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBoxLasersSettings.setTitle(_translate("MainWindow", "Lasers Control"))
        self.label488.setText(_translate("MainWindow", "488 nm"))
        self.label405.setText(_translate("MainWindow", "405 nm"))
        self.label561.setText(_translate("MainWindow", "561 nm"))
        self.pushButtonBlank.setText(_translate("MainWindow", "Blank"))
        self.groupBoxAF.setTitle(_translate("MainWindow", "AutoFocus"))
        self.pushButtonFindFocus.setText(_translate("MainWindow", "Find Focus"))
        self.labelStepNumber.setText(_translate("MainWindow", "Step number"))
        self.labelZRange.setText(_translate("MainWindow", "Z range (µm)"))
        self.labelStepSize.setText(_translate("MainWindow", "Step Size (µm)"))
        self.pushZoom.setText(_translate("MainWindow", "Zoom"))
        self.pushButtonSetROI.setText(_translate("MainWindow", "Set ROI"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.labelMinimum.setText(_translate("MainWindow", "Minimum"))
        self.labelMaximum.setText(_translate("MainWindow", "Maximum"))
        self.pushButtonAuto.setText(_translate("MainWindow", "Auto"))
        self.labelMicroscopeSettings.setText(_translate("MainWindow", "Microscope Settings"))
        self.labelShutterBF.setText(_translate("MainWindow", "Shutter"))
        self.buttonShutterBF.setText(_translate("MainWindow", "TL-Shutter"))
        self.labelApertureBF.setText(_translate("MainWindow", "Aperture"))
        self.labelIntensityBF.setText(_translate("MainWindow", "Intensity"))
        self.labelLight.setText(_translate("MainWindow", "Light"))
        self.labelFieldBF.setText(_translate("MainWindow", "Field"))
        self.pushButton.setText(_translate("MainWindow", "State"))
        self.labelLightState.setText(_translate("MainWindow", "Off"))
        self.labelShutterBFState.setText(_translate("MainWindow", "Closed"))
        self.tabWidgetMethod.setTabText(self.tabWidgetMethod.indexOf(self.TLBF), _translate("MainWindow", "TL BF"))
        self.labelShutterIL.setText(_translate("MainWindow", "Shutter"))
        self.buttonShuterIL.setText(_translate("MainWindow", "IL-Shutter"))
        self.LabelFilter.setText(_translate("MainWindow", "Filter"))
        self.labelShutterILState.setText(_translate("MainWindow", "Closed"))
        self.tabWidgetMethod.setTabText(self.tabWidgetMethod.indexOf(self.FLUO), _translate("MainWindow", "FLUO"))
        self.groupBoxCameraSettings.setTitle(_translate("MainWindow", "Camera Settings"))
        self.labelExposure.setText(_translate("MainWindow", "Exposure [ms]"))
        self.labelImageFormat.setText(_translate("MainWindow", "Image Format"))
        self.buttonAcquire.setText(_translate("MainWindow", "Acquire"))
        self.buttonSnap.setText(_translate("MainWindow", "Snap"))
        self.buttonStop.setText(_translate("MainWindow", "Stop"))
        self.buttonSave.setText(_translate("MainWindow", "PushButton"))
        self.groupBoxPALMAcquisition.setTitle(_translate("MainWindow", "PALM Acquisition"))
        self.labelImageNumber.setText(_translate("MainWindow", "Image number"))
        self.pushButtonAcquirePALMSingle.setText(_translate("MainWindow", "Single"))
        self.labelFile.setText(_translate("MainWindow", "SerialEM file:"))
        self.pushButtonBrowse.setText(_translate("MainWindow", "Browse..."))
        self.pushButtonAcquirePALMSequence.setText(_translate("MainWindow", "Acquire Serial EM Sequence"))
        self.labelProgress.setText(_translate("MainWindow", "TextLabel"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionLasers_Control.setText(_translate("MainWindow", "Lasers Control"))
        self.actionAutoFocus.setText(_translate("MainWindow", "AutoFocus"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
