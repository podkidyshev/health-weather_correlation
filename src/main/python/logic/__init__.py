import os
import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QTextCursor
from PyQt5.QtWidgets import QFrame, QFileDialog, QLabel, QTextEdit


root = os.path.dirname(sys.argv[0])
main_window = None
samples = os.path.join(root, "science", "samples")


def set_main_window(window):
    global main_window
    main_window = window


def get_file_filter(formats):
    file_filter = ""
    for f in formats:
        if f == "":
            file_filter += "Все файлы (*);;"
        elif f == "txt":
            file_filter = "Текстовые файлы (*.txt);;"
        elif f == "xlsx":
            file_filter = "Файлы таблиц xlsx (*.xlsx, *xls);;"
        else:
            raise ValueError("Неизвестный формат файла")


def dialog_open(parent, title, path=samples, *formats):
    # TODO: разобраться с диалогами
    dialog = QFileDialog(main_window)
    dialog.setLabelText(QFileDialog.Accept, "Добавить")
    dialog.setLabelText(QFileDialog.Reject, "Отмена")
    dialog.setDirectory(path)
    dialog.setWindowTitle(title)

    if dialog.exec():
        fname = dialog.selectedFiles()[0]
        if fname and not os.path.exists(fname):
            raise ValueError("Выбранный файл не существует")
        return fname
    else:
        return ""


def dialog_save(parent, title, path=root, file_format=''):
    dialog = QFileDialog(main_window)
    dialog.setLabelText(QFileDialog.Accept, "Добавить")

    dialog.setLabelText(QFileDialog.Reject, "Отмена")
    dialog.setDirectory(path)
    dialog.setWindowTitle(title)

    dialog.setAcceptMode(QFileDialog.AcceptSave)
    return dialog.selectedFiles()[0] if dialog.exec() else ""


class QFrameBase(QFrame):
    class QFrameBaseException(Exception):
        pass

    def __init__(self, parent, child_frame_class):
        # noinspection PyArgumentList
        QFrame.__init__(self, parent=parent)
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
