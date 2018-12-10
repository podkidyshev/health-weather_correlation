import os

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog, QGridLayout, QWidget, QFrame

from form import Ui_MainBaseForm
from frame_patient import Ui_FramePatient
from frame_default import Ui_FrameDefault


module = os.path.dirname(__file__)


class BaseFrame(QFrame):
    def __init__(self, parent, child_frame_class):
        # noinspection PyArgumentList
        QFrame.__init__(self, parent=parent)
        child_frame_class.setupUi(self, self)
        self.resize(500, 500)
        self.setMinimumSize(QtCore.QSize(500, 500))


class QDefaultFrame(BaseFrame, Ui_FrameDefault):
    def __init__(self, parent):
        BaseFrame.__init__(self, parent, Ui_FrameDefault)


class QPatientFrame(BaseFrame, Ui_FramePatient):
    def __init__(self, parent, patient_name):
        BaseFrame.__init__(self, parent, Ui_FramePatient)
        # делать остальные дела


class Main(Ui_MainBaseForm):
    # noinspection PyArgumentList,PyUnresolvedReferences
    def __init__(self):
        # КОСТЫЛЬ, НЕ ТРОГАТЬ
        self.dummy = QWidget()
        self.gridLayout = QGridLayout(self.dummy)
        self.setCentralWidget(self.dummy)
        self.gridLayout = self.centralWidget().layout()
        # КОСТЫЛЬ, НЕ ТРОГАТЬ

        # фрейм данных
        self.data_frame = None

    def start(self):
        self.exit_btn.clicked.connect(self.btn_exit_clicked)
        #self.report_btn.clicked.connect(self.report_btn_clicked)

        self.add_ref_btn.clicked.connect(self.add_ref_btn_clicked)
        self.del_ref_btn.clicked.connect(self.del_ref_btn_clicked)
        #self.add_group_btn.clicked.connect(self.add_group_btn_clicked)
        # self.del_group_btn.clicked.connect(self.del_group_btn_clicked)
        self.add_patient_btn.clicked.connect(self.add_patient_btn_clicked)
        self.del_patient_btn.clicked.connect(self.del_patient_btn_clicked)

        self.set_data_frame(QDefaultFrame)
        self.show()

    def set_data_frame(self, frame_class, *args):
        if self.data_frame is not None:
            self.data_layout.removeWidget(self.data_frame)
            self.data_frame.deleteLater()
        self.data_frame = frame_class(self, *args)
        self.data_layout.insertWidget(0, self.data_frame)

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
