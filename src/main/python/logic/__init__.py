import os
import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QTextCursor
from PyQt5.QtWidgets import QFrame, QFileDialog, QLabel, QTextEdit, QVBoxLayout


root = os.path.dirname(sys.argv[0])
main_window = None

_samples = os.path.join(root, "science", "samples")
samples = _samples if os.path.exists(_samples) else root

last_open = ""
last_save = ""


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
    global last_open
    path = samples if last_open == "" else last_open

    dialog = QFileDialog(main_window, title, path, get_file_filter(formats))
    dialog.setLabelText(QFileDialog.Accept, "Добавить")
    dialog.setLabelText(QFileDialog.Reject, "Отмена")
    dialog.setAcceptMode(QFileDialog.AcceptOpen)
    dialog.setFileMode(QFileDialog.ExistingFile)

    if dialog.exec():
        fname = dialog.selectedFiles()[0]
        if fname and not os.path.exists(fname):
            raise ValueError("Выбранный файл не существует")
        last_open = os.path.dirname(fname)
        return fname
    else:
        return ""


def dialog_save(title, *formats, filename=''):
    global last_save
    path = root if last_save == "" else last_save

    dialog = QFileDialog(main_window, title, path, get_file_filter(formats))
    dialog.setLabelText(QFileDialog.Accept, "Сохранить")
    dialog.setLabelText(QFileDialog.Reject, "Отмена")
    dialog.setAcceptMode(QFileDialog.AcceptSave)
    dialog.selectFile(filename)

    if dialog.exec():
        fname = dialog.selectedFiles()[0]
        last_save = os.path.dirname(fname)
        return fname
    return ""


def dialog_save_report(filename):
    return dialog_save("Сохранить отчет", "docx", filename=filename)


class QFrameBase(QFrame):
    class QFrameBaseException(Exception):
        pass

    def __init__(self, parent, child_frame_class=None):
        # noinspection PyArgumentList
        QFrame.__init__(self, parent=parent)
        if child_frame_class is not None:
            child_frame_class.setupUi(self, self)
        self.resize(500, 500)
        self.setMinimumSize(QSize(500, 500))

        if child_frame_class is None:
            QVBoxLayout(self)
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

    @staticmethod
    def get_custom(ui_class):
        class QFrameCustom(QFrameBase, ui_class):
            pass
        return QFrameCustom
