# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/main/python/ui/frame_standard_factor.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FrameStandardFactor(object):
    def setupUi(self, FrameStandardFactor):
        FrameStandardFactor.setObjectName("FrameStandardFactor")
        FrameStandardFactor.resize(581, 610)
        self.verticalLayout = QtWidgets.QVBoxLayout(FrameStandardFactor)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(FrameStandardFactor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 561, 590))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.text_edit_1 = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_edit_1.sizePolicy().hasHeightForWidth())
        self.text_edit_1.setSizePolicy(sizePolicy)
        self.text_edit_1.setMinimumSize(QtCore.QSize(100, 200))
        self.text_edit_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.text_edit_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.text_edit_1.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.text_edit_1.setReadOnly(True)
        self.text_edit_1.setObjectName("text_edit_1")
        self.verticalLayout_2.addWidget(self.text_edit_1)
        self.label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_1.sizePolicy().hasHeightForWidth())
        self.label_1.setSizePolicy(sizePolicy)
        self.label_1.setObjectName("label_1")
        self.verticalLayout_2.addWidget(self.label_1)
        self.text_edit_2 = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        self.text_edit_2.setObjectName("text_edit_2")
        self.verticalLayout_2.addWidget(self.text_edit_2)
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(FrameStandardFactor)
        QtCore.QMetaObject.connectSlotsByName(FrameStandardFactor)

    def retranslateUi(self, FrameStandardFactor):
        _translate = QtCore.QCoreApplication.translate
        FrameStandardFactor.setWindowTitle(_translate("FrameStandardFactor", "Frame"))
        self.label_1.setText(_translate("FrameStandardFactor", "TextLabel"))
        self.label_2.setText(_translate("FrameStandardFactor", "TextLabel"))

