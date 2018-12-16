from logic import QFrameBase
from frames.default import Ui_FrameDefault


class QFrameDefault(QFrameBase, Ui_FrameDefault):
    def __init__(self, parent):
        QFrameBase.__init__(self, parent, Ui_FrameDefault)
