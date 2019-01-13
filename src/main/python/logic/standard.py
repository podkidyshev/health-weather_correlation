from logic import QFrameBase, dialog_save
from logic.factor import QFrameFactor
from frames.standard import Ui_FrameStandard

from science import Printer
from science.classes import Standard, Sample
from science.reports import StandardFactorSample, StandardSample


class QFrameStandard(QFrameBase, Ui_FrameStandard):
    def __init__(self, parent, sample_name, std_name):
        QFrameBase.__init__(self, parent, Ui_FrameStandard)

        self.std = Standard.standards[std_name]
        self.sample = Sample.samples[sample_name]

        self.title_label.setText("Погода {}".format(std_name))

        self.report = StandardSample(self.std, self.sample)

        self.reports = []
        self.frames = []
        for factor in range(4):
            self.reports.append(StandardFactorSample(self.std, factor, self.sample))
            self.frames.append(QFrameFactor(self, self.reports[-1]))
            self.tabs.widget(factor).layout().insertWidget(0, self.frames[-1])

    def save_report(self):
        fname = dialog_save(self, "Сохранить отчет")
        Printer('doc', self.report.get_report).print(fname)