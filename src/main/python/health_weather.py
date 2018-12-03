# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Github\health-weather_correlation\src\main\python\ui\health_weather.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.resize(1303, 813)
        MainForm.setMinimumSize(QtCore.QSize(0, 0))
        MainForm.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.sample_btn = QtWidgets.QPushButton(MainForm)
        self.sample_btn.setGeometry(QtCore.QRect(10, 770, 111, 31))
        self.sample_btn.setObjectName("sample_btn")
        self.exit_btn = QtWidgets.QPushButton(MainForm)
        self.exit_btn.setGeometry(QtCore.QRect(1190, 770, 111, 31))
        self.exit_btn.setObjectName("exit_btn")
        self.start_btn = QtWidgets.QPushButton(MainForm)
        self.start_btn.setGeometry(QtCore.QRect(1190, 730, 111, 31))
        self.start_btn.setObjectName("start_btn")
        self.sample_line = QtWidgets.QLineEdit(MainForm)
        self.sample_line.setGeometry(QtCore.QRect(130, 770, 1041, 31))
        self.sample_line.setObjectName("sample_line")
        self.tabWidget = QtWidgets.QTabWidget(MainForm)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1301, 721))
        self.tabWidget.setMinimumSize(QtCore.QSize(1301, 721))
        self.tabWidget.setMaximumSize(QtCore.QSize(1301, 721))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.kde_tab = QtWidgets.QWidget()
        self.kde_tab.setObjectName("kde_tab")
        self.kde_image = QtWidgets.QLabel(self.kde_tab)
        self.kde_image.setGeometry(QtCore.QRect(0, 0, 1301, 691))
        self.kde_image.setMinimumSize(QtCore.QSize(0, 0))
        self.kde_image.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.kde_image.setText("")
        self.kde_image.setObjectName("kde_image")
        self.tabWidget.addTab(self.kde_tab, "")
        self.tests_tab = QtWidgets.QWidget()
        self.tests_tab.setObjectName("tests_tab")
        self.tests_image = QtWidgets.QLabel(self.tests_tab)
        self.tests_image.setGeometry(QtCore.QRect(0, 0, 1301, 691))
        self.tests_image.setMinimumSize(QtCore.QSize(0, 0))
        self.tests_image.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tests_image.setText("")
        self.tests_image.setObjectName("tests_image")
        self.tabWidget.addTab(self.tests_tab, "")
        self.table_tab = QtWidgets.QWidget()
        self.table_tab.setObjectName("table_tab")
        self.table_text = QtWidgets.QLabel(self.table_tab)
        self.table_text.setGeometry(QtCore.QRect(0, 0, 1301, 691))
        self.table_text.setMinimumSize(QtCore.QSize(0, 0))
        self.table_text.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.table_text.setText("")
        self.table_text.setObjectName("table_text")
        self.tabWidget.addTab(self.table_tab, "")
        self.standard_line = QtWidgets.QLineEdit(MainForm)
        self.standard_line.setGeometry(QtCore.QRect(130, 730, 1041, 31))
        self.standard_line.setObjectName("standard_line")
        self.standard_btn = QtWidgets.QPushButton(MainForm)
        self.standard_btn.setGeometry(QtCore.QRect(10, 730, 111, 31))
        self.standard_btn.setObjectName("standard_btn")

        self.retranslateUi(MainForm)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "Программа"))
        self.sample_btn.setText(_translate("MainForm", "Выбрать образец"))
        self.exit_btn.setText(_translate("MainForm", "Выход"))
        self.start_btn.setText(_translate("MainForm", "Запуск"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.kde_tab), _translate("MainForm", "Совместный KDE"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tests_tab), _translate("MainForm", "Тесты статистической нормальности"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.table_tab), _translate("MainForm", "Сводная таблица результатов"))
        self.standard_btn.setText(_translate("MainForm", "Выбрать эталон"))

