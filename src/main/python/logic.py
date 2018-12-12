import os

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QWidget, QFrame, QLabel
from PIL.ImageQt import ImageQt

from form import Ui_MainBaseForm
from frame_patient import Ui_FramePatient
from frame_default import Ui_FrameDefault

from science.classes import *
from science.single_patient import StandardPatientStat
from science import create_docx, save_docx, plot_to_image
from science.funcs import graph_kde


matplotlib.use("Qt5Agg")

module = os.path.dirname(__file__)


class BaseFrame(QFrame):
    def __init__(self, parent, child_frame_class):
        # noinspection PyArgumentList
        QFrame.__init__(self, parent=parent)
        child_frame_class.setupUi(self, self)
        self.resize(500, 500)
        self.setMinimumSize(QtCore.QSize(250, 250))
        self.layout().setContentsMargins(0, 0, 0, 0)


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
        graph_kde(self.report.get_report_item("distance"), self.plot)
        self.img_qt = ImageQt(plot_to_image(self.plot))
        self.img = QImage(self.img_qt)

        self.plot_canvas = QPixmap.fromImage(self.img)

        self.label = QLabel(self)
        self.tab_graphics.layout().insertWidget(0, self.label)

        self.label.setPixmap(self.plot_canvas)
        self.label.setScaledContents(True)

        self.get_report()

    def save_report(self):
        fname, _ = QFileDialog.getSaveFileName(self,
                                               'Сохранить отчет',
                                               os.path.join(module, 'science', 'samples'),
                                               options=QFileDialog.Options())
        doc = create_docx()
        self.report.get_report(doc)
        save_docx(doc, fname)

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
        self.dummy = QWidget()
        self.horizontalLayout = QHBoxLayout(self.dummy)
        self.setCentralWidget(self.dummy)
        # фрейм данных
        self.data_frame = None

    def start(self):
        # Создание/удаление эталона
        self.add_ref_btn.clicked.connect(self.add_ref_btn_clicked)
        self.del_ref_btn.clicked.connect(self.del_ref_btn_clicked)
        # Создание/удаление пациента
        self.add_pat_btn.clicked.connect(self.add_patient_btn_clicked)
        self.del_pat_btn.clicked.connect(self.del_patient_btn_clicked)
        # Кастомные фреймы
        self.pat_list.itemClicked.connect(self.patient_info)
        self.ref_list.itemClicked.connect(self.patient_info)
        # Отчет
        self.report_btn.clicked.connect(self.report_btn_clicked)

        self.set_data_frame(QDefaultFrame)
        self.show()

    def set_data_frame(self, frame_class, *args):
        if self.data_frame is not None:
            self.data_layout.removeWidget(self.data_frame)
            # sip.delete(self.data_frame)
            self.data_frame.hide()
            self.data_frame = None
        self.data_frame = frame_class(self, *args)
        self.data_layout.insertWidget(0, self.data_frame)

    def patient_info(self):
        selected_ref = self.ref_list.currentItem()
        selected_patient = self.pat_list.currentItem()
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

    def add_patient_btn_clicked(self):
        options = QFileDialog.Options()
        fname, _ = QFileDialog.getOpenFileName(self,
                                               'Выбрать файл пациента',
                                               "",  # os.path.join(module, 'science', 'samples'),
                                               options=options)
        try:
            pat = Patient.from_file(fname)
        except PatientDuplicateError as e:
            # TODO: всплывающее окно
            print(e.args[0])
            return
        self.pat_list.addItem(pat.name)

    def del_patient_btn_clicked(self):
        pat = self.pat_list.currentItem()
        if pat is None:
            # TODO: всплывающее окно
            print('Для удаления пациента кликните по нему!')
            return
        pat = pat.text()
        self.pat_list.takeItem(self.pat_list.currentRow())
        Patient.delete(Patient.patients[pat])
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
