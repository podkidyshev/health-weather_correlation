from logic import QFrameBase, dialog_save
from frames.sample import Ui_FramePatient

from science import create_docx, save_docx
from science.classes import Standard, Sample
from science.reports import FactorSampleStandard, SampleStandard


class QFramePatient(QFrameBase, Ui_FramePatient):
    def __init__(self, parent, sample_name, std_name):
        QFrameBase.__init__(self, parent, Ui_FramePatient)

        self.std = Standard.standards[std_name]
        self.sample = Sample.samples[sample_name]
        self.report_factors = SampleStandard(self.sample, self.std)
        self.reports = [FactorSampleStandard(self.sample, factor, self.std) for factor in range(4)]

        self.add_image(self.report_factors.kde, self.factors_label, 'rfs_kde')
        for factor in range(4):
            self.add_image(self.reports[factor].va,
                           self.__dict__['label_{}'.format(factor)],
                           'rs_{}_va'.format(factor))

        # self.text_factor_0.setPlaceholderText('kek')
        self.std_pat_label.setText("Образец {}".format(self.sample.name))

    def save_report(self):
        # fname = dialog_save(self, "Сохранить отчет")
        # doc = create_docx()
        # self.report.get_report(doc)
        # save_docx(doc, fname)
        print('NOT YET COMPLETED')
