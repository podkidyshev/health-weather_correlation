import matplotlib

from PyQt5.QtWidgets import QHBoxLayout, QWidget

from form import Ui_MainBaseForm

from science.classes import *

from logic import dialog_open
from logic.default import QFrameDefault
from logic.patient import QFramePatient


matplotlib.use("Qt5Agg")


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

        self.set_data_frame(QFrameDefault)
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
            self.set_data_frame(QFramePatient, selected_patient.text(), selected_ref.text())

    # КНОПКИ
    def add_ref_btn_clicked(self):
        fname = dialog_open(self, " Выбрать эталон")
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
        self.set_data_frame(QFrameDefault)

    def add_patient_btn_clicked(self):
        fname = dialog_open(self, "Выбрать файл пациента")
        try:
            pat = Sample.from_file(fname)
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
        Sample.delete(Sample.samples[pat])
        self.set_data_frame(QFrameDefault)

    def report_btn_clicked(self):
        if hasattr(self.data_frame, "save_report"):
            self.data_frame.save_report()
