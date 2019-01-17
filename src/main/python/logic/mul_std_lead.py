from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import Qt

from science import FACTORS
from science.classes import Sample, Standard

from reports.std_mul import FactorSampleMulStandards, SampleMulStandards
from reports.std_mul import MulFactorSamplesStandard, MulSamplesStandard, MulSamplesMulStandards
from reports.utils import Printer

from logic import QFrameBase, dialog_save_report
from logic.utils import QFrameCheck, QFrameCombo, QFrameInfo, QFrameImage
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

        values = list(Sample.samples.keys())
        values.remove(Sample.group.name)
        self.frame_group = QFrameCheck(self, values)
        self.frame_group.signal_func = self.group_changed
        self.layout().insertWidget(0, self.frame_group)

        self.std = Standard.standards[std]

        self.report_frame = None

        self.group_changed(self.frame_group.get_turned())

    def group_changed(self, new_values):
        if self.report_frame is not None:
            self.layout_vertical.removeWidget(self.report_frame)
            self.report_frame.hide()
            self.report_frame = None

        self.report_frame = QFrameMulSamples(self, self.std.name, new_values)
        self.layout_vertical.insertWidget(1, self.report_frame)

    def save_report(self):
        fname = dialog_save_report("Группа образцов. Эталон {}".format(self.std.name))
        if fname:
            Printer('doc', self.report_frame.report.get_report).print(fname)


class QFrameMulStdMulSamples(QFrameBase, Ui_FrameMulOne):
    def __init__(self, parent):
        QFrameBase.__init__(self, parent, Ui_FrameMulOne)

        layout = self.layout()

        stds = list(Standard.standards.keys())
        samples = list(Sample.samples.keys())
        samples.remove(Sample.group.name)

        self.horizontalLayout = QHBoxLayout()

        self.frame_group_stds = QFrameCheck(self, stds)
        self.frame_group_stds.signal_func = self.group_stds_changed
        layout.insertWidget(0, self.frame_group_stds)

        self.std_frame_combo = QFrameCombo(self, stds)
        self.horizontalLayout.insertWidget(0, self.std_frame_combo, alignment=Qt.AlignCenter)
        self.std_frame_combo.signal_func = self.std_changed

        self.frame_group_samples = QFrameCheck(self, samples)
        self.frame_group_samples.signal_func = self.group_samples_changed
        layout.insertWidget(1, self.frame_group_samples)

        # Layout для боксов выбора
        self.layout_vertical.addLayout(self.horizontalLayout)

        self.report_frame = None

        self.update(stds, samples)

    def group_stds_changed(self, new_stds):
        self.update(new_stds, self.frame_group_samples.get_turned())

    def group_samples_changed(self, new_samples):
        self.update(self.frame_group_stds.get_turned(), new_samples)

    def update(self, new_stds, new_samples):
        self.std_frame_combo.update_values(new_stds)
        self.std_frame_combo.combo.setCurrentIndex(0)
        self.std_frame_combo.combo_changed()

    def std_changed(self, std):
        if self.report_frame is not None:
            self.layout_vertical.removeWidget(self.report_frame)
            self.report_frame.hide()
            self.report_frame = None

        self.report_frame = QFrameMulSamples(self, std, self.frame_group_samples.get_turned())
        self.layout_vertical.insertWidget(1, self.report_frame)

    def save_report(self):
        fname = dialog_save_report("Группа образцов Группа эталонов")
        if fname:
            samples = [Sample.samples[sample] for sample in self.frame_group_samples.get_turned()]
            stds = [Standard.standards[std] for std in self.frame_group_stds.get_turned()]
            report = MulSamplesMulStandards(samples, stds)
            Printer('doc', report.get_report).print(fname)


class QFrameMulStdSample(QFrameBase, Ui_FrameMulOne):
    class QFrameMulStds(QFrameBase):
        def __init__(self, parent):
            QFrameBase.__init__(self, parent, None)

    def __init__(self, parent, sample):
        QFrameBase.__init__(self, parent, Ui_FrameMulOne)

        values = list(Standard.standards.keys())

        self.frame_group = QFrameCheck(self, values)
        self.frame_group.signal_func = self.group_changed
        self.layout().insertWidget(0, self.frame_group)

        self.frame_combo = QFrameCombo(self, values)
        self.layout_vertical.insertWidget(0, self.frame_combo)
        self.frame_combo.signal_func = self.std_changed

        self.sample = Sample.samples[sample] if '--Групповой--' != sample else Sample.group
        self.report_frame = None

        self.group_changed(values)

    def group_changed(self, new_values):
        self.frame_combo.update_values(new_values)
        self.frame_combo.combo.setCurrentIndex(0)
        self.frame_combo.combo_changed()

    def std_changed(self, std):
        if self.report_frame is not None:
            self.layout_vertical.removeWidget(self.report_frame)
            self.report_frame.hide()
            self.report_frame = None
        self.report_frame = QFrameSample(self, std, self.sample.name)
        self.layout_vertical.insertWidget(1, self.report_frame)

    def save_report(self):
        idx = self.report_frame.tabs.currentIndex()
        if idx == 0:
            fname = dialog_save_report("Группа эталонов. Образец {}".format(self.sample.name))
            if fname:
                report = SampleMulStandards(self.sample, [Standard.standards[std]
                                                          for std in self.frame_group.get_turned()])
                Printer('doc', report.get_report).print(fname)
        else:
            fname = dialog_save_report("Группа эталонов. Образец {}".format(FACTORS[idx - 1], self.sample.name))
            if fname:
                report = FactorSampleMulStandards(self.sample, idx - 1,
                                                  [Standard.standards[std] for std in self.frame_group.get_turned()])
                Printer('doc', report.get_report).print(fname)
