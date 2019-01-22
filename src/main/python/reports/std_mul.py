from science import plot_image, FACTORS_L
from science.funcs import *
from science.classes import Standard, Sample

from reports import Printer, str_arr
from reports.utils import report_ntest, report_stats


class MulStandardsFactorSample:
    def __init__(self, stds: list, sample: Sample, factor: int):
        self.stds = stds[:]
        self.sample = sample
        self.sample_name = sample.display()
        self.factor = factor

        self.distance = [sequence_distance(self.sample.seq_max[factor], std.seq_max) for std in stds]
        self.va = [plot_image(visual_analysis, xr) for xr in self.distance]
        self.ntest = [test_normal(xr, qq=False) for xr in self.distance]
        self.stat = [stat_analysis(xr) for xr in self.distance]

    def get_report(self, doc: Printer):
        doc.add_heading("{} {} и группа эталонов".format(self.sample_name, FACTORS_L[self.factor]), 0)

        doc.add_heading("Отчеты по эталонам", 1)
        for idx, std in enumerate(self.stds):
            doc.add_heading("Для эталона {}".format(std.name), 1)
            doc.add_paragraph("Последовательность расстояний. Количество значений равно = {}"
                              .format(len(self.distance[idx])))
            doc.add_paragraph(str_arr(self.distance[idx]))
            doc.add_heading("Результаты визуального анализа распределения расстояний", 2)
            doc.add_picture(self.va[idx])
            doc.add_heading("Результаты тестирования нормальности распределения расстояний", 2)
            report_ntest(self.ntest[idx], doc)
            doc.add_heading("Результаты статистического анализа распределения расстояний", 2)
            report_stats(self.stat[idx], doc)


class MulStandardsSample:
    def __init__(self, stds: list, sample: Sample):
        self.stds = stds[:]
        self.sample = sample
        self.sample_name = sample.display()

        self.distance = [[sequence_distance_1(sample.seq_max[factor], std.seq_max) for factor in range(4)]
                         for std in stds]
        self.va = [[plot_image(visual_analysis, factor) for factor in xr] for xr in self.distance]
        self.ntest = [[test_normal(factor, qq=False) for factor in xr] for xr in self.distance]
        self.stat = [[stat_analysis(factor) for factor in xr] for xr in self.distance]

    def get_report(self, doc: Printer):
        doc.add_heading("{} и группа эталонов".format(self.sample_name), 0)

        doc.add_heading("Отчеты по эталонам", 1)
        for idx, std in enumerate(self.stds):
            doc.add_heading("Для эталона {}".format(std.name), 1)
            for factor, factor_name in enumerate(FACTORS_L):
                doc.add_heading("Для фактор-образца {}".format(factor_name), 1)
                doc.add_paragraph("Последовательность расстояний для образца {} и эталона {}. "
                                  "Количество значений равно = {}".format(factor_name,
                                                                          std.name, len(self.distance[idx][factor])))
                doc.add_paragraph(str_arr(self.distance[idx][factor]))
                doc.add_heading("Результаты визуального анализа распределения расстояний "
                                "фактор-образца {} и эталона {}".format(factor_name, std.name), 2)
                doc.add_picture(self.va[idx][factor])
                doc.add_heading("Результаты тестирования нормальности распределения расстояний "
                                "фактор-образца {} и эталона {}".format(factor_name, std.name), 2)
                report_ntest(self.ntest[idx][factor], doc)
                doc.add_heading("Результаты статистического анализа распределения расстояний "
                                "фактор-образца {} и эталона {}".format(factor_name, std.name), 2)
                report_stats(self.stat[idx][factor], doc)


class StandardMulFactorSamples:
    def __init__(self, std: Standard, samples: list, factor: int):
        self.std = std
        self.samples = samples[:]
        self.factor = factor

        self.distance = [sequence_distance_1(sample.seq_max[factor], std.seq_max) for sample in samples]

        self.max_list = []
        for sample_num in range(len(samples)):
            self.max_list.append(np.mean(self.distance[sample_num][factor]))

        self.va = plot_image(visual_analysis, self.max_list)
        self.ntest = test_normal(self.max_list, qq=False)
        self.stat = stat_analysis(self.max_list)

    def get_report(self, doc: Printer):
        doc.add_heading("Группа образцов. Эталон {}".format(self.std.name), 0)

        factor_name = FACTORS_L[self.factor]
        doc.add_heading("Распределение средних значений образцов {}".format(factor_name), 2)
        doc.add_paragraph(str_arr(self.max_list))
        doc.add_heading("Результаты визуального анализа распределений средних значений фактор-образцов {}"
                        .format(factor_name), 2)
        doc.add_picture(self.va)
        doc.add_heading("Результаты тестирования нормальности распределений средних значений фактор-образцов {}"
                        .format(factor_name), 2)
        report_ntest(self.ntest, doc)
        doc.add_heading("Результаты статистического анализа распределений средних значений фактор-образцов {}"
                        .format(factor_name), 2)
        report_stats(self.stat, doc)

    def get_report_stat(self, doc: Printer):
        # TODO: Костыль 2, стоит от этого избавиться
        doc.add_heading("Фактор {}. Эталон {}".format(FACTORS_L[self.factor], self.std.name), 0)

        doc.add_heading("Результат статистического анализа распределения расстояний значений эталона", 1)
        report_stats(self.stat, doc)

    def get_report_ntest(self, doc: Printer):
        # TODO: Костыль 3, стоит от этого избавиться
        doc.add_heading("Фактор {}. Эталон {}".format(FACTORS_L[self.factor], self.std.name), 0)
        doc.add_heading("Результаты тестирования нормальности распределения расстояний значений эталона", 1)
        report_ntest(self.ntest, doc)


