from PyQt5.QtWidgets import QListWidget

from science.classes import Sample, Standard
from science.reports import MulSamplesStandard, MulSamplesMulStandards, SampleMulStandards, SampleStandard

from logic import QFrameBase, QFrameCheck, QFrameCombo
from logic.sample import QFrameSample
from frames.mul_one import Ui_FrameMulOne
from frames.mul_both import Ui_FrameMulBoth


class QFrameStdMulSamples(QFrameBase, Ui_FrameMulOne):
    def __init__(self, parent, std):
        QFrameBase.__init__(self, parent, Ui_FrameMulOne)

        values = list(Sample.samples.keys())
        values.remove(Sample.group.name)
        self.frame_group = QFrameCheck(self, values)
        self.frame_group.signal_func = self.group_changed
        self.layout().insertWidget(0, self.frame_group)

        self.std = Standard.standards[std]
        self.report = None

        self.group_changed(self.frame_group.get_turned())

    def group_changed(self, new_values):
        self.report = MulSamplesStandard([Sample.samples[name] for name in new_values], self.std)
        self.title_label.setText("Эталон: {}. {} значений".format(self.std.name, len(new_values)))


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
        self.report = None
        self.report_frame = None

        self.group_changed(values)

    def group_changed(self, new_values):
        # self.report = SampleMulStandards(self.sample, [Standard.standards[std] for std in new_values])
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


class QFrameMulStdMulSamples(QFrameBase, Ui_FrameMulBoth):
    def __init__(self, parent):
        QFrameBase.__init__(self, parent, Ui_FrameMulBoth)

        layout = self.layout()

        stds = list(Standard.standards.keys())
        samples = list(Sample.samples.keys())
        samples.remove(Sample.group.name)

        self.frame_group_stds = QFrameCheck(self, stds)
        self.frame_group_stds.signal_func = self.group_stds_changed
        layout.insertWidget(0, self.frame_group_stds)

        self.frame_group_samples = QFrameCheck(self, samples)
        self.frame_group_samples.signal_func = self.group_samples_chanhed
        layout.insertWidget(1, self.frame_group_samples)

        self.report = None
        self.update(stds, samples)

    def group_stds_changed(self, new_stds):
        self.update(new_stds, self.frame_group_samples.get_turned())

    def group_samples_chanhed(self, new_samples):
        self.update(self.frame_group_stds.get_turned(), new_samples)

    def update(self, new_stds, new_samples):
        self.title_label.setText("{} эталонов, {} образцов".format(len(new_stds), len(new_samples)))
        # self.report = MulSamplesMulStandards([Sample.samples[sample_name] for sample_name in new_samples],
        #                                      [Standard.standards[std_name] for std_name in new_stds])
