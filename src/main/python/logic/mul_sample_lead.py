from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import Qt

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


class QFrameMulSamplesStd(QFrameBase, Ui_FrameMulOne):
    class QFrameMulStds(QFrameBase):
        def __init__(self, parent):
            QFrameBase.__init__(self, parent, None)

    def __init__(self, parent, std):
        QFrameBase.__init__(self, parent, Ui_FrameMulOne)

        values = list(Sample.samples.keys())
        # Преобразовать имя группового образца из group в --Групповой--
        values.remove(Sample.group.name)
        values.append("--Групповой--")

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


class QFrameMulSamplesMulStd(QFrameBase, Ui_FrameMulOne):
    def __init__(self, parent):
        QFrameBase.__init__(self, parent, Ui_FrameMulOne)

        layout = self.layout()

        samples = list(Sample.samples.keys())
        # Преобразовать имя групповго образца из group в --Групповой--
        samples.remove(Sample.group.name)
        samples.append("--Групповой--")
        stds = list(Standard.standards.keys())

        self.horizontalLayout = QHBoxLayout()

        self.frame_group_samples = QFrameCheck(self, samples)
        self.frame_group_samples.signal_func = self.group_samples_changed
        layout.insertWidget(0, self.frame_group_samples)

        self.sample_frame_combo = QFrameCombo(self, samples)
        self.horizontalLayout.insertWidget(0, self.sample_frame_combo, alignment=Qt.AlignCenter)
        self.sample_frame_combo.signal_func = self.sample_changed

        self.frame_group_stds = QFrameCheck(self, stds)
        self.frame_group_stds.signal_func = self.group_stds_changed
        layout.insertWidget(1, self.frame_group_stds)

        self.std_frame_combo = QFrameCombo(self, stds)
        self.horizontalLayout.insertWidget(1, self.std_frame_combo, alignment=Qt.AlignCenter)
        self.std_frame_combo.signal_func = self.std_changed

        # Layout для боксов выбора
        self.layout_vertical.addLayout(self.horizontalLayout)

        # Для начальной инициализации, не знаю правильно/нет
        self.std = Standard.standards['BX_60']
        self.sample = Sample.samples['1_1']
        self.report = None
        self.report_frame = None

        self.update(samples, stds)

    def group_samples_changed(self, new_samples):
        self.update(self.frame_group_stds.get_turned(), new_samples)

    def group_stds_changed(self, new_stds):
        self.update(new_stds, self.frame_group_samples.get_turned())

    def update(self, new_samples, new_stds):
        self.sample_frame_combo.update_values(new_samples)
        self.sample_frame_combo.combo.setCurrentIndex(0)
        self.sample_frame_combo.combo_changed()

        self.std_frame_combo.update_values(new_stds)
        self.std_frame_combo.combo.setCurrentIndex(0)
        self.std_frame_combo.combo_changed()
        # self.report = MulSamplesMulStandards([Sample.samples[sample_name] for sample_name in new_samples],
        #                                      [Standard.standards[std_name] for std_name in new_stds])

    def sample_changed(self, sample):
        if self.report_frame is not None:
            self.layout_vertical.removeWidget(self.report_frame)
            self.report_frame.hide()
            self.report_frame = None
        self.report_frame = QFrameStandard(self, sample, self.std.name)
        self.layout_vertical.insertWidget(1, self.report_frame)

    def std_changed(self, std):
        if self.report_frame is not None:
            self.layout_vertical.removeWidget(self.report_frame)
            self.report_frame.hide()
            self.report_frame = None
        self.report_frame = QFrameStandard(self, self.sample.name, std)
        self.layout_vertical.insertWidget(1, self.report_frame)