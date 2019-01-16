# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/ui/frame_check.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FrameCheck(object):
    def setupUi(self, FrameCheck):
        FrameCheck.setObjectName("FrameCheck")
        FrameCheck.resize(120, 519)
        FrameCheck.setMinimumSize(QtCore.QSize(120, 0))
        FrameCheck.setMaximumSize(QtCore.QSize(120, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(FrameCheck)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scroll = QtWidgets.QScrollArea(FrameCheck)
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName("scroll")
        self.scroll_contents = QtWidgets.QWidget()
        self.scroll_contents.setGeometry(QtCore.QRect(0, 0, 100, 499))
        self.scroll_contents.setObjectName("scroll_contents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scroll_contents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scroll.setWidget(self.scroll_contents)
        self.verticalLayout.addWidget(self.scroll)

        self.retranslateUi(FrameCheck)
        QtCore.QMetaObject.connectSlotsByName(FrameCheck)

    def retranslateUi(self, FrameCheck):
        _translate = QtCore.QCoreApplication.translate
        FrameCheck.setWindowTitle(_translate("FrameCheck", "Frame"))

