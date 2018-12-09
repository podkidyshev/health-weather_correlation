import os

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import QFileDialog, QGridLayout, QWidget

# from science.samples_hist import patient_init_stat, plot
from form_updated import Ui_MainBaseForm
from science import patient_suffix

module = os.path.dirname(__file__)


class Main(Ui_MainBaseForm):
    def __init__(self):
        # КОСТЫЛЬ, НЕ ТРОГАТЬ
        self.dummy = QWidget()
        self.gridLayout = QGridLayout(self.dummy)
        self.setCentralWidget(self.dummy)
        self.gridLayout = self.centralWidget().layout()
        # КОСТЫЛЬ, НЕ ТРОГАТЬ

    def start(self):
        self.exit_btn.clicked.connect(self.btn_exit_clicked)
        #self.report_btn.clicked.connect(self.report_btn_clicked)

        self.add_ref_btn.clicked.connect(self.add_ref_btn_clicked)
        self.del_ref_btn.clicked.connect(self.del_ref_btn_clicked)
        #self.add_group_btn.clicked.connect(self.add_group_btn_clicked)
        # self.del_group_btn.clicked.connect(self.del_group_btn_clicked)
        self.add_patient_btn.clicked.connect(self.add_patient_btn_clicked)
        self.del_patient_btn.clicked.connect(self.del_patient_btn_clicked)
        self.show()

    # КНОПКИ
    def add_ref_btn_clicked(self):
        options = QFileDialog.Options()
        fname, _ = QFileDialog.getOpenFileName(self,
                                               'Выбрать эталон',
                                               os.path.join(module, 'science', 'samples'),
                                               options=options)
        self.ref_list.addItem(fname[fname.rfind('/') + 1:fname.rfind('.')])

    def del_ref_btn_clicked(self):
        listItems = self.ref_list.selectedItems()
        if not listItems: return
        for i in range(len(listItems)):
            self.ref_list.takeItem(i)

    def add_patient_btn_clicked(self):
        options = QFileDialog.Options()
        fname, _ = QFileDialog.getOpenFileName(self,
                                               'Выбрать файл пациента',
                                               os.path.join(module, 'science', 'samples'),
                                               options=options)
        self.patient_list.addItem(fname[fname.rfind('/') + 1:fname.rfind('.')])

    def del_patient_btn_clicked(self):
        listItems = self.patient_list.selectedItems()
        if not listItems: return
        for i in range(len(listItems)):
            self.patient_list.takeItem(i)

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
