import os

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import QFileDialog, QVBoxLayout
from PyQt5.QtWidgets import QWidget

# from science.samples_hist import patient_init_stat, plot
from form import Ui_MainBaseForm
from science import patient_suffix

module = os.path.dirname(__file__)


class Main(Ui_MainBaseForm):
    def __init__(self):
        # КОСТЫЛЬ, НЕ ТРОГАТЬ
        self.dummy = QWidget()
        self.verticalLayout = QVBoxLayout(self.dummy)
        self.setCentralWidget(self.dummy)
        self.verticalLayout = self.centralWidget().layout()
        # КОСТЫЛЬ, НЕ ТРОГАТЬ

    def start(self):
        self.start_btn.clicked.connect(self.btn_start_clicked)
        self.exit_btn.clicked.connect(self.btn_exit_clicked)
        self.standard_btn.clicked.connect(self.standard_btn_clicked)
        self.sample_btn.clicked.connect(self.sample_btn_clicked)

        self.show()

    # КНОПКИ
    def standard_btn_clicked(self):
        options = QFileDialog.Options()
        fname, _ = QFileDialog.getOpenFileName(self,
                                               'Выбрать эталон',
                                               os.path.join(module, 'science', 'samples'),
                                               options=options)
        self.standard_line.setText(fname)

    def sample_btn_clicked(self):
        options = QFileDialog.Options()
        fname, _ = QFileDialog.getOpenFileName(self,
                                               'Выбрать файл пациента',
                                               os.path.join(module, 'science', 'samples'),
                                               options=options)
        self.sample_line.setText(fname)

    def btn_start_clicked(self):
        self.figure = plt.figure(figsize=(5, 4), dpi=100)  # plt.figure(figsize=(100, 100), dpi=100)
        self.canvas = FigureCanvas(self.figure)

        self.plot()

        self.kde_layout.addWidget(self.canvas)

    def plot(self):
        patient = self.sample_line.text()
        # samples_hist_report = patient_init_stat(self.standard_line.text(), [patient,
        #                                                                     patient_suffix(patient, 'n'),
        #                                                                     patient_suffix(patient, 'o'),
        #                                                                     patient_suffix(patient, 'e')])
        # plot(samples_hist_report['distances'], self.figure)
        self.canvas.draw()

        # data = [i for i in range(25)]
        # self.figure.clear()
        # ax = self.figure.add_subplot(111)
        # ax.plot(data, 'r-')
        # self.canvas.draw()

    def btn_exit_clicked(self):
        exit()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = Main()
#     sys.exit(app.exec_())
