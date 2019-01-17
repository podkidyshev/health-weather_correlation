import os
import matplotlib

from PyQt5.QtWidgets import QHBoxLayout, QWidget, QLabel, QMainWindow, QTextEdit
from PyQt5.QtCore import QEvent, Qt

from form import Ui_MainBaseForm

from science.classes import *

from logic import dialog_open, set_main_window
from logic.default import QFrameDefault
from logic.sample import QFrameSample
from logic.standard import QFrameStandard
from logic.mul_std_lead import QFrameStdMulSamples, QFrameMulStdSample, QFrameMulStdMulSamples

matplotlib.use("Qt5Agg")

# counter = 0


class Main(Ui_MainBaseForm):
    # noinspection PyArgumentList,PyUnresolvedReferences
    def __init__(self):
        self.dummy = QWidget()
        self.horizontalLayout = QHBoxLayout(self.dummy)
        self.setCentralWidget(self.dummy)
        # фрейм данных
        self.data_frame = None
        # для автоскейлинга графиков
        set_main_window(self)

    # noinspection PyUnresolvedReferences
    def start(self):
        # Создание/удаление эталона
        self.add_std_btn.clicked.connect(self.add_std_btn_clicked)
        self.del_std_btn.clicked.connect(self.del_std_btn_clicked)
        # Создание/удаление пациента
        self.add_sample_btn.clicked.connect(self.add_sample_btn_clicked)
        self.del_sample_btn.clicked.connect(self.del_sample_btn_clicked)
        # Кастомные фреймы
        self.lead_box.activated.connect(self.lead_box_activated)
        self.slave_box.activated.connect(self.choose_data_frame)
        # Отчет
        self.report_btn.clicked.connect(self.report_btn_clicked)

        self.set_data_frame(QFrameDefault)
        self.show()
        # тестовый скрипт (для удобства)
        self.startup()

    def startup(self):
        if os.path.exists(r'src/main/python/science/samples/'):
            for group in '123':
                for idx in '123456':
                    self.add_sample(r'src/main/python/science/samples/{}_{}.xlsx'.format(group, idx))
            for entry in sorted(os.listdir(r'src/main/python/science/samples/')):
                if entry[-3:] == 'txt':
                    self.add_std(r'src/main/python/science/samples/{}'.format(entry))

    def add_sample(self, fname):
        try:
            sample = Sample.from_file(fname)
        except Sample.SampleError as e:
            # TODO: всплывающее окно
            print(e.args[0])
            return
        if self.sample_list.count() == 0:
            self.sample_list.addItem("--Групповой--")
        self.sample_list.insertItem(self.sample_list.count() - 1, sample.name)
        self.update_boxes()

    def add_std(self, fname):
        std = Standard.from_file(fname)
        self.std_list.addItem(std.name)
        self.update_boxes()

    def update_boxes(self):
        self.lead_box.clear()
        self.slave_box.clear()
        std_items = ["Погода: " + str(self.std_list.item(i).text()) for i in range(self.std_list.count())] + \
                    ["Погода: --Группа--"]
        sample_items = ["Образец: " + str(self.sample_list.item(i).text()) for i in range(self.sample_list.count())] + \
                       ["Образец: --Группа--"]
        self.lead_box.addItems(std_items + sample_items)

    def set_data_frame(self, frame_class, *args):
        if self.data_frame is not None:
            self.data_layout.removeWidget(self.data_frame)
            self.data_frame.hide()
            self.data_frame = None
        self.data_frame = frame_class(self, *args)
        self.data_layout.insertWidget(0, self.data_frame)

    def choose_data_frame(self):
        orientation = self.lead_box.currentText().split(' ')[0] == "Погода:"
        lead = self.lead_box.currentText().split(' ')[1]
        slave = self.slave_box.currentText().split(' ')[1]

        # Погода - образец
        if orientation:
            if lead in Standard.standards and (slave in Sample.samples or slave == "--Групповой--"):
                self.set_data_frame(QFrameSample, lead, slave)
            elif lead in Standard.standards and slave == "--Группа--":
                self.set_data_frame(QFrameStdMulSamples, lead)
            elif lead == "--Группа--" and (slave in Sample.samples or slave == "--Групповой--"):
                self.set_data_frame(QFrameMulStdSample, slave)
            elif lead == "--Группа--" and slave == "--Группа--":
                self.set_data_frame(QFrameMulStdMulSamples)
            else:
                raise ValueError("Неизвестный случай")
        # Образец - погода
        else:
            if (lead in Sample.samples or lead == "--Групповой--") and slave in Standard.standards:
                self.set_data_frame(QFrameStandard, lead, slave)
            else:
                raise ValueError('Неизвестный случай')

    # КНОПКИ
    def lead_box_activated(self):
        lead_type = self.lead_box.currentText().split(' ')[0]
        if lead_type == 'Образец:':
            items = ["Погода: " + str(self.std_list.item(i).text()) for i in range(self.std_list.count())] + \
                    ["Погода: --Группа--"]
        elif lead_type == 'Погода:':
            items = ["Образец: " + str(self.sample_list.item(i).text()) for i in range(self.sample_list.count())] + \
                    ["Образец: --Группа--"]
        else:
            raise ValueError('Неизвестный тип данных')
        self.slave_box.clear()
        self.slave_box.addItems(items)

    def add_std_btn_clicked(self):
        fname = dialog_open("Выбрать эталон", "txt")
        if fname:
            self.add_std(fname)

    def del_std_btn_clicked(self):
        std = self.std_list.currentItem()
        if std is None:
            # TODO: всплывающее окно
            print('Выберите эталон для удаления!')
        std = std.text()
        self.std_list.takeItem(self.std_list.currentRow())
        Standard.delete(Standard.standards[std])
        self.set_data_frame(QFrameDefault)
        self.update_boxes()

    def add_sample_btn_clicked(self):
        fname = dialog_open("Выбрать файл пациента", "xlsx")
        if fname:
            self.add_sample(fname)

    def del_sample_btn_clicked(self):
        sample = self.sample_list.currentItem()
        if sample is None:
            # TODO: всплывающее окно
            print('Для удаления пациента кликните по нему!')
            return
        sample = sample.text()
        self.sample_list.takeItem(self.sample_list.currentRow())
        if self.sample_list.count() == 1:
            self.sample_list.clear()
        Sample.delete(Sample.samples[sample])
        self.set_data_frame(QFrameDefault)
        self.update_boxes()

    def report_btn_clicked(self):
        if hasattr(self.data_frame, "save_report"):
            self.data_frame.save_report()
        else:
            print("ФУНКЦИЯ save_report НЕ РЕАЛИЗОВАНА")

    def eventFilter(self, widget, event):
        event_types = [QEvent.Resize, QEvent.Show, 24]

        if event.type() in event_types and isinstance(widget, QLabel) and hasattr(widget, '_pixmap'):
            widget.setPixmap(widget._pixmap.scaled(widget.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        if event.type() in event_types and isinstance(widget, QTextEdit) and hasattr(widget, '_custom'):
            if widget._updating:
                widget._updating = False
            else:
                widget._updating = True
                doc_height = widget.document().size().toSize().height()
                widget.setMinimumHeight(doc_height)
        # noinspection PyCallByClass,PyTypeChecker
        return QMainWindow.eventFilter(self, widget, event)
