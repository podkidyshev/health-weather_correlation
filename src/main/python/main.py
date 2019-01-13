import sys

from fbs_runtime.application_context import ApplicationContext
import PyQt5.QtWidgets
from PyQt5.QtWidgets import QMainWindow, QTabWidget


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


QTabWidgetOriginal = PyQt5.QtWidgets.QTabWidget
PyQt5.QtWidgets.QTabWidget = MyTabWidget


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
pyuic5 src/main\python/ui/frame_default.ui -o src/main/python/frames/default.py
pyuic5 src/main/python/ui/frame_sample.ui -o src/main/python/frames/sample.py
pyuic5 src/main/python/ui/frame_factor.ui -o src/main/python/frames/factor.py
"""