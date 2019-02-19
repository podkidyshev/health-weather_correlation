# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main\python/ui/default.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FrameDefault(object):
    def setupUi(self, FrameDefault):
        FrameDefault.setObjectName("FrameDefault")
        FrameDefault.resize(443, 300)
        self.horizontalLayout = QtWidgets.QHBoxLayout(FrameDefault)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.instructions_edit = QtWidgets.QTextEdit(FrameDefault)
        self.instructions_edit.setEnabled(True)
        self.instructions_edit.setReadOnly(True)
        self.instructions_edit.setObjectName("instructions_edit")
        self.horizontalLayout.addWidget(self.instructions_edit)

        self.retranslateUi(FrameDefault)
        QtCore.QMetaObject.connectSlotsByName(FrameDefault)

    def retranslateUi(self, FrameDefault):
        _translate = QtCore.QCoreApplication.translate
        FrameDefault.setWindowTitle(_translate("FrameDefault", "Frame"))

