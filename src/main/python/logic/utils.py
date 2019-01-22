from PyQt5.QtWidgets import QCheckBox, QDialog, QDialogButtonBox
from PyQt5.QtCore import Qt

from logic import QFrameBase

from frames.default import Ui_FrameDefault
from frames.utils.info import Ui_FrameInfo
from frames.utils.kde import Ui_FrameKde
from frames.utils.image import Ui_FrameImage
from frames.utils.text import Ui_FrameText
from frames.utils.standard_type import Ui_FrameStandardType
from frames.dialogs.stds import Ui_DialogGroup
from frames.dialogs.factors import Ui_DialogFactors

from reports import print_report

from science import FACTORS_ALL


class QFrameDefault(QFrameBase, Ui_FrameDefault):
    def __init__(self, parent):
        QFrameBase.__init__(self, parent, Ui_FrameDefault)


class QFrameInfo(QFrameBase, Ui_FrameInfo):
    def __init__(self, parent, report, val_type: str = "val"):
        QFrameBase.__init__(self, parent, Ui_FrameInfo)
        self.report = report
        self.val_type = val_type

        self.frames = [QFrameImage(self, self.report, self.val_type),
                       QFrameText(self, self.report, self.val_type, 'stat'),
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


class QFrameStandardType(QFrameBase, Ui_FrameStandardType):
    def __init__(self, parent, report):
        QFrameBase.__init__(self, parent, Ui_FrameStandardType)
        self.report = report

        self.frames = [QFrameInfo(self, self.report, "val"), QFrameInfo(self, self.report, "apl")]

        for info in range(2):
            self.tabs.widget(info).layout().insertWidget(0, self.frames[info])


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


class QDialogGroup(QDialog, Ui_DialogGroup):
    def __init__(self, parent, values):
        # noinspection PyArgumentList
        QDialog.__init__(self, parent)
        Ui_DialogGroup.setupUi(self, self)

        self.values = None
        self.cbs = []
        for v in reversed(values):
            self.cbs.append(QCheckBox(v, self))
            self.cbs[-1].setChecked(1)
            self.layout().insertWidget(0, self.cbs[-1])

        self.buttons.button(QDialogButtonBox.Save).setText("Сохранить")
        self.buttons.button(QDialogButtonBox.Cancel).setText("Отмена")
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)

    def accept(self):
        self.values = [cb.text() for cb in self.cbs if cb.isChecked()]
        QDialog.accept(self)


class QDialogGroupFactor(QDialog, Ui_DialogFactors):
    def __init__(self, parent):
        # noinspection PyArgumentList
        QDialog.__init__(self, parent)
        Ui_DialogFactors.setupUi(self, self)

        self.factor = FACTORS_ALL
        self.btn_all.setChecked(True)

        self.buttons.button(QDialogButtonBox.Save).setText("Сохранить")
        self.buttons.button(QDialogButtonBox.Cancel).setText("Отмена")
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)

    def accept(self):
        if self.btn_all.isChecked():
            self.factor = FACTORS_ALL
        else:
            for factor in range(4):
                if self.__dict__["btn_{}".format(factor)].isChecked():
                    self.factor = factor
        QDialog.accept(self)

    @staticmethod
    def get_factor(parent):
        dialog = QDialogGroupFactor(parent)
        return dialog.factor if dialog.exec() else None
