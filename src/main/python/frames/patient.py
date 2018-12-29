# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/ui/frame_patient.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FramePatient(object):
    def setupUi(self, FramePatient):
        FramePatient.setObjectName("FramePatient")
        FramePatient.resize(620, 380)
        FramePatient.setMinimumSize(QtCore.QSize(620, 380))
        self.verticalLayout = QtWidgets.QVBoxLayout(FramePatient)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.std_pat_label = QtWidgets.QLabel(FramePatient)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.std_pat_label.setFont(font)
        self.std_pat_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.std_pat_label.setObjectName("std_pat_label")
        self.verticalLayout.addWidget(self.std_pat_label)
        self.tabs = QtWidgets.QTabWidget(FramePatient)
        self.tabs.setObjectName("tabs")
        self.tab_factors = QtWidgets.QWidget()
        self.tab_factors.setObjectName("tab_factors")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_factors)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.factors_label = QtWidgets.QLabel(self.tab_factors)
        self.factors_label.setText("")
        self.factors_label.setObjectName("factors_label")
        self.verticalLayout_2.addWidget(self.factors_label)
        self.tabs.addTab(self.tab_factors, "")
        self.tab_factor_0 = QtWidgets.QWidget()
        self.tab_factor_0.setObjectName("tab_factor_0")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_factor_0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_0 = QtWidgets.QLabel(self.tab_factor_0)
        self.label_0.setObjectName("label_0")
        self.verticalLayout_3.addWidget(self.label_0)
        self.tabs.addTab(self.tab_factor_0, "")
        self.tab_factor_1 = QtWidgets.QWidget()
        self.tab_factor_1.setObjectName("tab_factor_1")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_factor_1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_1 = QtWidgets.QLabel(self.tab_factor_1)
        self.label_1.setObjectName("label_1")
        self.verticalLayout_4.addWidget(self.label_1)
        self.tabs.addTab(self.tab_factor_1, "")
        self.tab_factor_2 = QtWidgets.QWidget()
        self.tab_factor_2.setObjectName("tab_factor_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_factor_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.tab_factor_2)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_5.addWidget(self.label_2)
        self.tabs.addTab(self.tab_factor_2, "")
        self.tab_factor_3 = QtWidgets.QWidget()
        self.tab_factor_3.setObjectName("tab_factor_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_factor_3)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_3 = QtWidgets.QLabel(self.tab_factor_3)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_6.addWidget(self.label_3)
        self.tabs.addTab(self.tab_factor_3, "")
        self.verticalLayout.addWidget(self.tabs)

        self.retranslateUi(FramePatient)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FramePatient)

    def retranslateUi(self, FramePatient):
        _translate = QtCore.QCoreApplication.translate
        FramePatient.setWindowTitle(_translate("FramePatient", "Frame"))
        self.std_pat_label.setText(_translate("FramePatient", "Статистика"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_factors), _translate("FramePatient", "Все факторы"))
        self.label_0.setText(_translate("FramePatient", "TextLabel"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_factor_0), _translate("FramePatient", "Без нагрузки"))
        self.label_1.setText(_translate("FramePatient", "TextLabel"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_factor_1), _translate("FramePatient", "После физической"))
        self.label_2.setText(_translate("FramePatient", "TextLabel"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_factor_2), _translate("FramePatient", "После эмоциональной"))
        self.label_3.setText(_translate("FramePatient", "TextLabel"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_factor_3), _translate("FramePatient", "После отдыха"))

