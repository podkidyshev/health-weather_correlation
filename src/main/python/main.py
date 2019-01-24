import sys

from fbs_runtime.application_context import ApplicationContext
from PyQt5.QtWidgets import QMainWindow

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
pyuic5 src/main/python/ui/standard.ui -o src/main/python/frames/standard.py

pyuic5 src/main/python/ui/dialogs/stds.ui -o src/main/python/frames/dialogs/stds.py

pyuic5 src/main/python/ui/utils/image.ui -o src/main/python/frames/utils/image.py
pyuic5 src/main/python/ui/utils/info.ui -o src/main/python/frames/utils/info.py
pyuic5 src/main/python/ui/utils/kde.ui -o src/main/python/frames/utils/kde.py
pyuic5 src/main/python/ui/utils/standard_type.ui -o src/main/python/frames/utils/standard_type.py
pyuic5 src/main/python/ui/utils/text.ui -o src/main/python/frames/utils/text.py
"""