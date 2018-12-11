# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\main\python\ui\frame_default.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FrameDefault(object):
    def setupUi(self, FrameDefault):
        FrameDefault.setObjectName("FrameDefault")
        FrameDefault.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(FrameDefault)
        self.verticalLayout.setObjectName("verticalLayout")
        self.instructions_edit = QtWidgets.QPlainTextEdit(FrameDefault)
        self.instructions_edit.setEnabled(False)
        self.instructions_edit.setObjectName("instructions_edit")
        self.verticalLayout.addWidget(self.instructions_edit)

        self.retranslateUi(FrameDefault)
        QtCore.QMetaObject.connectSlotsByName(FrameDefault)

    def retranslateUi(self, FrameDefault):
        _translate = QtCore.QCoreApplication.translate
        FrameDefault.setWindowTitle(_translate("FrameDefault", "Frame"))
        self.instructions_edit.setPlaceholderText(_translate("FrameDefault", "Здесь можно написать краткую инструкцию и (связь с разработчиками)"))

