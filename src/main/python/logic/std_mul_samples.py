from science.classes import Sample, Standard
from science.reports import MulSamplesStandard

from logic import QFrameBase
from frames.std_mul_samples import Ui_FrameStdMulSamples
from logic.group import QFrameGroup


class QFrameStdMulSamples(QFrameBase, Ui_FrameStdMulSamples):
    def __init__(self, parent, std):
        QFrameBase.__init__(self, parent, Ui_FrameStdMulSamples)

        layout = self.layout()

        values = list(Sample.samples.keys())
        values.remove('group')
        self.frame_group = QFrameGroup(self, values)
        self.frame_group.signal_func = self.group_changed
        layout.insertWidget(0, self.frame_group)

        self.std = Standard.standards[std]
        self.report = None

        self.group_changed(self.frame_group.get_turned())

    def group_changed(self, new_values):
        self.report = MulSamplesStandard([Sample.samples[name] for name in new_values], self.std)
        self.title_label.setText("Эталон: {}. {} значений".format(self.std.name, len(new_values)))
