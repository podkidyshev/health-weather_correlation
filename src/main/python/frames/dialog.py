# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/ui/dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogGroup(object):
    def setupUi(self, DialogGroup):
        DialogGroup.setObjectName("DialogGroup")
        DialogGroup.setWindowModality(QtCore.Qt.WindowModal)
        DialogGroup.resize(250, 41)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogGroup.sizePolicy().hasHeightForWidth())
        DialogGroup.setSizePolicy(sizePolicy)
        DialogGroup.setMinimumSize(QtCore.QSize(250, 0))
        DialogGroup.setMaximumSize(QtCore.QSize(300, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(DialogGroup)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.buttons = QtWidgets.QDialogButtonBox(DialogGroup)
        self.buttons.setOrientation(QtCore.Qt.Horizontal)
        self.buttons.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttons.setCenterButtons(True)
        self.buttons.setObjectName("buttons")
        self.verticalLayout.addWidget(self.buttons)

        self.retranslateUi(DialogGroup)
        self.buttons.accepted.connect(DialogGroup.accept)
        self.buttons.rejected.connect(DialogGroup.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogGroup)

    def retranslateUi(self, DialogGroup):
        _translate = QtCore.QCoreApplication.translate
        DialogGroup.setWindowTitle(_translate("DialogGroup", "Групповой отчет"))

