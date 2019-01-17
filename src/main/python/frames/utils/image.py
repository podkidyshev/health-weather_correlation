# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/ui/utils/image.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FrameImage(object):
    def setupUi(self, FrameImage):
        FrameImage.setObjectName("FrameImage")
        FrameImage.resize(300, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FrameImage.sizePolicy().hasHeightForWidth())
        FrameImage.setSizePolicy(sizePolicy)
        FrameImage.setMinimumSize(QtCore.QSize(300, 300))
        self.verticalLayout = QtWidgets.QVBoxLayout(FrameImage)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.image = QtWidgets.QLabel(FrameImage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image.sizePolicy().hasHeightForWidth())
        self.image.setSizePolicy(sizePolicy)
        self.image.setObjectName("image")
        self.verticalLayout.addWidget(self.image)

        self.retranslateUi(FrameImage)
        QtCore.QMetaObject.connectSlotsByName(FrameImage)

    def retranslateUi(self, FrameImage):
        _translate = QtCore.QCoreApplication.translate
        FrameImage.setWindowTitle(_translate("FrameImage", "Frame"))
        self.image.setText(_translate("FrameImage", "TextLabel"))

