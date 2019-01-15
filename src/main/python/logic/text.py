from logic import QFrameBase, dialog_save
from frames.text import Ui_FrameText

from science import print_report


class QFrameText(QFrameBase, Ui_FrameText):
    def __init__(self, parent, report, type: str, func_name: str):
        QFrameBase.__init__(self, parent, Ui_FrameText)
        self.report = report
        self.type = type
        self.func_name = func_name

        self.add_text(print_report('ui', self.get_func()), self.text_edit)

    def get_func(self):
        if self.type == "val":
            return self.func()
        return self.func_apl()

    def func(self):
        if self.func_name == "stat":
            return self.report.get_report_stat
        else:
            return self.report.get_report_ntest

    def func_apl(self):
        if self.func_name == "stat":
            return self.report.get_report_stat_apl
        else:
            return self.report.get_report_ntest_apl