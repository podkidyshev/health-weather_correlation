from io import BytesIO

from docx import Document
from docx.shared import Cm

import science
import science.funcs


# noinspection PyUnresolvedReferences,PyTypeChecker
class Printer:
    def __init__(self, destination, func, *args):
        self.destination = destination
        if self.destination == 'doc':
            self.doc = Printer.create_docx()
        elif self.destination == 'ui':
            self.doc = ""
        else:
            raise ValueError("Неизвестное назначение")
        func(*args, self)

    def print(self, destination_obj=None):
        if self.destination == 'ui':
            return self.doc
        else:
            Printer.save_docx(self.doc, destination_obj)
            return True

    def add_heading(self, s, size):
        if self.destination == 'doc':
            self.doc.add_heading(s, size)
        else:
            self.doc += '-- {} --\n\n'.format(s)

    def add_paragraph(self, s):
        if self.destination == 'doc':
            self.doc.add_paragraph(s)
        else:
            self.doc += s + '\n'

    def add_picture(self, pic: bytes or bytearray):
        if self.destination == 'doc':
            self.doc.add_picture(BytesIO(pic))

    @staticmethod
    def create_docx():
        doc = Document()
        doc.core_properties.author = "Молчанов В.А."
        return doc

    @staticmethod
    def save_docx(doc, obj):
        # TODO: убрать, настроить default-паттерн в src/docx
        for section in doc.sections:
            section.top_margin = Cm(2)
            section.bottom_margin = Cm(2)
            section.left_margin = Cm(2.5)
            section.right_margin = Cm(1.5)
        doc.save(obj)


def print_report(destination, func, *args):
    return Printer(destination, func, *args).print()


def ntest_report(report, doc: Printer):
    res_ok = "Образец выглядит гауссовским (не может отклонить гипотезу H0)"
    res_nok = "Образец не выглядит гауссовским (отклонить гипотезу H0)"

    shapiro = report["shapiro"]
    doc.add_heading("Тест нормальности Шапиро-Вилка", 2)
    doc.add_paragraph("Statistics = {:.3f}, p = {:.3f}".format(shapiro["stat"], shapiro["p"]))
    doc.add_paragraph((res_ok if shapiro["res"] else res_nok) + '\n')

    agostino = report["agostino"]
    doc.add_heading("D'Agostino and Pearson's Test", 2)
    doc.add_paragraph("Statistics = {:.3f}, p = {:.3f}".format(agostino["stat"], agostino["p"]))
    doc.add_paragraph((res_ok if agostino["res"] else res_nok) + '\n')

    anderson = report["anderson"]
    doc.add_heading("Тест нормальности Андерсона-Дарлинга", 2)
    doc.add_paragraph("Statistic = {:.3f}".format(anderson["statistic"]))
    for res, cv, sl in zip(anderson["res"], anderson["critical"], anderson["sig_level"]):
        doc.add_paragraph("{:.3f}: {:.3f}, {}\n".format(sl, cv, res_ok if res else res_nok))

    ks = report["ks"]
    doc.add_heading("Тест нормальности Колмогорова-Смирнова", 2)
    num_tests = ks["num_tests"]
    num_rejects = ks["num_rejects"]
    ratio = ks["ratio"]
    alpha = ks["alpha"]
    doc.add_paragraph(
        "Результаты теста Колмогорова-Смирнова: "
        "из {} прогонов доля {}/{} = {:.2f} отклоняет гипотезу H0 на уровне отклонения {}\n".format(
            num_tests, num_rejects, num_tests, ratio, alpha))

    if report['qq']:
        img = science.plot_image(science.funcs.test_normal_plot, report, io=True)
        doc.add_picture(img)
