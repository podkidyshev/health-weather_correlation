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
        self.horizontalLayout.addLayout(self.layout_vertical)

        self.retranslateUi(FrameMulOne)
        QtCore.QMetaObject.connectSlotsByName(FrameMulOne)

    def retranslateUi(self, FrameMulOne):
        _translate = QtCore.QCoreApplication.translate
        FrameMulOne.setWindowTitle(_translate("FrameMulOne", "Frame"))

