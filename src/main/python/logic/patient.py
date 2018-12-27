import matplotlib.pyplot as plt

from PyQt5.QtGui import QPixmap

from logic import QFrameBase, dialog_save
from frames.patient import Ui_FramePatient

from science import plot_to_qimage, create_docx, save_docx
from science.classes import Standard, Sample
from science.single_patient import StandardPatientStat
from science.funcs import graph_kde


class QFramePatient(QFrameBase, Ui_FramePatient):
    def __init__(self, parent, pat_name, std_name):
        QFrameBase.__init__(self, parent, Ui_FramePatient)

        self.std = Standard.standards[std_name]
        self.pat = Sample.samples[pat_name]
        self.report = StandardPatientStat(self.std, self.pat)

        self.plot = plt.figure()
        graph_kde(self.report.get_report_item("distance"), self.plot)
        self.img = plot_to_qimage(self.plot)
        self.plot_canvas = QPixmap.fromImage(self.img)

        self.graph_label.setPixmap(self.plot_canvas)
        self.graph_label.setScaledContents(True)

        self.std_pat_label.setText("Пациент {}".format(self.pat.name))

    def save_report(self):
        fname = dialog_save(self, "Сохранить отчет")
        doc = create_docx()
        self.report.get_report(doc)
        save_docx(doc, fname)
