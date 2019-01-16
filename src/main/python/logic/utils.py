from logic import QFrameBase, dialog_save

from frames.info import Ui_FrameInfo
from frames.kde import Ui_FrameKde
from frames.image import Ui_FrameImage
from frames.text import Ui_FrameText

from science import print_report


class QFrameInfo(QFrameBase, Ui_FrameInfo):
    def __init__(self, parent, report, val_type: str = "val"):
        QFrameBase.__init__(self, parent, Ui_FrameInfo)
        self.report = report
        self.val_type = val_type

        self.frames = [QFrameImage(self, self.report, self.val_type), QFrameText(self, self.report, self.val_type, 'stat'),
                       QFrameText(self, self.report, self.val_type, 'ntest')]

        for info in range(3):
            self.tabs.widget(info).layout().insertWidget(0, self.frames[info])


# Убрать, объединить в одно с классом Info
class QFrameInfoKde(QFrameBase, Ui_FrameInfo):
    def __init__(self, parent, report, val_type: str = "val"):
        QFrameBase.__init__(self, parent, Ui_FrameInfo)
        self.report = report
        self.val_type = val_type

        self.frames = [QFrameKde(self, self.report), QFrameText(self, self.report, self.val_type, 'stat'),
                       QFrameText(self, self.report, self.val_type, 'ntest')]

        for info in range(3):
            self.tabs.widget(info).layout().insertWidget(0, self.frames[info])


# KDE куда лучше убрать
class QFrameKde(QFrameBase, Ui_FrameKde):
    def __init__(self, parent, report):
        QFrameBase.__init__(self, parent, Ui_FrameKde)
        self.report = report

        self.frames = [QFrameImage(self, self.report, "kde"), QFrameImage(self, self.report, "kde3")]

        for info in range(2):
            self.tabs.widget(info).layout().insertWidget(0, self.frames[info])


# Проблема со скролером изображений
class QFrameImage(QFrameBase, Ui_FrameImage):
    def __init__(self, parent, report, va_type: str):
        QFrameBase.__init__(self, parent, Ui_FrameImage)
        self.report = report
        self.va_type = va_type

        self.va, self.image_name = self.get_va()

        self.add_image(self.va, self.image, self.image_name)

    # Убрать отсюда
    def get_va(self):
        if self.va_type == "val":
            return self.report.va, 'va_img1'
        elif self.va_type == "apl":
            return self.report.va_apl, 'va_img2'
        elif self.va_type == "kde":
            return self.report.kde, 'label_kde_img'
        elif self.va_type == "kde3":
            return self.report.kde3, 'label_kde3_img'


class QFrameText(QFrameBase, Ui_FrameText):
    def __init__(self, parent, report, val_type: str, func_name: str):
        QFrameBase.__init__(self, parent, Ui_FrameText)
        self.report = report
        self.val_type = val_type
        self.func_name = func_name

        self.add_text(print_report('ui', self.get_func()), self.text_edit)

    # Убрать отсюда
    def get_func(self):
        if self.val_type == "val":
            return self.func_val()
        elif self.val_type == "apl":
            return self.func_apl()
        elif self.val_type == "kde":
            return self.func_kde()

    # Убрать отсюда
    def func_val(self):
        if self.func_name == "stat":
            return self.report.get_report_stat
        else:
            return self.report.get_report_ntest

    # Убрать отсюда
    def func_apl(self):
        if self.func_name == "stat":
            return self.report.get_report_stat_apl
        else:
            return self.report.get_report_ntest_apl

    # Убрать отсюда
    def func_kde(self):
        if self.func_name == "stat":
            return self.report.get_report_stat3
        else:
            return self.report.get_report_ntest3

