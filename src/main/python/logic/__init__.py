import os
import sys

from PyQt5.QtCore import QSize
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
    def __init__(self, parent, child_frame_class):
        # noinspection PyArgumentList
        QFrame.__init__(self, parent=parent)
        child_frame_class.setupUi(self, self)
        self.resize(500, 500)
        self.setMinimumSize(QSize(250, 250))
        self.layout().setContentsMargins(0, 0, 0, 0)
