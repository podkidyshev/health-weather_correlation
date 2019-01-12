import matplotlib

from PyQt5.QtWidgets import QHBoxLayout, QWidget, QLabel, QMainWindow, QTextEdit
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QResizeEvent

from form import Ui_MainBaseForm

from science.classes import *

from logic import dialog_open, set_main_window
from logic.default import QFrameDefault
from logic.sample import QFrameSample


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
        self.sample_list.itemClicked.connect(self.choose_data_frame)
        self.std_list.itemClicked.connect(self.choose_data_frame)
        # Отчет
        self.report_btn.clicked.connect(self.report_btn_clicked)

        self.set_data_frame(QFrameDefault)
        self.show()
        # тестовый скрипт (для удобства)
        self.startup()

    def startup(self):
        self.add_sample(r'src/main/python/science/samples/1_1.xlsx')
        self.add_std(r'src/main/python/science/samples/BX_60.txt')

        self.sample_list.setCurrentRow(0)
        self.std_list.setCurrentRow(0)

    def add_sample(self, fname):
        try:
            sample = Sample.from_file(fname)
        except Sample.SampleError as e:
            # TODO: всплывающее окно
            print(e.args[0])
            return
        self.sample_list.addItem(sample.name)

    def add_std(self, fname):
        std = fname[fname.rfind('/') + 1:fname.rfind('.')]
        Standard.from_file(fname, std)
        self.std_list.addItem(std)

    def set_data_frame(self, frame_class, *args):
        if self.data_frame is not None:
            self.data_layout.removeWidget(self.data_frame)
            self.data_frame.hide()
            self.data_frame = None
        self.data_frame = frame_class(self, *args)
        self.data_layout.insertWidget(0, self.data_frame)

    def choose_data_frame(self):
        selected_std = self.std_list.currentItem()
        selected_sample = self.sample_list.currentItem()
        if selected_std is None:
            # TODO: всплывающее окно
            print('Выберите эталон!')
        elif selected_sample is None:
            # TODO: выберите пациента
            print('Выберите пациента!')
        else:
            self.set_data_frame(QFrameSample, selected_sample.text(), selected_std.text())

    # КНОПКИ
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

    def report_btn_clicked(self):
        if hasattr(self.data_frame, "save_report"):
            self.data_frame.save_report()

    def eventFilter(self, widget, event):
        if event.type() == QEvent.Resize and isinstance(widget, QLabel) and hasattr(widget, '_pixmap'):
            if widget._updating:
                widget.setPixmap(widget._pixmap.scaled(widget.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                widget._updating = False
            else:
                widget._updating = True
                ratio = widget._pixmap.height() / widget._pixmap.width()
                widget.setMinimumHeight(widget.width() * ratio + 2)
            return True
        if event.type() == QEvent.Resize and isinstance(widget, QTextEdit) and hasattr(widget, '_custom'):
            if widget._updating:
                widget._updating = False
            else:
                widget._updating = True
                doc_height = widget.document().size().toSize().height()
                widget.setMinimumHeight(doc_height)
        # noinspection PyCallByClass,PyTypeChecker
        return QMainWindow.eventFilter(self, widget, event)
