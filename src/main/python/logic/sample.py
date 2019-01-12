from logic import QFrameBase, dialog_save
from frames.sample import Ui_FramePatient

from science import Printer
from science.classes import Standard, Sample
from science.reports import FactorSampleStandard, SampleStandard
from science.test_normal import get_report


class QFrameSample(QFrameBase, Ui_FramePatient):
    def __init__(self, parent, sample_name, std_name):
        QFrameBase.__init__(self, parent, Ui_FramePatient)

        self.std = Standard.standards[std_name]
        self.sample = Sample.samples[sample_name]
        self.report = SampleStandard(self.sample, self.std)
        self.reports = [FactorSampleStandard(self.sample, factor, self.std) for factor in range(4)]

        self.add_image(self.report.kde, self.label_kde, 'lable_kde_img')
        self.add_image(self.report.kde3, self.label_kde3, 'label_kde3_img')

        printer = Printer('ui')
        get_report(self.report.ntest[0], printer)
        self.text_main_1.setFontPointSize(16)
        self.text_main_1.setFixedHeight(300)
        self.text_main_1.insertPlainText(printer.print())
        # print(self.text_main_1.document().size())
        # self.text_main_1.insertPlainText('lolx2\n')

        for factor in range(4):
            self.add_image(self.reports[factor].va,
                           self.__dict__['label_{}'.format(factor)],
                           'rs_{}_va'.format(factor))

        self.title_label.setText("Образец {}".format(self.sample.name))

    def save_report(self):
        # fname = dialog_save(self, "Сохранить отчет")
        # doc = create_docx()
        # self.report.get_report(doc)
        # save_docx(doc, fname)
        print('NOT YET COMPLETED')
