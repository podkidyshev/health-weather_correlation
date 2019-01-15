from logic import QFrameBase, dialog_save
from frames.image import Ui_FrameImage


class QFrameImage(QFrameBase, Ui_FrameImage):
    def __init__(self, parent, report, type):
        QFrameBase.__init__(self, parent, Ui_FrameImage)
        self.report = report
        self.type = type

        self.va, self.image_name = self.get_va()

        self.add_image(self.va, self.image, self.image_name)

    def get_va(self):
        if self.type == "val":
            return self.report.va, 'va_img1'
        return self.report.va_apl, 'va_img2'