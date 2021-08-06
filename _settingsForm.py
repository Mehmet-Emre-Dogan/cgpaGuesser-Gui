# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingsForm.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.resize(453, 365)
        Settings.setStyleSheet("*{\n"
"    background-color: rgb(90, 90, 90);\n"
"    color: white;\n"
"}\n"
"QSpinBox::Disabled{\n"
"    background-color: rgb(30, 30, 30);\n"
"}\n"
"QGroupBox{\n"
"    border: 1px solid rgb(70, 70, 70);\n"
"    margin-top: 0.5em;\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QGroupBox::title {\n"
"    background-color: rgb(90, 90, 90);\n"
"    top: -10px;\n"
"    left: 10px;\n"
"}\n"
"QPushButton:disabled {\n"
"background-color:rgb(30, 30, 30);\n"
"}\n"
"QScrollArea{\n"
"    border: none;\n"
"}\n"
"QScrollBar:vertical {\n"
"    border: 1px solid rgb(50, 50, 50);\n"
"    width: 15px;\n"
"    padding-top: 15px;\n"
"    padding-bottom: 15px;\n"
"}\n"
"QScrollBar::handle:vertical {\n"
"    background: silver;\n"
"}\n"
"")
        self.centralwidget = QtWidgets.QWidget(Settings)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 421, 301))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 30, 401, 121))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioRememberWinHei = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioRememberWinHei.setFont(font)
        self.radioRememberWinHei.setObjectName("radioRememberWinHei")
        self.verticalLayout.addWidget(self.radioRememberWinHei)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.radioForceWinHei = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioForceWinHei.setFont(font)
        self.radioForceWinHei.setObjectName("radioForceWinHei")
        self.verticalLayout.addWidget(self.radioForceWinHei)
        self.spinBoxWindowHeight = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.spinBoxWindowHeight.setFont(font)
        self.spinBoxWindowHeight.setMaximum(999999999)
        self.spinBoxWindowHeight.setObjectName("spinBoxWindowHeight")
        self.verticalLayout.addWidget(self.spinBoxWindowHeight)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.btnSavePrefs = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSavePrefs.sizePolicy().hasHeightForWidth())
        self.btnSavePrefs.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnSavePrefs.setFont(font)
        self.btnSavePrefs.setObjectName("btnSavePrefs")
        self.horizontalLayout.addWidget(self.btnSavePrefs)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        Settings.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Settings)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 453, 21))
        self.menubar.setObjectName("menubar")
        Settings.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Settings)
        self.statusbar.setObjectName("statusbar")
        Settings.setStatusBar(self.statusbar)

        self.retranslateUi(Settings)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "MainWindow"))
        self.groupBox.setTitle(_translate("Settings", "Resolution"))
        self.radioRememberWinHei.setText(_translate("Settings", "Remember window height"))
        self.radioForceWinHei.setText(_translate("Settings", "Force the window height to value:"))
        self.btnSavePrefs.setText(_translate("Settings", "Save Preferences"))
