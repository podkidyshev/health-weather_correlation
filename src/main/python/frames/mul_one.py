# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/ui/frame_mul_one.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FrameMulOne(object):
    def setupUi(self, FrameMulOne):
        FrameMulOne.setObjectName("FrameMulOne")
        FrameMulOne.resize(725, 498)
        self.horizontalLayout = QtWidgets.QHBoxLayout(FrameMulOne)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.layout_vertical = QtWidgets.QVBoxLayout()
        self.layout_vertical.setObjectName("layout_vertical")
        self.title_label = QtWidgets.QLabel(FrameMulOne)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.title_label.setFont(font)
        self.title_label.setObjectName("title_label")
        self.layout_vertical.addWidget(self.title_label)
        self.tabs = QtWidgets.QTabWidget(FrameMulOne)
        self.tabs.setObjectName("tabs")
        self.tab_main = QtWidgets.QWidget()
        self.tab_main.setObjectName("tab_main")
        self.tabs.addTab(self.tab_main, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabs.addTab(self.tab_2, "")
        self.layout_vertical.addWidget(self.tabs)
        self.horizontalLayout.addLayout(self.layout_vertical)

        self.retranslateUi(FrameMulOne)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FrameMulOne)

    def retranslateUi(self, FrameMulOne):
        _translate = QtCore.QCoreApplication.translate
        FrameMulOne.setWindowTitle(_translate("FrameMulOne", "Frame"))
        self.title_label.setText(_translate("FrameMulOne", "Dolor amet"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_main), _translate("FrameMulOne", "Tab 1"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_2), _translate("FrameMulOne", "Tab 2"))

