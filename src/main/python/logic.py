import os

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog, QGridLayout, QWidget, QFrame, QTextEdit


from form import Ui_MainBaseForm
from frame_patient import Ui_FramePatient
from frame_default import Ui_FrameDefault

from science.classes import *
from science.single_patient import StandardPatientStat
from science import CATS


module = os.path.dirname(__file__)


class BaseFrame(QFrame):
    def __init__(self, parent, child_frame_class):
        # noinspection PyArgumentList
        QFrame.__init__(self, parent=parent)
        child_frame_class.setupUi(self, self)
        self.resize(500, 500)
        self.setMinimumSize(QtCore.QSize(500, 500))


class QDefaultFrame(BaseFrame, Ui_FrameDefault):
    def __init__(self, parent=None):
        BaseFrame.__init__(self, parent, Ui_FrameDefault)


class QPatientFrame(BaseFrame, Ui_FramePatient):
    def __init__(self, standard_name, patient_name, parent=None):
        BaseFrame.__init__(self, parent, Ui_FramePatient)
        # делать остальные дела

        # Дичь новую добавил
        self.std = Standard.standards[standard_name]
        self.pat = Patient.patients[patient_name]
        self.get_report()

    def get_report(self):
        for cat_s, cat_l in CATS:
            self.pat.add_category(cat_s, "science/samples/1_1{}.txt".format(cat_s))
        self.stat = StandardPatientStat(self.std, self.pat)
        # выводит в консоль, перенос в QTextEdit не делал
        self.stat.get_report()
        # тест добавленяи информации в форму
        self.tab.layout = QGridLayout(self)
        self.text = QTextEdit()
        self.tab.layout.addWidget(self.text)
        self.tab.setLayout(self.tab.layout)
        self.text.append("12312")
        self.show()


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
        self.add_group_btn.clicked.connect(self.add_group_btn_clicked)
        self.del_group_btn.clicked.connect(self.del_group_btn_clicked)
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

    def patient_info(self):
        selected_ref = self.ref_list.currentItem()
        selected_patient = self.patient_list.currentItem()
        if selected_ref is not None and selected_patient is not None:
            self.patient = QPatientFrame(selected_ref.text(), selected_patient.text())
            self.patient.show()

    # КНОПКИ
    def add_ref_btn_clicked(self):
        options = QFileDialog.Options()
        fname, _ = QFileDialog.getOpenFileName(self,
                                               'Выбрать эталон',
                                               os.path.join(module, 'science', 'samples'),
                                               options=options)
        standard = fname[fname.rfind('/') + 1:fname.rfind('.')]
        Standard.from_file(fname, standard)
        self.ref_list.addItem(standard)

    def del_ref_btn_clicked(self):
        standard = self.ref_list.currentItem().text()
        self.ref_list.takeItem(self.ref_list.currentRow())
        Standard.delete(Standard.standards[standard])

    def add_group_btn_clicked(self):
        # Для тестирования, добавляется только одна группа '1'
        group = '1'
        self.group_list.addItem(group)
        Group(group)

    def del_group_btn_clicked(self):
        group = self.group_list.currentItem().text()
        for patient in Group.groups[group].pats:
            items = self.patient_list.findItems(patient, QtCore.Qt.MatchExactly)
            for item in items:
                self.patient_list.takeItem(self.patient_list.row(item))
        self.group_list.takeItem(self.group_list.currentRow())
        Group.delete(Group.groups[group])

    def add_patient_btn_clicked(self):
        if self.group_list.currentItem() is None:
            return
        group = self.group_list.currentItem().text()
        options = QFileDialog.Options()
        fname, _ = QFileDialog.getOpenFileName(self,
                                               'Выбрать файл пациента',
                                               os.path.join(module, 'science', 'samples'),
                                               options=options)
        patient = fname[fname.rfind('/') + 1:fname.rfind('.')]
        Patient(patient, group)
        self.patient_list.addItem(patient)
        self.patient_list.itemClicked.connect(self.patient_info)

    def del_patient_btn_clicked(self):
        patient = self.patient_list.currentItem().text()
        self.patient_list.takeItem(self.patient_list.currentRow())
        Patient.delete(Patient.patients[patient])

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
