import os
import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QFileDialog, QLabel


root = os.path.dirname(sys.argv[0])
main_window = None
samples = os.path.join(root, "science", "samples")


def set_main_window(window):
    global main_window
    main_window = window


def dialog_open(parent, title, path=samples):
    fname, _ = QFileDialog.getOpenFileName(parent, title, path, options=QFileDialog.Options())
    return fname


def dialog_save(parent, title, path=root):
    fname, _ = QFileDialog.getSaveFileName(parent, title, path, options=QFileDialog.Options())
    return fname


class QFrameBase(QFrame):
    class QFrameBaseException(Exception):
        pass

    def __init__(self, parent, child_frame_class):
        # noinspection PyArgumentList
        QFrame.__init__(self, parent=parent)
        child_frame_class.setupUi(self, self)
        self.resize(500, 500)
        self.setMinimumSize(QSize(500, 250))
        self.layout().setContentsMargins(0, 0, 0, 0)

    def add_image(self, img_obj: bytes or bytearray, img_label: QLabel, img_name: str):
        """
        принимает PIL-изображение и рисует на img-label картинку:
        добавляет необходимые объекты в корневой объект и конфигурирует лейбл
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

        img_label.installEventFilter(main_window)
        img_label._pixmap = pixmap
        img_label.setPixmap(pixmap)
        img_label.setAlignment(Qt.AlignCenter)
        img_label.setMinimumSize(QSize(600, 600))
