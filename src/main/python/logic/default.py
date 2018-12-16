from logic import BaseFrame
from frames.default import Ui_FrameDefault


class QDefaultFrame(BaseFrame, Ui_FrameDefault):
    def __init__(self, parent):
        BaseFrame.__init__(self, parent, Ui_FrameDefault)
