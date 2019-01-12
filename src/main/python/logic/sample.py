from logic import QFrameBase, dialog_save
from frames.sample import Ui_FramePatient

from science import create_docx, save_docx, FACTORS
from science.classes import Standard, Sample
from science.reports import FactorSampleStandard, SampleStandard


class QFrameSample(QFrameBase, Ui_FramePatient):
    def __init__(self, parent, sample_name, std_name, factor_name):
        QFrameBase.__init__(self, parent, Ui_FramePatient)

        self.std = Standard.standards[std_name]
        self.sample = Sample.samples[sample_name]
        self.factor = FACTORS.index(factor_name) if factor_name in FACTORS else -1

        if self.factor == -1:
            # выбран образец
            case = 2
            if case == 2:
                # выбран один эталон (случай 2)
                # TODO: групповой фактор-образец, уточнить

                self.report_factors = SampleStandard(self.sample, self.std)
                self.reports = [FactorSampleStandard(self.sample, factor, self.std) for factor in range(4)]

                # строится только KDE для всех факторов
                self.add_image(self.report_factors.kde, self.factors_label, 'rfs_kde')

                # TODO: во вкладки картинки раскидать
                # for factor in range(4):
                #     self.add_image(self.reports[factor].va,
                #                    self.__dict__['label_{}'.format(factor)],
                #                    'rs_{}_va'.format(factor))

                text = self.merge_text(std_name)
                self.textEdit.setText(text)
            else:
                # TODO: группа эталонов, уточнить
                pass
            self.title_label.setText("Образец: {}".format(self.sample.name))
        else:
            # выбран фактор-образец
            case = 1
            if case == 1:
                # выбран фактор-образец (индивидуальный) (случай 1)
                # TODO: групповой фактор-образец, уточнить

                self.reports = FactorSampleStandard(self.sample, self.factor, self.std)

                # гистограмма и ядерная оценка (вроде) добавляется, про кривую Гаусса не понял
                self.add_image(self.reports.va, self.factors_label, 'rfs_kde')

                text = self.merge_text(std_name)
                self.textEdit.setText(text)
            else:
                # TODO: группа эталонов, уточнить (случай 4)
                pass
                self.title_label.setText("Образец: {}   Фактор: {}".format(self.sample.name, FACTORS[self.factor]))
                # self.textEdit.setText('Лол Кек Чебурек')

    def merge_text(self, std_name):
        text = ""
        if type(self.reports) is list:
            for factor in range(4):
                text += self.create_text(factor, std_name) + '\n'
        else:
            text += self.create_text(self.factor, std_name)
        return text

    def create_text(self, factor, std_name):
        if type(self.reports) is list:
            distance, ntest, stat_mean, stat_std, stat_interval = self.reports[factor].distance, self.reports[
                factor].ntest, self.reports[factor].stat_mean, self.reports[factor].stat_std, self.reports[
                                                                      factor].stat_interval
        else:
            distance, ntest, stat_mean, stat_std, stat_interval = self.reports.distance, self.reports.ntest, \
                                                                  self.reports.stat_mean, self.reports.stat_std, self.reports.stat_interval
        text = "Последовательность расстояний для фактор-образца {} (Фактор: {}) и эталона {}: {}\n".format(
            self.sample.name, FACTORS[factor], std_name, str(distance))
        # TODO: тест нормальности осознать
        # text += "Результаты тестирования нормальности распределения расстояний фактор-образца {} (Фактор: {}) для эталона {}: {}\n".format(
        #     self.sample.name, FACTORS[factor], std_name, ntest)
        text += "Результат статистического анализа распределения расстояний фактор-образца {} (Фактор: {}) для эталона {}\n".format(
            self.sample.name, FACTORS[factor], std_name)
        text += "Выборочное среднее: {}\nСтандартное отклонение: {}\nДоверительный интервал: {}\n".format(
            str(stat_mean), str(stat_std),
            str(stat_interval))
        return text

    def save_report(self):
        # fname = dialog_save(self, "Сохранить отчет")
        # doc = create_docx()
        # self.report.get_report(doc)
        # save_docx(doc, fname)
        print('NOT YET COMPLETED')
