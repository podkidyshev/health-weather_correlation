# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/ui/frame_group.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FrameGroup(object):
    def setupUi(self, FrameGroup):
        FrameGroup.setObjectName("FrameGroup")
        FrameGroup.resize(120, 519)
        FrameGroup.setMinimumSize(QtCore.QSize(120, 0))
        FrameGroup.setMaximumSize(QtCore.QSize(120, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(FrameGroup)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scroll = QtWidgets.QScrollArea(FrameGroup)
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName("scroll")
        self.scroll_contents = QtWidgets.QWidget()
        self.scroll_contents.setGeometry(QtCore.QRect(0, 0, 100, 499))
        self.scroll_contents.setObjectName("scroll_contents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scroll_contents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scroll.setWidget(self.scroll_contents)
        self.verticalLayout.addWidget(self.scroll)

        self.retranslateUi(FrameGroup)
        QtCore.QMetaObject.connectSlotsByName(FrameGroup)

    def retranslateUi(self, FrameGroup):
        _translate = QtCore.QCoreApplication.translate
        FrameGroup.setWindowTitle(_translate("FrameGroup", "Frame"))

