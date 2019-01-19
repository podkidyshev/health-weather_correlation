from science.classes import Sample, Standard

from reports.sample_mul import MulStandardsSample, StandardMulSamples, StandardMulFactorSamples, MulStandardsMulSamples
from reports.utils import Printer

from logic import QFrameBase, dialog_save_report
from logic.utils import QFrameCheck, QFrameCombo, QFrameStandardType
from logic.standard import QFrameStandard

from frames.standard import Ui_FrameStandard
from frames.mul_one import Ui_FrameMulOne


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


class QFrameSampleMulStd(QFrameBase, Ui_FrameMulOne):
    def __init__(self, parent, sample):
        QFrameBase.__init__(self, parent, Ui_FrameMulOne)

        values = list(Standard.standards.keys())

        self.frame_group = QFrameCheck(self, values)
        self.frame_group.signal_func = self.group_changed
        self.layout().insertWidget(0, self.frame_group)

        self.frame_combo = QFrameCombo(self, values)
        self.layout_vertical.insertWidget(0, self.frame_combo)
        self.frame_combo.signal_func = self.sample_changed

        self.sample = Sample.samples[sample] if sample != "--Групповой--" else Sample.group
        self.report = None
        self.report_frame = None

        self.group_changed(self.frame_group.get_turned())

    def group_changed(self, new_values):
        self.frame_combo.update_values(new_values)
        self.frame_combo.combo.setCurrentIndex(0)
        self.frame_combo.combo_changed()

    def sample_changed(self, std):
        if self.report_frame is not None:
            self.layout_vertical.removeWidget(self.report_frame)
            self.report_frame.hide()
            self.report_frame = None
        self.report_frame = QFrameStandard(self, self.sample.name, std)
        self.layout_vertical.insertWidget(1, self.report_frame)

    def save_report(self):
        fname = dialog_save_report("Группа эталонов. Образец {}".format(self.sample.name))
        if fname:
            report = MulStandardsSample([Standard.standards[std]
                                                      for std in self.frame_group.get_turned()], self.sample)
            Printer('doc', report.get_report).print(fname)


class QFrameMulSamplesStd(QFrameBase, Ui_FrameMulOne):
    class QFrameMulStds(QFrameBase):
        def __init__(self, parent):
            QFrameBase.__init__(self, parent, None)

    def __init__(self, parent, std):
        QFrameBase.__init__(self, parent, Ui_FrameMulOne)

        values = list(Sample.samples.keys())
        values.remove(Sample.group.name)

        self.frame_group = QFrameCheck(self, values)
        self.frame_group.signal_func = self.group_changed
        self.layout().insertWidget(0, self.frame_group)

        self.std = Standard.standards[std]
        self.report = None
        self.report_frame = None

        self.group_changed(self.frame_group.get_turned())

    def group_changed(self, new_samples):
        if self.report_frame is not None:
            self.layout_vertical.removeWidget(self.report_frame)
            self.report_frame.hide()
            self.report_frame = None
        self.report_frame = QFrameMulSamples(self, self.std.name, new_samples)
        self.layout_vertical.insertWidget(1, self.report_frame)

    def save_report(self):
        fname = dialog_save_report("Эталон {}. Группа образцов".format(self.std.name))
        if fname:
            Printer('doc', self.report_frame.report.get_report).print(fname)


class QFrameMulSamplesMulStd(QFrameBase, Ui_FrameMulOne):
    def __init__(self, parent):
        QFrameBase.__init__(self, parent, Ui_FrameMulOne)

        layout = self.layout()

        samples = list(Sample.samples.keys())
        samples.remove(Sample.group.name)
        stds = list(Standard.standards.keys())

        self.frame_group_samples = QFrameCheck(self, samples)
        self.frame_group_samples.signal_func = self.group_samples_changed
        layout.insertWidget(0, self.frame_group_samples)

        self.frame_group_stds = QFrameCheck(self, stds)
        self.frame_group_stds.signal_func = self.group_stds_changed
        layout.insertWidget(1, self.frame_group_stds)

        self.std_frame_combo = QFrameCombo(self, stds)
        self.layout_vertical.insertWidget(0, self.std_frame_combo)
        self.std_frame_combo.signal_func = self.std_changed

        self.report_frame = None

        self.update(samples, stds)

    def group_samples_changed(self, new_samples):
        self.update(new_samples, self.frame_group_stds.get_turned())

    def group_stds_changed(self, new_stds):
        self.update(self.frame_group_samples.get_turned(), new_stds)

    def update(self, new_samples, new_stds):
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
        fname = dialog_save_report("Группа эталонов. Группа образцов")
        if fname:
            stds = [Standard.standards[std] for std in self.frame_group_stds.get_turned()]
            samples = [Sample.samples[sample] for sample in self.frame_group_samples.get_turned()]
            report = MulStandardsMulSamples(stds, samples)
            Printer('doc', report.get_report).print(fname)