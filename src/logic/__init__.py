import os
import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QTextCursor
from PyQt5.QtWidgets import QFrame, QFileDialog, QLabel, QTextEdit, QVBoxLayout, QMessageBox


root = os.path.dirname(sys.argv[0])
main_window = None

_samples_dev = os.path.join(root, "science", "samples")
_samples_exe = os.path.join(root, "samples")
PATH_SAMPLES = _samples_exe if os.path.exists(_samples_exe) else _samples_dev if os.path.exists(_samples_dev) else root

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
            error_dialog("Попытка получить фильтр на неизвестный формат файла: {}".format(f), unknown=True)
    return file_filter[:-2]


def dialog_open(title, *formats):
    global last_open
    path = PATH_SAMPLES if last_open == "" else last_open

    dialog = QFileDialog(main_window, title, path, get_file_filter(formats))
    dialog.setLabelText(QFileDialog.Accept, "Добавить")
    dialog.setLabelText(QFileDialog.Reject, "Отмена")
    dialog.setAcceptMode(QFileDialog.AcceptOpen)
    dialog.setFileMode(QFileDialog.ExistingFiles)

    if dialog.exec():
        fnames = dialog.selectedFiles()
        if not fnames:
            return
        for fname in fnames:
            if not os.path.exists(fname):
                error_dialog("Файл не существует: {}".format(fname))
                return
        last_open = os.path.dirname(fnames[0])
        return fnames
    else:
        return


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


def error_dialog(msg, *, unknown=False):
    mbox = QMessageBox()
    mbox.setWindowTitle(main_window.windowTitle())
    msg = msg if isinstance(msg, str) else msg.args[0]
    if unknown:
        if isinstance(msg, str):
            mbox.setText("НЕИЗВЕСТНАЯ ОШИБКА: " + msg +
                         "\nПожалуйста сделайте скриншот экрана и свяжитесь с разработчиком")
        else:
            mbox.setText("НЕИЗВЕСТНАЯ ОШИБКА: \nПожалуйста сделайте скриншот экрана и свяжитесь с разработчиком")
    else:
        mbox.setText("ОШИБКА: " + msg)
    mbox.setIcon(QMessageBox.Warning)
    mbox.exec()


class QFrameBase(QFrame):
    class QFrameBaseException(Exception):
        pass

    def __init__(self, parent, child_frame_class=None):
        # noinspection PyArgumentList
        QFrame.__init__(self, parent=parent)
        if child_frame_class is not None:
            child_frame_class.setupUi(self, self)
        self.setMinimumSize(QSize(300, 300))

        if child_frame_class is None:
            QVBoxLayout(self)
        self.layout().setContentsMargins(5, 0, 5, 0)

    def add_image(self, img_obj: bytes or bytearray, img_label: QLabel, img_name: str):
        if img_name in self.__dict__:
            raise QFrameBase.QFrameBaseException('img_name должно быть уникальным')

        pixmap = QPixmap()
        pixmap.loadFromData(img_obj)
        self.__dict__[img_name] = pixmap

        img_label.plot_pixmap = pixmap
        img_label.setPixmap(pixmap.scaled(img_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        img_label.setAlignment(Qt.AlignCenter)
        img_label.setMinimumSize(QSize(300, 300))

        img_label.installEventFilter(main_window)
        img_label.updateGeometry()

    def add_text(self, text: str, text_edit: QTextEdit):
        text_edit.setFontPointSize(13)
        text_edit.insertPlainText(text)
        text_edit.document().adjustSize()
        text_edit.verticalScrollBar().setEnabled(False)

        cursor = QTextCursor()
        cursor.movePosition(QTextCursor.Start)
        text_edit.setTextCursor(cursor)

        text_edit.c_updating = False

        text_edit.installEventFilter(main_window)
        self.__dict__["has_text"] = True

    @staticmethod
    def get_custom(ui_class):
        class QFrameCustom(QFrameBase, ui_class):
            pass
        return QFrameCustom
