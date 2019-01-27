from PyQt5.QtWidgets import QCheckBox, QDialog, QDialogButtonBox, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from logic import QFrameBase, error_dialog

from frames.default import Ui_FrameDefault
from frames.utils.info import Ui_FrameInfo
from frames.utils.kde import Ui_FrameKde
from frames.utils.image import Ui_FrameImage
from frames.utils.text import Ui_FrameText
from frames.utils.standard_type import Ui_FrameStandardType
from frames.dialogs.stds import Ui_DialogStds

from reports import print_report

from science import FACTORS_ALL
from science.classes import Standard


class QFrameDefault(QFrameBase, Ui_FrameDefault):
    INSTRUCTIONS = \
"""Терминология:
  *  параметры погоды называются Эталонами, 
  *  медицинские данные пациентов называются Образцами, 
  *  отдельные факторы Образцов называются фактор-образцами
Все данные в программы представлены вещественными числами, дробная часть отделяется от целой символом точки.

С помощью кнопок «Добавить» загружаем данные из папки «samples»: 
     «Эталоны» – параметры погоды, загружаются временными рядами из txt-файлов (каждая строчка файла – одно число, без знаков препинания); 
     «Пациенты» – медицинские данные пациентов загружаются сразу четырьмя временными рядами (по факторам «без нагрузки», с физической нагрузкой», «с эмоциональной нагрузкой», «после отдыха») из xlsx-файлов. Столбец A – фактор "без нагрузки" и так далее столбцы BCD. Каждая ячейка – дробное число.
В окне выбора файла можно выбрать сразу несколько файлов (выделив их курсором или с помощью клавиш Ctrl/Shift).

     В окне «Ведущий ряд» выбирается любой из загруженных файлов, затем в окне «Ведомый ряд» выбирается также любой из загруженных файлов (ряды распределения расстояний формируются от максимумов Ведомого ряда до максимумов Ведущего ряда)
     
     В основном окне показываются фрагменты анализа в зависимости от выбранных кнопок «Все факторы», «Без нагрузки», «С физической нагрузкой», «С эмоциональной нагрузкой», «После отдыха», «Визуализация», «Статистика», «Тестирование нормальности», «4-х ядерные оценки» (график показывает ядерные оценки плотности распределений для всех факторов), «3-х ядерные оценки» (график показывает ядерные оценки плотности распределений расстояний от максимумов факторов «С физической нагрузкой», «С эмоциональной нагрузкой», «После отдыха» до фактора «Без нагрузки»)

     Для формирования файла отчета (в формате docx) по выбранному эталону необходимо нажать кнопку «Сформировать отчет», в открывшемся окне выбрать фактор или все факторы и нажать кнопку «Сохранить» – будет предложено выбрать название файла и место для сохранения.
     Для формирования файла отчета (в формате docx) по группе эталонов необходимо нажать кнопку «Сформировать групповой отчет», в открывшемся окне выбрать группу эталонов и фактор и нажать кнопку «Сохранить» – будет предложено выбрать название файла и место для сохранения.
"""

    def __init__(self, parent):
        QFrameBase.__init__(self, parent, Ui_FrameDefault)
        self.add_text(QFrameDefault.INSTRUCTIONS, self.instructions_edit)
        delattr(self.instructions_edit, "c_updating")
        font = QFont("Times New Roman", 11)
        self.instructions_edit.setFont(font)
        self.instructions_edit.verticalScrollBar().setEnabled(True)


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


class QDialogStds(QDialog, Ui_DialogStds):
    def __init__(self, parent, **kwargs):
        # noinspection PyArgumentList
        QDialog.__init__(self, parent)
        Ui_DialogStds.setupUi(self, self)

        self.dimension = 1
        self.result = None
        # Эталоны
        self.get_stds = kwargs.get("get_stds", False)
        self.std_main = kwargs.get("std_main", None)
        if self.get_stds:
            self.dimension += 1

        # Факторы
        self.btn_all.setChecked(True)
        # Эталоны
        if self.get_stds:
            self.cbs = []
            for v in reversed(sorted(list(Standard.standards.keys()))):
                self.cbs.append(QCheckBox(v, self))
                if self.std_main is None or self.std_main != v:
                    self.cbs[-1].setChecked(False)
                else:
                    self.cbs[-1].setChecked(1)
                self.layout_stds.insertWidget(0, self.cbs[-1])
        else:
            self.layout().removeItem(self.layout_stds)

        self.buttons.button(QDialogButtonBox.Save).setText("Сохранить")
        self.buttons.button(QDialogButtonBox.Cancel).setText("Отмена")
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)

    def accept(self):
        self.result = []
        # Факторы
        if self.btn_all.isChecked():
            factor = FACTORS_ALL
        else:
            for idx in range(4):
                if self.__dict__["btn_{}".format(idx)].isChecked():
                    factor = idx
                    break
            else:
                error_dialog("Не выбран ни один фактор/все факторы")
                return
        self.result.append(factor)
        # Эталоны
        if self.get_stds:
            stds = [cb.text() for cb in self.cbs if cb.isChecked()]
            if not len(stds):
                error_dialog("Выберите по крайней мере один эталон")
                return
            self.result.append(stds)

        QDialog.accept(self)

    @staticmethod
    def settings(parent, **kwargs):
        dialog = QDialogStds(parent, **kwargs)
        if dialog.exec():
            res = dialog.result
        else:
            res = [None] * dialog.dimension
        return res[0] if len(res) == 1 else res
