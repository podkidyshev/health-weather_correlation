# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/ui/frame_combo.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FrameCombo(object):
    def setupUi(self, FrameCombo):
        FrameCombo.setObjectName("FrameCombo")
        FrameCombo.resize(482, 520)
        self.verticalLayout = QtWidgets.QVBoxLayout(FrameCombo)
        self.verticalLayout.setObjectName("verticalLayout")
        self.combo = QtWidgets.QComboBox(FrameCombo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo.sizePolicy().hasHeightForWidth())
        self.combo.setSizePolicy(sizePolicy)
        self.combo.setMinimumSize(QtCore.QSize(200, 0))
        self.combo.setObjectName("combo")
        self.verticalLayout.addWidget(self.combo)

        self.retranslateUi(FrameCombo)
        QtCore.QMetaObject.connectSlotsByName(FrameCombo)

    def retranslateUi(self, FrameCombo):
        _translate = QtCore.QCoreApplication.translate
        FrameCombo.setWindowTitle(_translate("FrameCombo", "Frame"))

