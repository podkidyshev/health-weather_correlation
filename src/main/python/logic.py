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
from science import CATS, file_base_name
from science.funcs import graph_kde

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
    def __init__(self, parent, pat_name, std_name):
        BaseFrame.__init__(self, parent, Ui_FramePatient)

        self.std = Standard.standards[std_name]
        self.pat = Patient.patients[pat_name]
        self.report = StandardPatientStat(self.std, self.pat)

        self.plot = plt.figure()
        self.plot_canvas = FigureCanvas(self.plot)
        graph_kde(self.report.get_report_item("distance"), self.plot)
        self.plot_canvas.draw()
        self.tab_graphics.layout().addWidget(self.plot_canvas)

        self.get_report()

    def save_report(self):
        # fname, _ = QFileDialog.getSaveFileName(self,
        #                                        'Сохранить отчет',
        #                                        os.path.join(module, 'science', 'samples'),
        #                                        options=QFileDialog.Options())
        return

    def get_report(self):
        pass
        # for cat_s, cat_l in CATS:
        #     self.pat.add_category(cat_s, "science/samples/1_1{}.txt".format(cat_s))
        # тест добавленяи информации в форму
        # self.tab.layout = QGridLayout(self)
        # self.text = QTextEdit()
        # self.tab.layout.addWidget(self.text)
        # self.tab.setLayout(self.tab.layout)
        # self.text.append("12312")
        # self.show()


class Main(Ui_MainBaseForm):
    # noinspection PyArgumentList,PyUnresolvedReferences
    def __init__(self):
        # НЕ ТРОГАТЬ
        self.dummy = QWidget()
        self.gridLayout = QGridLayout(self.dummy)
        self.setCentralWidget(self.dummy)
        self.gridLayout = self.centralWidget().layout()
        # НЕ ТРОГАТЬ

        # фрейм данных
        self.data_frame = None

    def start(self):
        # Создание/удаление эталона
        self.add_ref_btn.clicked.connect(self.add_ref_btn_clicked)
        self.del_ref_btn.clicked.connect(self.del_ref_btn_clicked)
        # Создание/удаление группы
        self.add_group_btn.clicked.connect(self.add_group_btn_clicked)
        self.del_group_btn.clicked.connect(self.del_group_btn_clicked)
        # Создание/удаление пациента
        self.add_patient_btn.clicked.connect(self.add_patient_btn_clicked)
        self.del_patient_btn.clicked.connect(self.del_patient_btn_clicked)
        # Кастомные фреймы
        self.patient_list.itemClicked.connect(self.patient_info)
        self.ref_list.itemClicked.connect(self.patient_info)
        # Отчет
        self.report_btn.clicked.connect(self.report_btn_clicked)

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
        if selected_ref is None:
            # TODO: всплывающее окно
            print('Выберите эталон!')
        elif selected_patient is None:
            # TODO: выберите пациента
            print('Выберите пациента!')
        else:
            self.set_data_frame(QPatientFrame, selected_patient.text(), selected_ref.text())

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
        standard = self.ref_list.currentItem()
        if standard is None:
            # TODO: всплывающее окно
            print('Выберите эталон для удаления!')
        standard = standard.text()
        self.ref_list.takeItem(self.ref_list.currentRow())
        Standard.delete(Standard.standards[standard])
        self.set_data_frame(QDefaultFrame)

    def add_group_btn_clicked(self):
        if len(Group.groups) > 0:
            return
        # Для тестирования, добавляется только одна группа '1'
        group = '1'
        self.group_list.addItem(group)
        Group(group)

    def del_group_btn_clicked(self):
        group = self.group_list.currentItem()
        if group is None:
            # TODO: всплывающее окно
            print('Выберите группу для удаления!')
            return
        group = group.text()
        for patient in Group.groups[group].pats:
            items = self.patient_list.findItems(patient, QtCore.Qt.MatchExactly)
            for item in items:
                self.patient_list.takeItem(self.patient_list.row(item))
        self.group_list.takeItem(self.group_list.currentRow())
        Group.delete(Group.groups[group])
        self.set_data_frame(QDefaultFrame)

    def add_patient_btn_clicked(self):
        if self.group_list.currentItem() is None:
            # TODO: здесь будет всплывающее окно с подсказкой
            print('Сначала надо выбрать группу')
            return
        group = self.group_list.currentItem().text()
        options = QFileDialog.Options()
        fname, _ = QFileDialog.getOpenFileName(self,
                                               'Выбрать файл пациента',
                                               "",  # os.path.join(module, 'science', 'samples'),
                                               options=options)
        patient = file_base_name(fname)
        try:
            pat = Patient(patient, group)
            pat.add_category("", fname)
        except PatientDuplicateError:
            # TODO: всплывающее окно
            print("Пациент с имненем {} уже загружен".format(patient))
            return
        self.patient_list.addItem(patient)

    def del_patient_btn_clicked(self):
        patient = self.patient_list.currentItem()
        if patient is None:
            # TODO: всплывающее окно
            print('Для удаления пациента кликните по нему!')
            return
        patient = patient.text()
        self.patient_list.takeItem(self.patient_list.currentRow())
        Patient.delete(Patient.patients[patient])
        self.set_data_frame(QDefaultFrame)

    def report_btn_clicked(self):
        if hasattr(self.data_frame, "save_report"):
            self.data_frame.save_report()

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


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = Main()
#     sys.exit(app.exec_())
