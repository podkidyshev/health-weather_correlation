import logic
from logic import QFrameBase, dialog_save
from frames.factor import Ui_FrameFactor

from science import print_report
from science.reports import FactorSampleStandard
from science.test_normal import get_report


class QFrameFactor(QFrameBase, Ui_FrameFactor):
    def __init__(self, parent, report: FactorSampleStandard):
        QFrameBase.__init__(self, parent, Ui_FrameFactor)
        self.report = report

        self.add_image(self.report.va, self.label, 'va_img')
        self.add_text(print_report('ui', get_report, self.report.ntest), self.text_edit)