class StandardMulSamples:
    def __init__(self, std: Standard, samples: list):
        self.std = std
        self.samples = samples[:]

        self.distance = [[sequence_distance_1(sample.seq_max[factor], std.seq_max) for factor in range(4)]
                         for sample in samples]

        self.max_list = []
        for factor in range(4):
            max_list_factor = []
            for sample_num in range(len(samples)):
                max_list_factor.append(np.mean(self.distance[sample_num][factor]))
            self.max_list.append(max_list_factor)

        self.va = [plot_image(visual_analysis, xr) for xr in self.max_list]
        self.ntest = [test_normal(max_list_factor, qq=False) for max_list_factor in self.max_list]
        self.stat = [stat_analysis(max_list_factor) for max_list_factor in self.max_list]

    def get_report(self, doc: Printer):
        doc.add_heading("Группа образцов. Эталон {}".format(self.std.name), 0)

        for factor in range(4):
            factor_name = FACTORS_L[factor]
            doc.add_heading("Для фактора {}".format(factor_name), 1)
            doc.add_heading("Распределение средних значений образцов {}".format(factor_name), 2)
            doc.add_paragraph(str_arr(self.max_list[factor]))
            doc.add_heading("Результаты  визуального  анализа распределений средних значений фактор-образцов {}"
                            .format(factor_name), 2)
            doc.add_picture(self.va[factor])
            doc.add_heading("Результаты тестирования нормальности распределений средних значений фактор-образцов {}"
                            .format(factor_name), 2)
            report_ntest(self.ntest[factor], doc)
            doc.add_heading("Результаты статистического анализа распределений средних значений фактор-образцов {}"
                            .format(factor_name), 2)
            report_stats(self.stat[factor], doc)


class MulStandardsMulFactorSamples:
    def __init__(self, stds: list, samples: list, factor: int):
        self.stds = stds[:]
        self.samples = samples[:]
        self.factor = factor

        self.distance = [[sequence_distance_1(sample.seq_max[self.factor], std.seq_max)
                          for sample in samples] for std in stds]

        self.max_list = [[np.mean(std[sample_num][self.factor]) for sample_num in range(len(self.samples))]
                         for std in self.distance]

        self.va = [plot_image(visual_analysis, xr) for xr in self.max_list]
        self.ntest = [test_normal(xr, qq=False) for xr in self.max_list]
        self.stat = [stat_analysis(xr) for xr in self.max_list]

    def get_report(self, doc: Printer):
        doc.add_heading("{} Группа эталонов".format(Sample.display_file_group(self.factor)), 0)

        doc.add_heading("Распределение средних значений образцов {}".format(FACTORS_L[self.factor]), 1)
        for std, ml in zip(self.stds, self.max_list):
            doc.add_heading("Для эталона {}".format(std.name), 2)
            doc.add_paragraph(str_arr(ml))

        doc.add_heading("Результаты визуального анализа распределений средних значений", 1)
        for std, va in zip(self.stds, self.va):
            doc.add_heading("Для эталона {}".format(std.name), 2)
            doc.add_picture(va)

        doc.add_heading("Результаты тестирования нормальности распределений средних значений", 1)
        for std, ntest in zip(self.stds, self.ntest):
            doc.add_heading("Для эталона {}".format(std.name), 2)
            report_ntest(ntest, doc)

        doc.add_heading("Результаты статистического анализа распределений средних значений", 1)
        for std, stat in zip(self.stds, self.stat):
            doc.add_heading("Для эталона {}".format(std.name), 2)
            report_stats(stat, doc)


class MulStandardsMulSamples:
    def __init__(self, stds: list, samples: list):
        self.stds = stds[:]
        self.samples = samples[:]

        self.distance = [[[sequence_distance_1(factor, std.seq_max) for factor in sample.seq_max]
                          for sample in samples] for std in stds]

        self.max_list = [[[np.mean(std[sample_num][factor]) for sample_num in range(len(self.samples))]
                          for factor in range(4)] for std in self.distance]

        self.va = [[plot_image(visual_analysis, factor) for factor in xr] for xr in self.max_list]
        self.ntest = [[test_normal(factor, qq=False) for factor in std] for std in self.max_list]
        self.stat = [[stat_analysis(factor) for factor in std] for std in self.max_list]

    def get_report(self, doc: Printer):
        doc.add_heading("Группа образцов. Группа эталонов", 0)

        for idx, std in enumerate(self.stds):
            for factor in range(4):
                factor_name = FACTORS_L[factor]
                doc.add_heading("Для эталона {} и фактора {}".format(std.name, factor_name), 1)
                doc.add_heading("Распределение средних значений образцов {}".format(factor_name), 2)
                doc.add_paragraph(str(self.max_list[idx][factor]))
                doc.add_heading("Результаты  визуального  анализа распределений средних значений фактор-образцов {}"
                                .format(factor_name), 2)
                doc.add_picture(self.va[idx][factor])
                doc.add_heading("Результаты тестирования нормальности распределений средних значений фактор-образцов {}"
                                .format(factor_name), 2)
                report_ntest(self.ntest[idx][factor], doc)
                doc.add_heading("Результаты статистического анализа распределений средних значений фактор-образцов {}"
                                .format(factor_name), 2)
                report_stats(self.stat[idx][factor], doc)
