from logic import QFrameBase, dialog_save_report
from logic.utils import QFrameInfo, QFrameInfoKde, QDialogGroupFactor

from frames.sample import Ui_FramePatient

from science import FACTORS_ALL
from science.classes import Standard, Sample

from reports import Printer
from reports.std import FactorSampleStandard, SampleStandard
from reports.std_mul import FactorSampleMulStandards, SampleMulStandards
from reports.std_mul import (MulSamplesStandard, MulFactorSamplesStandard,
                             MulSamplesMulStandards, MulFactorSamplesMulStandards)


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
        tab = self.tabs.currentIndex()
        factor = FACTORS_ALL if tab == 0 else tab - 1
        fname = dialog_save_report("{} Эталон {}".format(self.sample.display_file(factor), self.std.name))
        if not fname:
            return
        if factor == FACTORS_ALL:
            Printer('doc', self.report.get_report).print(fname)
        else:
            Printer('doc', self.reports[factor].get_report).print(fname)

    def save_report_group(self, stds: "лист строк"):
        tab = self.tabs.currentIndex()
        factor = FACTORS_ALL if tab == 0 else tab - 1
        fname = dialog_save_report("{} Группа эталонов".format(self.sample.display_file(factor)))
        stds = [Standard.standards[std] for std in stds]
        if not fname:
            return
        if factor == FACTORS_ALL:
            report = SampleMulStandards(self.sample, stds)
        else:
            report = FactorSampleMulStandards(self.sample, tab - 1, stds)
        Printer('doc', report.get_report).print(fname)


class QFrameStdMulSamples(QFrameBase, Ui_FramePatient):
    def __init__(self, parent, std):
        QFrameBase.__init__(self, parent, Ui_FramePatient)

        self.samples = list(Sample.samples.values())
        self.std = Standard.standards[std]

        self.report = MulSamplesStandard(self.samples, self.std)
        self.reports, self.frames = [], []

        self.tabs.removeTab(0)
        for factor in range(4):
            self.reports.append(MulFactorSamplesStandard(self.samples, factor, self.std))
            self.frames.append(QFrameInfo(self, self.reports[-1]))
            self.tabs.widget(factor).layout().insertWidget(0, self.frames[-1])

        self.title_label.setText("Эталон {} и группа образцов".format(self.std.name))

    def save_report(self):
        factor = QDialogGroupFactor.get_factor(self)
        if factor is None:
            return
        fname = dialog_save_report("{} {}".format(Sample.display_file_group(factor), self.std.display_file()))
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
        fname = dialog_save_report("{} Группа эталонов".format(Sample.display_file_group(factor)))
        if not fname:
            return
        stds = [Standard.standards[std] for std in stds]
        if factor == FACTORS_ALL:
            report = MulSamplesMulStandards(self.samples, stds)
        else:
            report = MulFactorSamplesMulStandards(self.samples, factor, stds)
        Printer('doc', report.get_report).print(fname)
