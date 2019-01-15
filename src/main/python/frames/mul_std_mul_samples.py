# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/ui/frame_mul_std_mul_samples.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FrameMulStdMulSamples(object):
    def setupUi(self, FrameMulStdMulSamples):
        FrameMulStdMulSamples.setObjectName("FrameMulStdMulSamples")
        FrameMulStdMulSamples.resize(697, 496)
        self.horizontalLayout = QtWidgets.QHBoxLayout(FrameMulStdMulSamples)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.layout_vertical = QtWidgets.QVBoxLayout()
        self.layout_vertical.setObjectName("layout_vertical")
        self.title_label = QtWidgets.QLabel(FrameMulStdMulSamples)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.title_label.setFont(font)
        self.title_label.setObjectName("title_label")
        self.layout_vertical.addWidget(self.title_label)
        self.tabs = QtWidgets.QTabWidget(FrameMulStdMulSamples)
        self.tabs.setObjectName("tabs")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabs.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabs.addTab(self.tab_2, "")
        self.layout_vertical.addWidget(self.tabs)
        self.horizontalLayout.addLayout(self.layout_vertical)

        self.retranslateUi(FrameMulStdMulSamples)
        QtCore.QMetaObject.connectSlotsByName(FrameMulStdMulSamples)

    def retranslateUi(self, FrameMulStdMulSamples):
        _translate = QtCore.QCoreApplication.translate
        FrameMulStdMulSamples.setWindowTitle(_translate("FrameMulStdMulSamples", "Frame"))
        self.title_label.setText(_translate("FrameMulStdMulSamples", "TextLabel"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab), _translate("FrameMulStdMulSamples", "Tab 1"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_2), _translate("FrameMulStdMulSamples", "Tab 2"))

