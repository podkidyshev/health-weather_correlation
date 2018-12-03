from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_health_weather(object):
    def setupUi(self, health_weather):
        health_weather.setObjectName("health_weather")
        health_weather.resize(1304, 807)
        health_weather.setMinimumSize(QtCore.QSize(0, 0))
        health_weather.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.sample_btn = QtWidgets.QPushButton(health_weather)
        self.sample_btn.setGeometry(QtCore.QRect(10, 770, 111, 31))
        self.sample_btn.setObjectName("sample_btn")
        self.exit_btn = QtWidgets.QPushButton(health_weather)
        self.exit_btn.setGeometry(QtCore.QRect(1190, 770, 111, 31))
        self.exit_btn.setObjectName("exit_btn")
        self.start_btn = QtWidgets.QPushButton(health_weather)
        self.start_btn.setGeometry(QtCore.QRect(1190, 730, 111, 31))
        self.start_btn.setObjectName("start_btn")
        self.sample_line = QtWidgets.QLineEdit(health_weather)
        self.sample_line.setGeometry(QtCore.QRect(130, 770, 1041, 31))
        self.sample_line.setObjectName("sample_line")
        self.tabWidget = QtWidgets.QTabWidget(health_weather)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1301, 721))
        self.tabWidget.setMinimumSize(QtCore.QSize(1301, 721))
        self.tabWidget.setMaximumSize(QtCore.QSize(1301, 721))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.kde_tab = QtWidgets.QWidget()
        self.kde_tab.setObjectName("kde_tab")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.kde_tab)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1301, 691))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.kde_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.kde_layout.setContentsMargins(0, 0, 0, 0)
        self.kde_layout.setObjectName("kde_layout")
        self.tabWidget.addTab(self.kde_tab, "")
        self.tests_tab = QtWidgets.QWidget()
        self.tests_tab.setObjectName("tests_tab")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.tests_tab)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 1301, 691))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.tests_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.tests_layout.setContentsMargins(0, 0, 0, 0)
        self.tests_layout.setObjectName("tests_layout")
        self.tabWidget.addTab(self.tests_tab, "")
        self.table_tab = QtWidgets.QWidget()
        self.table_tab.setObjectName("table_tab")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.table_tab)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 1301, 691))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.table_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.table_layout.setContentsMargins(0, 0, 0, 0)
        self.table_layout.setObjectName("table_layout")
        self.tabWidget.addTab(self.table_tab, "")
        self.standard_line = QtWidgets.QLineEdit(health_weather)
        self.standard_line.setGeometry(QtCore.QRect(130, 730, 1041, 31))
        self.standard_line.setObjectName("standard_line")
        self.standard_btn = QtWidgets.QPushButton(health_weather)
        self.standard_btn.setGeometry(QtCore.QRect(10, 730, 111, 31))
        self.standard_btn.setObjectName("standard_btn")

        self.retranslateUi(health_weather)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(health_weather)

    def retranslateUi(self, health_weather):
        _translate = QtCore.QCoreApplication.translate
        health_weather.setWindowTitle(_translate("health_weather", "Программа"))
        self.sample_btn.setText(_translate("health_weather", "Выбрать образец"))
        self.exit_btn.setText(_translate("health_weather", "Выход"))
        self.start_btn.setText(_translate("health_weather", "Запуск"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.kde_tab), _translate("health_weather", "Совместный KDE"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tests_tab), _translate("health_weather", "Тесты статистической нормальности"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.table_tab), _translate("health_weather", "Сводная таблица результатов"))
        self.standard_btn.setText(_translate("health_weather", "Выбрать эталон"))

