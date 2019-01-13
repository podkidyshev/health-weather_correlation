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

matplotlib.use("Qt5Agg")


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
            for entry in os.listdir(r'src/main/python/science/samples/'):
                if entry[-3:] == 'txt':
                    self.add_std(r'src/main/python/science/samples/{}'.format(entry))

    def add_sample(self, fname):
        try:
            sample = Sample.from_file(fname)
            if sample is None:
                return
        except Sample.SampleError as e:
            # TODO: всплывающее окно
            print(e.args[0])
            return
        self.sample_list.addItem(sample.name)
        self.update_boxes()

    def add_std(self, fname):
        std = fname[fname.rfind('/') + 1:fname.rfind('.')]
        if std == "":
            return None
        Standard.from_file(fname, std)
        self.std_list.addItem(std)
        self.update_boxes()

    def update_boxes(self):
        self.lead_box.clear()
        self.slave_box.clear()
        std_items = ["Погода: " + str(self.std_list.item(i).text()) for i in range(self.std_list.count())]
        sample_items = ["Образец: " + str(self.sample_list.item(i).text()) for i in range(self.sample_list.count())]
        if len(sample_items):
            sample_items.append("Образец: --Групповой--")
        self.lead_box.addItems(std_items + sample_items)

    def set_data_frame(self, frame_class, *args):
        if self.data_frame is not None:
            self.data_layout.removeWidget(self.data_frame)
            self.data_frame.hide()
            self.data_frame = None
        self.data_frame = frame_class(self, *args)
        self.data_layout.insertWidget(0, self.data_frame)

    def choose_data_frame(self):
        lead = self.lead_box.currentText().split(' ')[1]
        slave = self.slave_box.currentText().split(' ')[1]

        if lead in Standard.standards and slave in Sample.samples:
            self.set_data_frame(QFrameSample, lead, slave)
        elif lead in Standard.standards and slave == "--Групповой--":
            self.set_data_frame(QFrameSample, lead, Sample.group.name)
        elif lead in Standard.standards and slave == 'Образец: --Все образцы--':
            print('фрейм для MulStandardsMulSamples')
        elif lead in Sample.samples and slave in Standard.standards:
            self.set_data_frame(QFrameStandard, lead, slave)
        elif lead == "--Групповой--" and slave in Standard.standards:
            self.set_data_frame(QFrameStandard, Sample.group.name, slave)
        else:
            raise ValueError('Неизвестный случай')

    # КНОПКИ
    def lead_box_activated(self):
        lead_type = self.lead_box.currentText().split(' ')[0]
        if lead_type == 'Образец:':
            items = ["Погода: " + str(self.std_list.item(i).text()) for i in range(self.std_list.count())]
        elif lead_type == 'Погода:':
            items = ["Образец: " + str(self.sample_list.item(i).text()) for i in range(self.sample_list.count())]
            if len(items):
                items.append("Образец: --Групповой--")
        else:
            raise ValueError('Неизвестный тип данных')
        self.slave_box.clear()
        self.slave_box.addItems(items)

    def add_std_btn_clicked(self):
        fname = dialog_open(self, " Выбрать эталон")
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
        fname = dialog_open(self, "Выбрать файл пациента")
        self.add_sample(fname)

    def del_sample_btn_clicked(self):
        sample = self.sample_list.currentItem()
        if sample is None:
            # TODO: всплывающее окно
            print('Для удаления пациента кликните по нему!')
            return
        sample = sample.text()
        self.sample_list.takeItem(self.sample_list.currentRow())
        Sample.delete(Sample.samples[sample])
        self.set_data_frame(QFrameDefault)
        self.update_boxes()

    def report_btn_clicked(self):
        if hasattr(self.data_frame, "save_report"):
            self.data_frame.save_report()

    def eventFilter(self, widget, event):
        event_types = [QEvent.Resize, QEvent.Show]

        if event.type() in event_types and isinstance(widget, QLabel) and hasattr(widget, '_pixmap'):
            if widget._updating:
                widget.setPixmap(widget._pixmap.scaled(widget.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                widget._updating = False
            else:
                widget._updating = True
                ratio = widget._pixmap.height() / widget._pixmap.width()
                widget.setMinimumHeight(widget.width() * ratio + 2)
            return True
        if event.type() in event_types and isinstance(widget, QTextEdit) and hasattr(widget, '_custom'):
            if widget._updating:
                widget._updating = False
            else:
                widget._updating = True
                doc_height = widget.document().size().toSize().height()
                widget.setMinimumHeight(doc_height)
        # noinspection PyCallByClass,PyTypeChecker
        return QMainWindow.eventFilter(self, widget, event)
