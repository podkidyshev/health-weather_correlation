from logic import QFrameBase, dialog_save_report
from logic.utils import QFrameInfo, QFrameInfoKde

from frames.sample import Ui_FramePatient

from science import print_report, Printer
from science.classes import Standard, Sample
from science.reports import FactorSampleStandard, SampleStandard


class QFrameSample(QFrameBase, Ui_FramePatient):
    def __init__(self, parent, std_name, sample_name):
        QFrameBase.__init__(self, parent, Ui_FramePatient)

        self.std = Standard.standards[std_name]
        self.sample = Sample.samples[sample_name] if sample_name != "--Групповой--" else Sample.group

        self.report = SampleStandard(self.sample, self.std)

        self.title_label.setText("{}".format(self.report.sample_name))

        self.reports = []
        self.frames = []
        for factor in range(4):
            self.reports.append(FactorSampleStandard(self.sample, factor, self.std))
            self.frames.append(QFrameInfo(self, self.reports[-1]))
            self.tabs.widget(1 + factor).layout().insertWidget(0, self.frames[-1])

        self.tabs.widget(0).layout().insertWidget(0, QFrameInfoKde(self, self.report, "kde"))

    def save_report(self):
        sample_name_pretty = "Образец {}".format(self.sample.name) if self.sample.name != "group" \
            else self.report.sample_name
        fname = dialog_save_report("{} Эталон {}".format(sample_name_pretty, self.std.name))
        if fname:
            Printer('doc', self.report.get_report).print(fname)
