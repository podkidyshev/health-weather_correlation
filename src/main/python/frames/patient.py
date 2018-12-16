# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/ui/frame_patient.ui'
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
        self.std_pat_label = QtWidgets.QLabel(FramePatient)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.std_pat_label.setFont(font)
        self.std_pat_label.setAlignment(QtCore.Qt.AlignCenter)
        self.std_pat_label.setObjectName("std_pat_label")
        self.verticalLayout.addWidget(self.std_pat_label)
        self.tabs = QtWidgets.QTabWidget(FramePatient)
        self.tabs.setObjectName("tabs")
        self.tab_graphics = QtWidgets.QWidget()
        self.tab_graphics.setObjectName("tab_graphics")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_graphics)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.graph_label = QtWidgets.QLabel(self.tab_graphics)
        self.graph_label.setText("")
        self.graph_label.setObjectName("graph_label")
        self.verticalLayout_2.addWidget(self.graph_label)
        self.tabs.addTab(self.tab_graphics, "")
        self.verticalLayout.addWidget(self.tabs)

        self.retranslateUi(FramePatient)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FramePatient)

    def retranslateUi(self, FramePatient):
        _translate = QtCore.QCoreApplication.translate
        FramePatient.setWindowTitle(_translate("FramePatient", "Frame"))
        self.std_pat_label.setText(_translate("FramePatient", "Статистика"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_graphics), _translate("FramePatient", "График"))

