# Ведущий ряд - эталон
from logic import QFrameBase, dialog_save_report
from logic.utils import QFrameInfo, QFrameInfoKde, QDialogStds

from frames.sample import Ui_FramePatient

from science import FACTORS_ALL
from science.classes import Standard, Sample

from reports import Printer
# Для QFrameStdSample
from reports.std import StandardFactorSample, StandardSample
from reports.std_mul import MulStandardsFactorSample, MulStandardsSample
# Для QFrameStdMulSamples
from reports.std_mul import StandardMulFactorSamples, StandardMulSamples
from reports.std_mul import MulStandardsMulFactorSamples, MulStandardsMulSamples


class QFrameStdSample(QFrameBase, Ui_FramePatient):
    def __init__(self, parent, std_name, sample_name):
        QFrameBase.__init__(self, parent, Ui_FramePatient)

        self.std = Standard.standards[std_name]
        self.sample = Sample.samples[sample_name] if sample_name != "--Групповой--" else Sample.group

        self.report = StandardSample(self.std, self.sample)

        self.title_label.setText("{}".format(self.report.sample_name))

        self.reports = []
        self.frames = []
        for factor in range(4):
            self.reports.append(StandardFactorSample(self.std, self.sample, factor))
            self.frames.append(QFrameInfo(self, self.reports[-1]))
            self.tabs.widget(1 + factor).layout().insertWidget(0, self.frames[-1])

        self.tabs.widget(0).layout().insertWidget(0, QFrameInfoKde(self, self.report, "kde"))

    def dialog_std_sample(self, factor):
        fname = dialog_save_report("Эталон {} {}".format(self.std.name, self.sample.display_file(factor)))
        if not fname:
            return
        if factor == FACTORS_ALL:
            Printer('doc', self.report.get_report).print(fname)
        else:
            Printer('doc', self.reports[factor].get_report).print(fname)

    def save_report(self):
        factor = QDialogStds.settings(self, get_stds=False)
        if factor is None:
            return
        self.dialog_std_sample(factor)

    def save_report_group(self):
        factor, stds = QDialogStds.settings(self, get_stds=True, std_main=self.std.name)
        if factor is None:
            return
        if not len(stds):
            return
        if len(stds) == 1:
            self.dialog_std_sample(factor)
        else:
            fname = dialog_save_report("Группа эталонов {}".format(self.sample.display_file(factor)))
            stds = [Standard.standards[std] for std in stds]
            if not fname:
                return
            if factor == FACTORS_ALL:
                report = MulStandardsSample(stds, self.sample)
            else:
                report = MulStandardsFactorSample(stds, self.sample, factor)
            Printer('doc', report.get_report).print(fname)


class QFrameStdMulSamples(QFrameBase, Ui_FramePatient):
    def __init__(self, parent, std):
        QFrameBase.__init__(self, parent, Ui_FramePatient)

        self.std = Standard.standards[std]
        self.samples = list(Sample.samples.values())

        self.report = StandardMulSamples(self.std, self.samples)

        self.title_label.setText("Эталон {} и группа образцов".format(self.std.name))

        self.reports, self.frames = [], []
        self.tabs.removeTab(0)
        for factor in range(4):
            self.reports.append(StandardMulFactorSamples(self.std, self.samples, factor))
            self.frames.append(QFrameInfo(self, self.reports[-1]))
            self.tabs.widget(factor).layout().insertWidget(0, self.frames[-1])

    def dialog_std_samples(self, factor):
        fname = dialog_save_report("Эталон {} {}".format(self.std.name, Sample.display_file_group(factor)))
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
        self.dialog_std_samples(factor)

    def save_report_group(self):
        factor, stds = QDialogStds.settings(self, get_stds=True, std_main=self.std.name)
        if factor is None:
            return
        if not len(stds):
            return
        if len(stds) == 1:
            self.dialog_std_samples(factor)
        else:
            fname = dialog_save_report("Группа эталонов {}".format(Sample.display_file_group(factor)))
            if not fname:
                return
            stds = [Standard.standards[std] for std in stds]
            if factor == FACTORS_ALL:
                report = MulStandardsMulSamples(stds, self.samples)
            else:
                report = MulStandardsMulFactorSamples(stds, self.samples, factor)
            Printer('doc', report.get_report).print(fname)
