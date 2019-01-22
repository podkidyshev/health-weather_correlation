from science.classes import Sample, Standard

from reports.sample_mul import MulStandardsSample, StandardMulSamples, StandardMulFactorSamples, MulStandardsMulSamples
from reports.utils import Printer

from logic import QFrameBase, dialog_save_report
from logic.utils import QFrameStandardType

from frames.standard import Ui_FrameStandard


# TODO: таб значения/амплитуды некорректно ресайзится
class QFrameMulSamples(QFrameBase, Ui_FrameStandard):
    def __init__(self, parent, std, samples):
        QFrameBase.__init__(self, parent, Ui_FrameStandard)
        self.std = Standard.standards[std]
        self.samples = [Sample.samples[name] for name in samples]

        self.report = StandardMulSamples(self.std, self.samples)
        self.reports, self.frames = [], []

        for factor in range(4):
            self.reports.append(StandardMulFactorSamples(self.std, self.samples, factor))
            self.frames.append(QFrameStandardType(self, self.reports[-1]))
            self.tabs.widget(factor).layout().insertWidget(0, self.frames[-1])

        self.title_label.setText("Группа образцов и эталон {}".format(self.std.name))


class QFrameMulSamplesStd(QFrameBase):
    def __init__(self, parent, std):
        QFrameBase.__init__(self, parent)

        self.samples = list(Sample.samples.values())
        self.std = Standard.standards[std]

        self.report_frame = QFrameMulSamples(self, self.std.name, [s.name for s in self.samples])
        self.layout().insertWidget(1, self.report_frame)

    def save_report(self):
        fname = dialog_save_report("Эталон {}. Группа образцов".format(self.std.name))
        if fname:
            Printer('doc', self.report_frame.report.get_report).print(fname)
