# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/ui/utils/standard_type.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FrameStandardType(object):
    def setupUi(self, FrameStandardType):
        FrameStandardType.setObjectName("FrameStandardType")
        FrameStandardType.resize(620, 579)
        FrameStandardType.setMinimumSize(QtCore.QSize(620, 380))
        self.verticalLayout = QtWidgets.QVBoxLayout(FrameStandardType)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabs = QtWidgets.QTabWidget(FrameStandardType)
        self.tabs.setObjectName("tabs")
        self.tab_info_0 = QtWidgets.QWidget()
        self.tab_info_0.setObjectName("tab_info_0")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab_info_0)
        self.verticalLayout_7.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.tabs.addTab(self.tab_info_0, "")
        self.tab_info_1 = QtWidgets.QWidget()
        self.tab_info_1.setObjectName("tab_info_1")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_info_1)
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tabs.addTab(self.tab_info_1, "")
        self.verticalLayout.addWidget(self.tabs)

        self.retranslateUi(FrameStandardType)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FrameStandardType)

    def retranslateUi(self, FrameStandardType):
        _translate = QtCore.QCoreApplication.translate
        FrameStandardType.setWindowTitle(_translate("FrameStandardType", "Frame"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_info_0), _translate("FrameStandardType", "Значения"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_info_1), _translate("FrameStandardType", "Амплитуды"))

