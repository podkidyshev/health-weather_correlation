from logic import QFrameBase, dialog_save
from logic.factor import QFrameFactor
from frames.sample import Ui_FramePatient

from science import Printer
from science.classes import Standard, Sample
from science.reports import FactorSampleStandard, SampleStandard
import science.test_normal as ntest


class QFrameSample(QFrameBase, Ui_FramePatient):
    def __init__(self, parent, sample_name, std_name, factor_name):
        QFrameBase.__init__(self, parent, Ui_FramePatient)

        self.std = Standard.standards[std_name]
        self.sample = Sample.samples[sample_name]

        self.report = SampleStandard(self.sample, self.std)

        self.title_label.setText("Образец {}".format(self.sample.name))

        self.reports = []
        self.frames = []
        for factor in range(4):
            self.reports.append(FactorSampleStandard(self.sample, factor, self.std))
            self.frames.append(QFrameFactor(self, self.reports[-1]))
            self.tabs.widget(1 + factor).layout().insertWidget(0, self.frames[-1])

        self.add_image(self.report.kde, self.label_kde, 'lable_kde_img')
        self.add_image(self.report.kde3, self.label_kde3, 'label_kde3_img')

        # Printer.launch('ui', self.text_main_1, ntest.get_report, self.report.ntest[0])

    def save_report(self):
        # fname = dialog_save(self, "Сохранить отчет")
        # doc = create_docx()
        # self.report.get_report(doc)
        # save_docx(doc, fname)
        print('NOT YET COMPLETED')
