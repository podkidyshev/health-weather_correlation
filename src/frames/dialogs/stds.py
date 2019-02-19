# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/ui/dialogs/stds.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogStds(object):
    def setupUi(self, DialogStds):
        DialogStds.setObjectName("DialogStds")
        DialogStds.setWindowModality(QtCore.Qt.WindowModal)
        DialogStds.resize(300, 252)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogStds.sizePolicy().hasHeightForWidth())
        DialogStds.setSizePolicy(sizePolicy)
        DialogStds.setMinimumSize(QtCore.QSize(250, 0))
        DialogStds.setMaximumSize(QtCore.QSize(300, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(DialogStds)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.layout_stds = QtWidgets.QVBoxLayout()
        self.layout_stds.setObjectName("layout_stds")
        self.horizontalLayout.addLayout(self.layout_stds)
        self.group_box = QtWidgets.QGroupBox(DialogStds)
        self.group_box.setTitle("")
        self.group_box.setObjectName("group_box")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.group_box)
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.btn_all = QtWidgets.QRadioButton(self.group_box)
        self.btn_all.setObjectName("btn_all")
        self.verticalLayout_3.addWidget(self.btn_all)
        self.btn_0 = QtWidgets.QRadioButton(self.group_box)
        self.btn_0.setObjectName("btn_0")
        self.verticalLayout_3.addWidget(self.btn_0)
        self.btn_1 = QtWidgets.QRadioButton(self.group_box)
        self.btn_1.setObjectName("btn_1")
        self.verticalLayout_3.addWidget(self.btn_1)
        self.btn_2 = QtWidgets.QRadioButton(self.group_box)
        self.btn_2.setObjectName("btn_2")
        self.verticalLayout_3.addWidget(self.btn_2)
        self.btn_3 = QtWidgets.QRadioButton(self.group_box)
        self.btn_3.setObjectName("btn_3")
        self.verticalLayout_3.addWidget(self.btn_3)
        self.horizontalLayout.addWidget(self.group_box)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttons = QtWidgets.QDialogButtonBox(DialogStds)
        self.buttons.setOrientation(QtCore.Qt.Horizontal)
        self.buttons.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttons.setCenterButtons(True)
        self.buttons.setObjectName("buttons")
        self.verticalLayout.addWidget(self.buttons)

        self.retranslateUi(DialogStds)
        self.buttons.accepted.connect(DialogStds.accept)
        self.buttons.rejected.connect(DialogStds.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogStds)

    def retranslateUi(self, DialogStds):
        _translate = QtCore.QCoreApplication.translate
        DialogStds.setWindowTitle(_translate("DialogStds", "Групповой отчет"))
        self.btn_all.setText(_translate("DialogStds", "Все факторы"))
        self.btn_0.setText(_translate("DialogStds", "Без нагрузки"))
        self.btn_1.setText(_translate("DialogStds", "С физической нагрузкой"))
        self.btn_2.setText(_translate("DialogStds", "С эмоциональной нагрузкой"))
        self.btn_3.setText(_translate("DialogStds", "После отдыха"))

