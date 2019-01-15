# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/ui/frame_std_mul_samples.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FrameStdMulSamples(object):
    def setupUi(self, FrameStdMulSamples):
        FrameStdMulSamples.setObjectName("FrameStdMulSamples")
        FrameStdMulSamples.resize(725, 498)
        self.horizontalLayout = QtWidgets.QHBoxLayout(FrameStdMulSamples)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.layout_vertical = QtWidgets.QVBoxLayout()
        self.layout_vertical.setObjectName("layout_vertical")
        self.title_label = QtWidgets.QLabel(FrameStdMulSamples)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.title_label.setFont(font)
        self.title_label.setObjectName("title_label")
        self.layout_vertical.addWidget(self.title_label)
        self.tabs = QtWidgets.QTabWidget(FrameStdMulSamples)
        self.tabs.setObjectName("tabs")
        self.tab_main = QtWidgets.QWidget()
        self.tab_main.setObjectName("tab_main")
        self.tabs.addTab(self.tab_main, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabs.addTab(self.tab_2, "")
        self.layout_vertical.addWidget(self.tabs)
        self.horizontalLayout.addLayout(self.layout_vertical)

        self.retranslateUi(FrameStdMulSamples)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FrameStdMulSamples)

    def retranslateUi(self, FrameStdMulSamples):
        _translate = QtCore.QCoreApplication.translate
        FrameStdMulSamples.setWindowTitle(_translate("FrameStdMulSamples", "Frame"))
        self.title_label.setText(_translate("FrameStdMulSamples", "Dolor amet"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_main), _translate("FrameStdMulSamples", "Tab 1"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_2), _translate("FrameStdMulSamples", "Tab 2"))

