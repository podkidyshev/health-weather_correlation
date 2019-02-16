import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

import logic.logic as logic


class ExampleApp(QMainWindow, logic.Main):
    def __init__(self):
        # noinspection PyArgumentList
        QMainWindow.__init__(self)
        logic.Main.__init__(self)
        # создание виджетов в MainForm (если что переопределить в logic.Main)
        self.setupUi(self)
        # старт (собстно show)
        logic.Main.start(self)
        self.setWindowTitle("Health-weather correlation")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    sys.exit(app.exec_())

# https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk
# https://tproger.ru/translations/python-gui-pyqt/
r"""
pyuic5 src/main\python/ui/form.ui -o src/main/python/form.py
pyuic5 src/main\python/ui/default.ui -o src/main/python/frames/default.py
pyuic5 src/main/python/ui/sample.ui -o src/main/python/frames/sample.py
pyuic5 src/main/python/ui/standard.ui -o src/main/python/frames/standard.py

pyuic5 src/main/python/ui/dialogs/stds.ui -o src/main/python/frames/dialogs/stds.py

pyuic5 src/main/python/ui/utils/image.ui -o src/main/python/frames/utils/image.py
pyuic5 src/main/python/ui/utils/info.ui -o src/main/python/frames/utils/info.py
pyuic5 src/main/python/ui/utils/kde.ui -o src/main/python/frames/utils/kde.py
pyuic5 src/main/python/ui/utils/standard_type.ui -o src/main/python/frames/utils/standard_type.py
pyuic5 src/main/python/ui/utils/text.ui -o src/main/python/frames/utils/text.py
"""