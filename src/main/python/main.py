import sys

from fbs_runtime.application_context import ApplicationContext
import PyQt5.QtWidgets
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QTextEdit
from PyQt5.QtGui import QWheelEvent


class MyTabWidget(QTabWidget):
    def __init__(self, *args, **kwargs):
        super(MyTabWidget, self).__init__(*args, **kwargs)
        # noinspection PyUnresolvedReferences
        self.currentChanged.connect(self.on_change)

    def on_change(self, index):
        tab = self.widget(index)
        if tab.layout() is not None:
            for child in range(tab.layout().count()):
                widget = tab.layout().itemAt(child).widget()
                widget.update()


class MyTextEdit(QTextEdit):
    def __init__(self, *args):
        super(MyTextEdit, self).__init__(*args)

    def wheelEvent(self, event: QWheelEvent):
        if hasattr(self, '_custom'):
            event.ignore()


QTabWidgetOriginal = PyQt5.QtWidgets.QTabWidget
PyQt5.QtWidgets.QTabWidget = MyTabWidget

QTextEditOriginal = PyQt5.QtWidgets.QTextEdit
PyQt5.QtWidgets.QTextEdit = MyTextEdit


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


class AppContext(ApplicationContext):           # 1. Subclass ApplicationContext
    def run(self):                              # 2. Implement run()
        window = ExampleApp()
        window.setWindowTitle("Health-weather correlation")
        # window.resize(250, 150)
        window.show()
        return self.app.exec_()                 # 3. End run() with this line


if __name__ == '__main__':
    appctxt = AppContext()                      # 4. Instantiate the subclass
    exit_code = appctxt.run()                   # 5. Invoke run()
    sys.exit(exit_code)

# https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk
# https://tproger.ru/translations/python-gui-pyqt/
r"""
pyuic5 src/main\python/ui/form.ui -o src/main/python/form.py
pyuic5 src/main\python/ui/default.ui -o src/main/python/frames/default.py
pyuic5 src/main/python/ui/sample.ui -o src/main/python/frames/sample.py
pyuic5 src/main/python/ui/factor.ui -o src/main/python/frames/factor.py

pyuic5 src/main/python/ui/mul_std.ui -o src/main/python/frames/mul_both.py
pyuic5 src/main/python/ui/mul_one.ui -o src/main/python/frames/mul_one.py
pyuic5 src/main/python/ui/mul_both.ui -o src/main/python/frames/mul_both.py

pyuic5 src/main/python/ui/utils/check.ui -o src/main/python/frames/utils/check.py
pyuic5 src/main/python/ui/utils/combo.ui -o src/main/python/frames/utils/combo.py
pyuic5 src/main/python/ui/utils/image.ui -o src/main/python/frames/utils/image.py
pyuic5 src/main/python/ui/utils/kde.ui -o src/main/python/frames/utils/kde.py
pyuic5 src/main/python/ui/utils/info.ui -o src/main/python/frames/utils/info.py
pyuic5 src/main/python/ui/utils/text.ui -o src/main/python/frames/utils/text.py

pyuic5 src/main/python/ui/dialog.ui -o src/main/python/frames/dialog.py
"""