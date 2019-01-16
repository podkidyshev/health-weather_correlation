import os
import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QTextCursor
from PyQt5.QtWidgets import QFrame, QFileDialog, QLabel, QTextEdit, QCheckBox

from frames.check import Ui_FrameCheck
from frames.combo import Ui_FrameCombo


root = os.path.dirname(sys.argv[0])
main_window = None

_samples = os.path.join(root, "science", "samples")
samples = _samples if os.path.exists(_samples) else root


def set_main_window(window):
    global main_window
    main_window = window


def get_file_filter(formats: tuple):
    file_filter = ""
    if "" not in formats:
        formats += ("",)
    for f in formats:
        if f == "":
            file_filter += "Все файлы (*);;"
        elif f == "txt":
            file_filter += "Текстовые файлы (*.txt);;"
        elif f == "xlsx":
            file_filter += "Файлы таблиц xlsx (*.xlsx);;"
        elif f == "docx":
            file_filter += "Текстовые документы (*.docx);;"
        else:
            raise ValueError("Неизвестный формат файла")
    return file_filter[:-2]


def dialog_open(title, *formats):
    # TODO: разобраться с диалогами
    dialog = QFileDialog(main_window, title, samples, get_file_filter(formats))
    dialog.setLabelText(QFileDialog.Accept, "Добавить")
    dialog.setLabelText(QFileDialog.Reject, "Отмена")
    dialog.setAcceptMode(QFileDialog.AcceptOpen)
    dialog.setFileMode(QFileDialog.ExistingFile)

    if dialog.exec():
        fname = dialog.selectedFiles()[0]
        if fname and not os.path.exists(fname):
            raise ValueError("Выбранный файл не существует")
        return fname
    else:
        return ""


def dialog_save(title, *formats, filename=''):
    dialog = QFileDialog(main_window, title, root, get_file_filter(formats))
    dialog.setLabelText(QFileDialog.Accept, "Сохранить")
    dialog.setLabelText(QFileDialog.Reject, "Отмена")
    dialog.setAcceptMode(QFileDialog.AcceptSave)
    dialog.selectFile(filename)
    return dialog.selectedFiles()[0] if dialog.exec() else ""


def dialog_save_report(filename):
    return dialog_save("Сохранить отчет", "docx", filename=filename)


class QFrameBase(QFrame):
    class QFrameBaseException(Exception):
        pass

    def __init__(self, parent, child_frame_class):
        # noinspection PyArgumentList
        QFrame.__init__(self, parent=parent)
        if child_frame_class is not None:
            child_frame_class.setupUi(self, self)
        self.resize(500, 500)
        self.setMinimumSize(QSize(500, 500))
        self.layout().setContentsMargins(0, 0, 0, 0)

    def add_image(self, img_obj: bytes or bytearray, img_label: QLabel, img_name: str):
        """
        принимает PIL-изображение и рисует на img-label картинку:
        добавляет необходимые объекты в корневой объект и конфигурирует лейбл
        ВАЖНО!
        label.sizePolicy: Expanding, Maximum
        label_layout.layoutSizeConstraint.SetDefaultSizeConstraint
        ВАЖНО!
        :param img_obj: PIL-изображение для рисование
        :param img_label: лейбл, на котором рисовать
        :param img_name: имя объекта изображения - должно быть уникальным в self.__dict__
        :return: None
        """
        if img_name in self.__dict__:
            raise QFrameBase.QFrameBaseException('img_name должно быть уникальным')

        pixmap = QPixmap()
        pixmap.loadFromData(img_obj)
        self.__dict__[img_name] = pixmap

        img_label._pixmap = pixmap
        img_label.setPixmap(pixmap.scaled(img_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        img_label._updating = False
        img_label.setAlignment(Qt.AlignCenter)
        img_label.setMinimumSize(QSize(200, 200))

        img_label.installEventFilter(main_window)
        img_label.updateGeometry()

    def add_text(self, text: str, text_edit: QTextEdit):
        # scroll area: лейаут, ей содержащий - layoutSizeConstraint->SetMinimumSize
        # у самого лейаута scroll area то же самое
        text_edit.setFontPointSize(13)
        text_edit.insertPlainText(text)
        text_edit.document().adjustSize()
        text_edit.verticalScrollBar().setEnabled(False)

        cursor = QTextCursor()
        cursor.movePosition(QTextCursor.Start)
        text_edit.setTextCursor(cursor)

        text_edit._custom = True
        text_edit._updating = False

        text_edit.installEventFilter(main_window)


class QFrameCheck(QFrame, Ui_FrameCheck):
    def __init__(self, parent, values):
        # noinspection PyArgumentList
        QFrame.__init__(self, parent=parent)
        Ui_FrameCheck.setupUi(self, self)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.values = values
        self.cbs = []
        for idx, value in enumerate(values):
            cb = QCheckBox(value, self)
            cb.setChecked(1)
            # noinspection PyUnresolvedReferences
            cb.stateChanged.connect(self.state_changed)
            self.cbs.append(cb)
            self.scroll_contents.layout().insertWidget(idx, cb)

        self.signal_func = None

    def get_turned(self):
        pressed = [cb.isChecked() for cb in self.cbs]
        values_pressed = []
        for p, v in zip(pressed, self.values):
            if p:
                values_pressed.append(v)
        return values_pressed

    def state_changed(self, *_):
        if self.signal_func is not None:
            self.signal_func(self.get_turned())


class QFrameCombo(QFrame, Ui_FrameCombo):
    def __init__(self, parent, values):
        # noinspection PyArgumentList
        QFrame.__init__(self, parent=parent)
        Ui_FrameCombo.setupUi(self, self)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.update_values(values)
        self.signal_func = None

    def update_values(self, values):
        try:
            self.combo.currentIndexChanged.disconnect()
        except TypeError:
            pass
        self.combo.clear()
        for value in values:
            self.combo.addItem(value)
        self.combo.currentIndexChanged.connect(self.combo_changed)

    def combo_changed(self, *_):
        if self.signal_func is not None:
            value = self.combo.currentText()
            self.signal_func(value)
