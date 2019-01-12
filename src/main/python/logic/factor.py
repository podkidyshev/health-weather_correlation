from logic import QFrameBase, dialog_save
from frames.factor import Ui_FrameFactor

from science import print_report
from science.reports import FactorSampleStandard


class QFrameFactor(QFrameBase, Ui_FrameFactor):
    def __init__(self, parent, report: FactorSampleStandard):
        QFrameBase.__init__(self, parent, Ui_FrameFactor)
        self.report = report

        self.add_image(self.report.va, self.label, 'va_img')
        self.add_text(print_report('ui', self.report.get_report), self.text_edit)
