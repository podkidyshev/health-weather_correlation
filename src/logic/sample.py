# Ведущий ряд - образец
from logic import QFrameBase, dialog_save_report
from logic.utils import QFrameStandardType, QDialogStds

from frames.standard import Ui_FrameStandard

from science import FACTORS_ALL
from science.classes import Standard, Sample

from reports import Printer
# Для QFrameSampleStd
from reports.sample import FactorSampleStandard, SampleStandard
from reports.sample_mul import FactorSampleMulStandards, SampleMulStandards
# Для QFrameMulSamplesStd
from reports.sample_mul import MulFactorSamplesStandard, MulSamplesStandard
from reports.sample_mul import MulFactorSamplesMulStandards, MulSamplesMulStandards


class QFrameSampleStd(QFrameBase, Ui_FrameStandard):
    def __init__(self, parent, sample_name, std_name):
        QFrameBase.__init__(self, parent, Ui_FrameStandard)

        self.sample = Sample.samples[sample_name] if sample_name != "--Групповой--" else Sample.group
        self.std = Standard.standards[std_name]

        self.report = SampleStandard(self.sample, self.std)

        self.title_label.setText("Погода {}".format(std_name))

        self.reports, self.frames = [], []
        for factor in range(4):
            self.reports.append(FactorSampleStandard(self.sample, factor, self.std))
            self.frames.append(QFrameStandardType(self, self.reports[-1]))
            self.tabs.widget(factor).layout().insertWidget(0, self.frames[-1])

    def dialog_sample_std(self, factor):
        fname = dialog_save_report("{} {}".format(self.sample.display_file(factor), self.std.display_file()))
        if not fname:
            return
        if factor == FACTORS_ALL:
            Printer("doc", self.report.get_report).print(fname)
        else:
            Printer("doc", self.reports[factor].get_report).print(fname)

    def save_report(self):
        factor = QDialogStds.settings(self, get_stds=False)
        if factor is None:
            return
        self.dialog_sample_std(factor)

    def save_report_group(self):
        factor, stds = QDialogStds.settings(self, get_stds=True, std_main=self.std.name)
        if factor is None:
            return
        if not len(stds):
            return
        if len(stds) == 1:
            self.dialog_sample_std(factor)
        else:
            fname = dialog_save_report("{} Группа эталонов".format(self.sample.display_file(factor)))
            if not fname:
                return
            stds = [Standard.standards[std] for std in stds]
            if factor == FACTORS_ALL:
                report = SampleMulStandards(self.sample, stds)
            else:
                report = FactorSampleMulStandards(self.sample, factor, stds)
            Printer("doc", report.get_report).print(fname)


# TODO: пока не понятно нужен этот фрейм или нет
class QFrameMulSamplesStd(QFrameBase):
    def __init__(self, parent, std):
        QFrameBase.__init__(self, parent)

        self.samples = list(Sample.samples.values())
        self.std = Standard.standards[std]

        self.report = MulSamplesStandard(self.samples, self.std)

        self.title_label.setText("Группа образцов и эталон {}".format(self.std.name))

        self.reports, self.frames = [], []
        for factor in range(4):
            self.reports.append(MulFactorSamplesStandard(self.samples, factor, self.std))
            self.frames.append(QFrameStandardType(self, self.reports[-1]))
            self.tabs.widget(factor).layout().insertWidget(0, self.frames[-1])

    def save_report(self):
        factor = QDialogStds.settings(self, get_stds=False)
        if factor is None:
            return
        fname = dialog_save_report("{} {}".format(Sample.display_file_group(factor), self.std.display_file()))
        if not fname:
            return
        if factor == FACTORS_ALL:
            Printer("doc", self.report.get_report).print(fname)
        else:
            Printer("doc", self.reports[factor].get_report).print(fname)

    def save_report_group(self):
        factor, stds = QDialogStds.settings(self, get_stds=True, std_main=self.std.name)
        if factor is None:
            return
        fname = dialog_save_report("{} Группа эталонов".format(Sample.display_file_group(factor)))
        if not fname:
            return
        stds = [Standard.standards[std] for std in stds]
        if factor == FACTORS_ALL:
            report = MulSamplesMulStandards(self.samples, stds)
        else:
            report = MulFactorSamplesMulStandards(self.samples, factor, stds)
        Printer("doc", report.get_report).print(fname)
