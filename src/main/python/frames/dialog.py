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
        DialogGroup.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(DialogGroup)
        self.verticalLayout.setObjectName("verticalLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogGroup)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DialogGroup)
        self.buttonBox.accepted.connect(DialogGroup.accept)
        self.buttonBox.rejected.connect(DialogGroup.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogGroup)

    def retranslateUi(self, DialogGroup):
        _translate = QtCore.QCoreApplication.translate
        DialogGroup.setWindowTitle(_translate("DialogGroup", "Dialog"))

