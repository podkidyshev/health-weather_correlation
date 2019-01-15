from logic import QFrameBase, dialog_save
from logic.text import QFrameText
from logic.image import QFrameImage
from frames.frame_info import Ui_FrameInfo


class QFrameInfo(QFrameBase, Ui_FrameInfo):
    def __init__(self, parent, report, type: str = "val"):
        QFrameBase.__init__(self, parent, Ui_FrameInfo)
        self.report = report

        self.frames = [QFrameImage(self, self.report, type), QFrameText(self, self.report, type, 'stat'),
                       QFrameText(self, self.report, type, 'ntest')]

        for info in range(3):
            self.tabs.widget(info).layout().insertWidget(0, self.frames[info])

