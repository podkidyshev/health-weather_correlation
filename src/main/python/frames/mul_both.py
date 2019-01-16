# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/ui/frame_mul_both.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FrameMulBoth(object):
    def setupUi(self, FrameMulBoth):
        FrameMulBoth.setObjectName("FrameMulBoth")
        FrameMulBoth.resize(697, 496)
        self.horizontalLayout = QtWidgets.QHBoxLayout(FrameMulBoth)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.layout_vertical = QtWidgets.QVBoxLayout()
        self.layout_vertical.setObjectName("layout_vertical")
        self.title_label = QtWidgets.QLabel(FrameMulBoth)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.title_label.setFont(font)
        self.title_label.setObjectName("title_label")
        self.layout_vertical.addWidget(self.title_label)
        self.tabs = QtWidgets.QTabWidget(FrameMulBoth)
        self.tabs.setObjectName("tabs")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabs.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabs.addTab(self.tab_2, "")
        self.layout_vertical.addWidget(self.tabs)
        self.horizontalLayout.addLayout(self.layout_vertical)

        self.retranslateUi(FrameMulBoth)
        QtCore.QMetaObject.connectSlotsByName(FrameMulBoth)

    def retranslateUi(self, FrameMulBoth):
        _translate = QtCore.QCoreApplication.translate
        FrameMulBoth.setWindowTitle(_translate("FrameMulBoth", "Frame"))
        self.title_label.setText(_translate("FrameMulBoth", "TextLabel"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab), _translate("FrameMulBoth", "Tab 1"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_2), _translate("FrameMulBoth", "Tab 2"))

