# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/ui/sample.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FramePatient(object):
    def setupUi(self, FramePatient):
        FramePatient.setObjectName("FramePatient")
        FramePatient.resize(620, 579)
        FramePatient.setMinimumSize(QtCore.QSize(620, 380))
        self.verticalLayout = QtWidgets.QVBoxLayout(FramePatient)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title_label = QtWidgets.QLabel(FramePatient)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.title_label.setFont(font)
        self.title_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.title_label.setObjectName("title_label")
        self.verticalLayout.addWidget(self.title_label)
        self.tabs = QtWidgets.QTabWidget(FramePatient)
        self.tabs.setObjectName("tabs")
        self.tab_factors = QtWidgets.QWidget()
        self.tab_factors.setObjectName("tab_factors")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_factors)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabs.addTab(self.tab_factors, "")
        self.tab_factor_0 = QtWidgets.QWidget()
        self.tab_factor_0.setObjectName("tab_factor_0")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab_factor_0)
        self.verticalLayout_7.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.tabs.addTab(self.tab_factor_0, "")
        self.tab_factor_1 = QtWidgets.QWidget()
        self.tab_factor_1.setObjectName("tab_factor_1")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_factor_1)
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tabs.addTab(self.tab_factor_1, "")
        self.tab_factor_2 = QtWidgets.QWidget()
        self.tab_factor_2.setObjectName("tab_factor_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_factor_2)
        self.verticalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.tabs.addTab(self.tab_factor_2, "")
        self.tab_factor_3 = QtWidgets.QWidget()
        self.tab_factor_3.setObjectName("tab_factor_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_factor_3)
        self.verticalLayout_6.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.tabs.addTab(self.tab_factor_3, "")
        self.verticalLayout.addWidget(self.tabs)

        self.retranslateUi(FramePatient)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FramePatient)

    def retranslateUi(self, FramePatient):
        _translate = QtCore.QCoreApplication.translate
        FramePatient.setWindowTitle(_translate("FramePatient", "Frame"))
        self.title_label.setText(_translate("FramePatient", "Статистика"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_factors), _translate("FramePatient", "Все факторы"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_factor_0), _translate("FramePatient", "Без нагрузки"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_factor_1), _translate("FramePatient", "С физической"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_factor_2), _translate("FramePatient", "С эмоциональной"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_factor_3), _translate("FramePatient", "После отдыха"))

