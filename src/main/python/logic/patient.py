import matplotlib.pyplot as plt

from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel

from logic import BaseFrame, dialog_save
from frames.patient import Ui_FramePatient

from science import plot_to_image, create_docx, save_docx
from science.classes import Standard, Patient
from science.single_patient import StandardPatientStat
from science.funcs import graph_kde


class QPatientFrame(BaseFrame, Ui_FramePatient):
    def __init__(self, parent, pat_name, std_name):
        BaseFrame.__init__(self, parent, Ui_FramePatient)

        self.std = Standard.standards[std_name]
        self.pat = Patient.patients[pat_name]
        self.report = StandardPatientStat(self.std, self.pat)

        self.plot = plt.figure()
        graph_kde(self.report.get_report_item("distance"), self.plot)
        self.img_qt = ImageQt(plot_to_image(self.plot))
        self.img = QImage(self.img_qt)

        self.plot_canvas = QPixmap.fromImage(self.img)

        self.label = QLabel(self)
        self.tab_graphics.layout().insertWidget(0, self.label)

        self.label.setPixmap(self.plot_canvas)
        self.label.setScaledContents(True)

        self.get_report()

    def save_report(self):
        fname = dialog_save(self, "Сохранить отчет")
        doc = create_docx()
        self.report.get_report(doc)
        save_docx(doc, fname)

    def get_report(self):
        pass
        # for cat_s, cat_l in CATS:
        #     self.pat.add_category(cat_s, "science/samples/1_1{}.txt".format(cat_s))
        # тест добавленяи информации в форму
        # self.tab.layout = QGridLayout(self)
        # self.text = QTextEdit()
        # self.tab.layout.addWidget(self.text)
        # self.tab.setLayout(self.tab.layout)
        # self.text.append("12312")
        # self.show()
