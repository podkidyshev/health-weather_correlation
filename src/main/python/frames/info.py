# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/ui/frame_info.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FrameInfo(object):
    def setupUi(self, FrameInfo):
        FrameInfo.setObjectName("FrameInfo")
        FrameInfo.resize(620, 579)
        FrameInfo.setMinimumSize(QtCore.QSize(620, 380))
        self.verticalLayout = QtWidgets.QVBoxLayout(FrameInfo)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabs = QtWidgets.QTabWidget(FrameInfo)
        self.tabs.setObjectName("tabs")
        self.tab_info_0 = QtWidgets.QWidget()
        self.tab_info_0.setObjectName("tab_info_0")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab_info_0)
        self.verticalLayout_7.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.tabs.addTab(self.tab_info_0, "")
        self.tab_info_1 = QtWidgets.QWidget()
        self.tab_info_1.setObjectName("tab_info_1")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_info_1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tabs.addTab(self.tab_info_1, "")
        self.tab_info_2 = QtWidgets.QWidget()
        self.tab_info_2.setObjectName("tab_info_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_info_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.tabs.addTab(self.tab_info_2, "")
        self.verticalLayout.addWidget(self.tabs)

        self.retranslateUi(FrameInfo)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FrameInfo)

    def retranslateUi(self, FrameInfo):
        _translate = QtCore.QCoreApplication.translate
        FrameInfo.setWindowTitle(_translate("FrameInfo", "Frame"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_info_0), _translate("FrameInfo", "Визуализация"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_info_1), _translate("FrameInfo", "Статистика"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_info_2), _translate("FrameInfo", "Тестирование нормальности"))

