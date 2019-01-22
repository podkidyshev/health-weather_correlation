from logic import QFrameBase, dialog_save_report
from logic.utils import QFrameInfo, QFrameInfoKde

from frames.sample import Ui_FramePatient

from science.classes import Standard, Sample

from reports import Printer
from reports.std import StandardFactorSample, StandardSample
from reports.std_mul import MulStandardsFactorSample, MulStandardsSample
from reports.std_mul import StandardMulSamples, StandardMulFactorSamples, MulStandardsMulSamples


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

    def save_report(self):
        tab = self.tabs.currentIndex()
        factor = None if tab == 0 else tab - 1
        fname = dialog_save_report("{} Эталон {}".format(self.sample.display_file(factor), self.std.name))
        if not fname:
            return
        if factor is None:
            Printer('doc', self.report.get_report).print(fname)
        else:
            Printer('doc', self.reports[factor].get_report).print(fname)

    def save_report_group(self, stds: "лист строк"):
        tab = self.tabs.currentIndex()
        factor = None if tab == 0 else tab - 1
        fname = dialog_save_report("{} Группа эталонов".format(self.sample.display_file(factor)))
        stds = [Standard.standards[std] for std in stds]
        if not fname:
            return
        if factor is None:
            report = MulStandardsSample(stds, self.sample)
        else:
            report = MulStandardsFactorSample(stds, self.sample, tab - 1)
        Printer('doc', report.get_report).print(fname)


class QFrameStdMulSamples(QFrameBase, Ui_FramePatient):
    def __init__(self, parent, std):
        QFrameBase.__init__(self, parent, Ui_FramePatient)

        self.std = Standard.standards[std]
        self.samples = list(Sample.samples.values())

        self.report = StandardMulSamples(self.std, self.samples)
        self.reports, self.frames = [], []

        self.tabs.removeTab(0)
        for factor in range(4):
            self.reports.append(StandardMulFactorSamples(self.std, self.samples, factor))
            self.frames.append(QFrameInfo(self, self.reports[-1]))
            self.tabs.widget(factor).layout().insertWidget(0, self.frames[-1])

        self.title_label.setText("Группа образцов и эталон {}".format(self.std.name))

    def save_report(self):
        fname = dialog_save_report("Группа образцов Эталон {}".format(self.std.name))
        if fname:
            Printer('doc', self.report_frame.report.get_report).print(fname)

# TODO: реализовать сохранение отчета по факторам
    def save_report_group(self, stds: "лист строк"):
        fname = dialog_save_report("Группа образцов Группа эталонов")
        if not fname:
            return
        stds = [Standard.standards[std] for std in stds]
        report = MulStandardsMulSamples(stds, self.samples)
        Printer('doc', report.get_report).print(fname)
