from science.classes import Sample, Standard

from logic import QFrameBase
from logic.utils import QFrameCheck, QFrameCombo
from logic.standard import QFrameStandard

from frames.mul_one import Ui_FrameMulOne
from frames.mul_both import Ui_FrameMulBoth


class QFrameSampleMulStd(QFrameBase, Ui_FrameMulOne):
    def __init__(self, parent, sample):
        QFrameBase.__init__(self, parent, Ui_FrameMulOne)

        values = list(Standard.standards.keys())
        self.frame_group = QFrameCheck(self, values)
        self.frame_group.signal_func = self.group_changed
        self.layout().insertWidget(0, self.frame_group)

        self.sample = Sample.samples[sample] if sample != "--Групповой--" else Sample.group
        self.report = None

        self.group_changed(self.frame_group.get_turned())

    def group_changed(self, new_values):
        # self.report = MulSamplesStandard([Sample.samples[name] for name in new_values], self.std)
        # self.title_label.setText("Эталон: {}. {} значений".format(self.std.name, len(new_values)))
        pass


class QFrameMulSampleStd(QFrameBase, Ui_FrameMulOne):
    class QFrameMulStds(QFrameBase):
        def __init__(self, parent):
            QFrameBase.__init__(self, parent, None)

    def __init__(self, parent, std):
        QFrameBase.__init__(self, parent, Ui_FrameMulOne)

        values = list(Sample.samples.keys())
        # Преобразовать имя групповго образца из group в --Групповой--
        values.remove(Sample.group.name)
        self.frame_group = QFrameCheck(self, values)
        self.frame_group.signal_func = self.group_changed
        self.layout().insertWidget(0, self.frame_group)

        self.frame_combo = QFrameCombo(self, values)
        self.layout_vertical.insertWidget(0, self.frame_combo)
        self.frame_combo.signal_func = self.sample_changed

        self.std = Standard.standards[std]
        self.report = None
        self.report_frame = None

        self.group_changed(values)

    def group_changed(self, new_values):
        # self.report = SampleMulStandards(self.sample, [Standard.standards[std] for std in new_values])
        self.frame_combo.update_values(new_values)
        self.frame_combo.combo.setCurrentIndex(0)
        self.frame_combo.combo_changed()

    def sample_changed(self, sample):
        if self.report_frame is not None:
            self.layout_vertical.removeWidget(self.report_frame)
            self.report_frame.hide()
            self.report_frame = None
        self.report_frame = QFrameStandard(self, sample, self.std.name)
        self.layout_vertical.insertWidget(1, self.report_frame)