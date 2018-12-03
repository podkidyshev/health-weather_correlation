import os

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import QFileDialog, QVBoxLayout
from PyQt5.QtWidgets import QWidget


from form import Ui_MainBaseForm

module = os.path.dirname(__file__)


class Main(Ui_MainBaseForm):
    def __init__(self):
        self.dummy = QWidget()
        self.verticalLayout = QVBoxLayout(self.dummy)
        self.setCentralWidget(self.dummy)
        self.verticalLayout = self.centralWidget().layout()

    def start(self):
        # self.start_btn.clicked.connect(self.btn_start_clicked)
        # self.exit_btn.clicked.connect(self.btn_exit_clicked)
        # self.sample_btn.clicked.connect(self.sample_btn_clicked)
        # self.show()
        pass

    # КНОПКИ
    def sample_btn_clicked(self):
        options = QFileDialog.Options()
        fname, _ = QFileDialog.getOpenFileName(self,
                                               'Open file',
                                               os.path.join(module, 'science', 'samples'),
                                               options=options)
        self.standard_line.setText(fname)

    def btn_start_clicked(self):
        self.figure = plt.figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)

        self.plot()

        self.kde_layout.addWidget(self.canvas)

        # self.show()

    def plot(self):
        data = [i for i in range(25)]
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        self.canvas.draw()

    def btn_exit_clicked(self):
        exit()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = Main()
#     sys.exit(app.exec_())
