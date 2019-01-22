from science import FACTORS
from science.classes import Sample, Standard

from reports.std_mul import FactorSampleMulStandards, SampleMulStandards
from reports.std_mul import MulFactorSamplesStandard, MulSamplesStandard, MulSamplesMulStandards
from reports.utils import Printer

from logic import QFrameBase, dialog_save_report
from logic.utils import QFrameInfo
from logic.sample import QFrameSample

from frames.sample import Ui_FramePatient
from frames.mul_one import Ui_FrameMulOne


class QFrameMulSamples(QFrameBase, Ui_FramePatient):
    def __init__(self, parent, std, samples):
        QFrameBase.__init__(self, parent, Ui_FramePatient)
        self.std = Standard.standards[std]
        self.samples = [Sample.samples[name] for name in samples]

        self.report = MulSamplesStandard(self.samples, self.std)
        self.reports, self.frames = [], []

        self.tabs.removeTab(0)
        for factor in range(4):
            self.reports.append(MulFactorSamplesStandard(self.samples, factor, self.std))
            self.frames.append(QFrameInfo(self, self.reports[-1]))
            self.tabs.widget(factor).layout().insertWidget(0, self.frames[-1])

        self.title_label.setText("Эталон {} и группа образцов".format(self.std.name))


class QFrameStdMulSamples(QFrameBase, Ui_FrameMulOne):
    def __init__(self, parent, std):
        QFrameBase.__init__(self, parent, Ui_FrameMulOne)

        self.samples = list(Sample.samples.values())
        self.std = Standard.standards[std]

        self.report_frame = QFrameMulSamples(self, self.std.name, [s.name for s in self.samples])
        self.layout_vertical.insertWidget(1, self.report_frame)

    def save_report(self):
        fname = dialog_save_report("Группа образцов. Эталон {}".format(self.std.name))
        if fname:
            Printer('doc', self.report_frame.report.get_report).print(fname)
