import sys

from src.main.python.health_weather import Ui_health_weather
from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class Main(QWidget):
    def __init__(self):
        super(Main, self).__init__()

        self.ui = Ui_health_weather()
        self.ui.setupUi(self)

        self.ui.start_btn.clicked.connect(self.btn_start_clicked)
        self.ui.exit_btn.clicked.connect(self.btn_exit_clicked)

        self.show()

    def btn_start_clicked(self):
        self.figure = plt.figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)

        self.plot()

        self.ui.kde_layout.addWidget(self.canvas)

        self.show()

    def plot(self):
        data = [i for i in range(25)]
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        self.canvas.draw()

    def btn_exit_clicked(self):
        exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())



