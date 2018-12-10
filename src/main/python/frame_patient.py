# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\main\python\ui\frame_patient.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FramePatient(object):
    def setupUi(self, FramePatient):
        FramePatient.setObjectName("FramePatient")
        FramePatient.resize(491, 342)
        self.verticalLayout = QtWidgets.QVBoxLayout(FramePatient)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabs = QtWidgets.QTabWidget(FramePatient)
        self.tabs.setObjectName("tabs")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabs.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabs.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabs)

        self.retranslateUi(FramePatient)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FramePatient)

    def retranslateUi(self, FramePatient):
        _translate = QtCore.QCoreApplication.translate
        FramePatient.setWindowTitle(_translate("FramePatient", "Frame"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab), _translate("FramePatient", "Tab 1"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_2), _translate("FramePatient", "Tab 2"))

