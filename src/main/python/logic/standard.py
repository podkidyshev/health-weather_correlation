from logic import QFrameBase, dialog_save_report
from logic.utils import QFrameStandardType, QDialogGroupFactor

from frames.standard import Ui_FrameStandard

from science import FACTORS_ALL
from science.classes import Standard, Sample

from reports import Printer
from reports.sample import StandardFactorSample, StandardSample
from reports.sample_mul import MulStandardsSample
from reports.sample_mul import StandardMulSamples, StandardMulFactorSamples, MulStandardsMulSamples


class QFrameStandard(QFrameBase, Ui_FrameStandard):
    def __init__(self, parent, sample_name, std_name):
        QFrameBase.__init__(self, parent, Ui_FrameStandard)

        self.std = Standard.standards[std_name]
        self.sample = Sample.samples[sample_name] if sample_name != "--Групповой--" else Sample.group

        self.report = StandardSample(self.std, self.sample)

        self.title_label.setText("Погода {}".format(std_name))

        self.reports = []
        self.frames = []
        for factor in range(4):
            self.reports.append(StandardFactorSample(self.std, factor, self.sample))
            self.frames.append(QFrameStandardType(self, self.reports[-1]))
            self.tabs.widget(factor).layout().insertWidget(0, self.frames[-1])

    def save_report(self):
        factor = QDialogGroupFactor.get_factor(self)
        if factor is None:
            return
        fname = dialog_save_report("{} {}".format(self.std.display_file(), self.sample.display_file(factor)))
        if not fname:
            return
        if factor == FACTORS_ALL:
            Printer("doc", self.report.get_report).print(fname)
        else:
            Printer("doc", self.reports[factor].get_report).print(fname)

    def save_report_group(self, stds: "лист строк"):
        factor = QDialogGroupFactor.get_factor(self)
        if factor is None:
            return
        fname = dialog_save_report("Группа эталонов {}".format(self.sample.display_file(factor)))
        if not fname:
            return
        stds = [Standard.standards[std] for std in stds]
        if factor == FACTORS_ALL:
            report = MulStandardsSample(stds, self.sample)
        else:
            return
            # TODO: сделать отчет
            # report = MulStandardsFactorSample
        Printer("doc", report.get_report).print(fname)


# TODO: пока не понятно нужен этот фрейм или нет
class QFrameMulSamplesStd(QFrameBase):
    def __init__(self, parent, std):
        QFrameBase.__init__(self, parent)

        self.samples = list(Sample.samples.values())
        self.std = Standard.standards[std]

        self.report = StandardMulSamples(self.std, self.samples)
        self.reports, self.frames = [], []

        for factor in range(4):
            self.reports.append(StandardMulFactorSamples(self.std, self.samples, factor))
            self.frames.append(QFrameStandardType(self, self.reports[-1]))
            self.tabs.widget(factor).layout().insertWidget(0, self.frames[-1])

        self.title_label.setText("Группа образцов и эталон {}".format(self.std.name))

    def save_report(self):
        factor = QDialogGroupFactor.get_factor(self)
        if factor is None:
            return
        fname = dialog_save_report("{} {}".format(self.std.display_file(), Sample.display_file_group(factor)))
        if not fname:
            return
        if factor == FACTORS_ALL:
            Printer("doc", self.report.get_report).print(fname)
        else:
            Printer("doc", self.reports[factor].get_report).print(fname)

    def save_report_group(self, stds: "лист строк"):
        factor = QDialogGroupFactor.get_factor(self)
        if factor is None:
            return
        fname = dialog_save_report("Группа эталонов {}".format(Sample.display_file_group(factor)))
        if not fname:
            return
        stds = [Standard.standards[std] for std in stds]
        if factor == FACTORS_ALL:
            report = MulStandardsMulSamples(stds, self.samples)
        else:
            return
            # TODO: сделать отчет
            # report = MulStandardsMulFactorSamples
        Printer("doc", report.get_report).print(fname)
