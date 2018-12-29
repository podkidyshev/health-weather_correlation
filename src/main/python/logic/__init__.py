import os
import sys

from PIL.ImageQt import ImageQt

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QFrame, QFileDialog


root = os.path.dirname(sys.argv[0])
samples = os.path.join(root, "science", "samples")


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

    def add_image(self, img_obj, img_label, canvas_name, **kwargs):
        """
        принимает PIL-изображение и рисует на img-label картинку:
        добавляет необходимые объекты в корневой объект и конфигурирует лейбл
        :param img_obj: PIL-изображение для рисование
        :param img_label: лейбл, на котором рисовать
        :param canvas_name: имя объекта канваса - должно быть уникальным
        :param kwargs: на всякий случай
        :return: None
        """
        img_name = canvas_name + 'img'

        if img_name in self.__dict__ or canvas_name in self.__dict__:
            raise QFrameBase.QFrameBaseException('img_name и canvas_name должны быть уникальны')

        self.__dict__[img_name] = QImage(ImageQt(img_obj))
        self.__dict__[canvas_name] = QPixmap.fromImage(self.__dict__[img_name])

        img_label.setPixmap(self.__dict__[canvas_name])
        img_label.setScaledContents(True)
        img_label.setMinimumSize(QSize(200, 200))
