# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/ui/dialog_factors.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogFactors(object):
    def setupUi(self, DialogFactors):
        DialogFactors.setObjectName("DialogFactors")
        DialogFactors.resize(203, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(DialogFactors)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.group_box = QtWidgets.QGroupBox(DialogFactors)
        self.group_box.setTitle("")
        self.group_box.setObjectName("group_box")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.group_box)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btn_all = QtWidgets.QRadioButton(self.group_box)
        self.btn_all.setObjectName("btn_all")
        self.verticalLayout_2.addWidget(self.btn_all)
        self.btn_0 = QtWidgets.QRadioButton(self.group_box)
        self.btn_0.setObjectName("btn_0")
        self.verticalLayout_2.addWidget(self.btn_0)
        self.btn_1 = QtWidgets.QRadioButton(self.group_box)
        self.btn_1.setObjectName("btn_1")
        self.verticalLayout_2.addWidget(self.btn_1)
        self.btn_2 = QtWidgets.QRadioButton(self.group_box)
        self.btn_2.setObjectName("btn_2")
        self.verticalLayout_2.addWidget(self.btn_2)
        self.btn_3 = QtWidgets.QRadioButton(self.group_box)
        self.btn_3.setObjectName("btn_3")
        self.verticalLayout_2.addWidget(self.btn_3)
        self.verticalLayout.addWidget(self.group_box)
        self.buttons = QtWidgets.QDialogButtonBox(DialogFactors)
        self.buttons.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.buttons.setOrientation(QtCore.Qt.Horizontal)
        self.buttons.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttons.setObjectName("buttons")
        self.verticalLayout.addWidget(self.buttons)

        self.retranslateUi(DialogFactors)
        self.buttons.accepted.connect(DialogFactors.accept)
        self.buttons.rejected.connect(DialogFactors.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogFactors)

    def retranslateUi(self, DialogFactors):
        _translate = QtCore.QCoreApplication.translate
        DialogFactors.setWindowTitle(_translate("DialogFactors", "Dialog"))
        self.btn_all.setText(_translate("DialogFactors", "Все факторы"))
        self.btn_0.setText(_translate("DialogFactors", "Без нагрузки"))
        self.btn_1.setText(_translate("DialogFactors", "С физической нагрузкой"))
        self.btn_2.setText(_translate("DialogFactors", "С эмоциональной нагрузкой"))
        self.btn_3.setText(_translate("DialogFactors", "После отдыха"))

