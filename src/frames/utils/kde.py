# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/ui/frame_kde.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FrameKde(object):
    def setupUi(self, FrameKde):
        FrameKde.setObjectName("FrameKde")
        FrameKde.resize(300, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FrameKde.sizePolicy().hasHeightForWidth())
        FrameKde.setSizePolicy(sizePolicy)
        FrameKde.setMinimumSize(QtCore.QSize(300, 300))
        self.verticalLayout = QtWidgets.QVBoxLayout(FrameKde)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabs = QtWidgets.QTabWidget(FrameKde)
        self.tabs.setObjectName("tabs")
        self.tab_info_0 = QtWidgets.QWidget()
        self.tab_info_0.setObjectName("tab_info_0")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab_info_0)
        self.verticalLayout_7.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.tabs.addTab(self.tab_info_0, "")
        self.tab_info_1 = QtWidgets.QWidget()
        self.tab_info_1.setObjectName("tab_info_1")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_info_1)
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tabs.addTab(self.tab_info_1, "")
        self.verticalLayout.addWidget(self.tabs)

        self.retranslateUi(FrameKde)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FrameKde)

    def retranslateUi(self, FrameKde):
        _translate = QtCore.QCoreApplication.translate
        FrameKde.setWindowTitle(_translate("FrameKde", "Frame"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_info_0), _translate("FrameKde", "4-х ядерные оценки"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_info_1), _translate("FrameKde", "3-х ядерные оценки"))

