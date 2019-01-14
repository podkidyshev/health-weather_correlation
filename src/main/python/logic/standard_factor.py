from logic import QFrameBase, dialog_save
from frames.standard_factor import Ui_FrameStandardFactor

from science import print_report
from science.reports import StandardFactorSample


class QFrameStandardFactor(QFrameBase, Ui_FrameStandardFactor):
    def __init__(self, parent, report: StandardFactorSample):
        QFrameBase.__init__(self, parent, Ui_FrameStandardFactor)
        self.report = report

        self.add_image(self.report.va, self.label_1, 'va_img_1')
        self.add_image(self.report.va_apl, self.label_2, 'va_img_2')
        self.add_text(print_report('ui', self.report.get_report_stat), self.text_edit_1)
        self.add_text(print_report('ui', self.report.get_report_stat_apl), self.text_edit_2)