import os
import sys
import matplotlib

from PyQt5.QtWidgets import QHBoxLayout, QWidget, QLabel, QMainWindow, QTextEdit
from PyQt5.QtCore import QEvent, Qt

from form import Ui_MainBaseForm

from science import ClassesError, ScienceError
from science.classes import *

from logic import dialog_open, set_main_window, error_dialog
from logic.standard import QFrameStdSample, QFrameStdMulSamples
from logic.sample import QFrameSampleStd  # , QFrameMulSamplesStd

from logic.utils import QFrameDefault

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
        self.report_group_btn.clicked.connect(self.report_group_btn_clicked)

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
        except ClassesError as e:
            error_dialog(e)
            return
        except Exception as e:
            error_dialog(e, unknown=True)
            return
        if self.sample_list.count() == 0:
            self.sample_list.addItem("--Групповой--")
        self.sample_list.insertItem(self.sample_list.count() - 1, sample.name)
        self.update_boxes()

    def add_std(self, fname):
        try:
            std = Standard.from_file(fname)
        except ClassesError as e:
            error_dialog(e)
            return
        except Exception as e:
            error_dialog(e, unknown=True)
            return
        self.std_list.addItem(std.name)
        self.update_boxes()

    def update_boxes(self):
        self.lead_box.clear()
        self.slave_box.clear()
        std_items = ["Погода: " + str(self.std_list.item(i).text()) for i in range(self.std_list.count())]
        sample_items = ["Образец: " + str(self.sample_list.item(i).text()) for i in range(self.sample_list.count())]
        self.lead_box.addItems(std_items + sample_items)

    def set_data_frame(self, frame_class, *args):
        if self.data_frame is not None:
            self.data_layout.removeWidget(self.data_frame)
            self.data_frame.hide()
            self.data_frame = None
        try:
            self.data_frame = frame_class(self, *args)
            self.data_layout.insertWidget(0, self.data_frame)
        except (ScienceError, Exception) as e:
            raise ValueError from e
            if frame_class == QFrameDefault:
                error_dialog("Ошибка в окне по умолчанию. Свяжитесь с разработчиком")
                sys.exit(1)
            error_dialog(e, unknown=True)
            self.data_frame = None
            self.set_data_frame(QFrameDefault)

    def choose_data_frame(self):
        orientation = self.lead_box.currentText().split(' ')[0] == "Погода:"
        lead = self.lead_box.currentText().split(' ')[1]
        slave = self.slave_box.currentText().split(' ')[1]

        # Погода - образец
        if orientation:
            if lead in Standard.standards and (slave in Sample.samples or slave == "--Групповой--"):
                self.set_data_frame(QFrameStdSample, lead, slave)
            elif lead in Standard.standards and slave == "--Группа--":
                if len(Sample.samples) < 3:
                    error_dialog("Для составления отчета по группе эталонов необходимо как минимум 3 образца")
                    return
                self.set_data_frame(QFrameStdMulSamples, lead)
            else:
                error_dialog("Необработанный случай выбора фрейма: lead={}, slave={}, orient={}"
                             .format(lead, slave, orientation), unknown=True)
        # Образец - погода
        else:
            if (lead in Sample.samples or lead == "--Групповой--") and slave in Standard.standards:
                self.set_data_frame(QFrameSampleStd, lead, slave)
            # elif lead == "--Группа--" and slave in Standard.standards:
            #     self.set_data_frame(QFrameMulSamplesStd, slave)
            else:
                error_dialog("Необработанный случай выбора фрейма: lead={}, slave={}, orient={}"
                             .format(lead, slave, orientation), unknown=True)

    # КНОПКИ
    def lead_box_activated(self):
        lead_type = self.lead_box.currentText().split(' ')[0]
        if lead_type == 'Образец:':
            items = ["Погода: " + str(self.std_list.item(i).text()) for i in range(self.std_list.count())]
        elif lead_type == 'Погода:':
            items = ["Образец: " + str(self.sample_list.item(i).text()) for i in range(self.sample_list.count())] + \
                    ["Образец: --Группа--"]
        else:
            error_dialog("Неизвестный тип данных в боксе: {}".format(lead_type), unknown=True)
            return
        if self.slave_box.count():
            slave_type = self.slave_box.currentText().split(' ')[0]
            if slave_type != lead_type:
                self.choose_data_frame()
                return
        self.slave_box.clear()
        self.slave_box.addItems(items)

    def add_std_btn_clicked(self):
        fnames = dialog_open("Выбрать эталон", "txt")
        if fnames:
            for fname in fnames:
                self.add_std(fname)

    def del_std_btn_clicked(self):
        std = self.std_list.currentItem()
        if self.std_list.count() == 0:
            return
        if std is None:
            error_dialog("Выберите эталон для удаления!")
            return
        std = std.text()
        self.std_list.takeItem(self.std_list.currentRow())
        Standard.delete(Standard.standards[std])
        self.set_data_frame(QFrameDefault)
        self.update_boxes()

    def add_sample_btn_clicked(self):
        fnames = dialog_open("Выбрать файл пациента", "xlsx")
        if fnames:
            for fname in fnames:
                self.add_sample(fname)

    def del_sample_btn_clicked(self):
        sample = self.sample_list.currentItem()
        if self.sample_list.count() == 0:
            return
        if sample is None:
            error_dialog("Выберите пациента для удаления!")
            return
        sample = sample.text()
        if sample == "--Групповой--":
            # error_dialog("Невозможно удалить групповой образец!")
            return
        try:
            Sample.delete(Sample.samples[sample])
        except ClassesError as e:
            error_dialog(e)
        except Exception as e:
            error_dialog(e, unknown=True)
        self.sample_list.takeItem(self.sample_list.currentRow())
        if self.sample_list.count() == 1:
            self.sample_list.clear()
        self.set_data_frame(QFrameDefault)
        self.update_boxes()

    def report_btn_clicked(self):
        if self.data_frame is not None and hasattr(self.data_frame, "save_report"):
            try:
                self.data_frame.save_report()
            except (ScienceError, Exception) as e:
                error_dialog(e, unknown=True)
        elif self.data_frame is not None:
            error_dialog("Функция save_report не реализована у окна {}. Пожалуйста, свяжитесь с разработчиком"
                         .format(type(self.data_frame).__name__))

    def report_group_btn_clicked(self):
        if self.data_frame is not None and hasattr(self.data_frame, "save_report_group"):
            try:
                self.data_frame.save_report_group()
            except (ScienceError, Exception) as e:
                error_dialog(e, unknown=True)
        elif self.data_frame is not None:
            error_dialog("Функция save_report_group не реализована у окна {}. Пожалуйста, свяжитесь с разработчиком"
                         .format(type(self.data_frame).__name__))

    def eventFilter(self, widget, event):
        event_types = [QEvent.Resize, QEvent.Show, 24]

        if event.type() in event_types and isinstance(widget, QLabel) and hasattr(widget, 'plot_pixmap'):
            widget.setPixmap(widget.plot_pixmap.scaled(widget.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        if event.type() in event_types and isinstance(widget, QTextEdit) and hasattr(widget, 'c_updating'):
            if widget.c_updating:
                widget.c_updating = False
            else:
                widget.c_updating = True
                doc_height = widget.document().size().toSize().height()
                widget.setMinimumHeight(doc_height)
        # noinspection PyCallByClass,PyTypeChecker
        return QMainWindow.eventFilter(self, widget, event)
