from science import plot_image, FACTORS
from science.funcs import *
from science.classes import Standard, Sample

from reports import Printer, str_arr
from reports.utils import report_ntest


class FactorSampleMulStandards:
    def __init__(self, sample: Sample, factor: int, stds: list):
        self.sample = sample
        self.sample_name = "Групповой образец" if self.sample.name == "group" else "Образец " + self.sample.name
        self.factor = factor
        self.stds = stds[:]

        self.distance = [sequence_distance(self.sample.seq_max[factor], std.seq_max) for std in stds]
        self.va = [plot_image(visual_analysis, xr) for xr in self.distance]
        self.ntest = [test_normal(xr, qq=False) for xr in self.distance]
        self.stat = [stat_analysis(xr) for xr in self.distance]

    def get_report(self, doc: Printer):
        doc.add_heading("{}, фактор {} и группа эталонов".format(self.sample_name, FACTORS[self.factor]), 0)

        doc.add_heading("Отчеты по эталонам", 1)
        for idx, std in enumerate(self.stds):
            doc.add_paragraph("Последовательность расстояний для эталона {}. Количество значений равно = {}"
                              .format(std.name, len(self.distance[idx])))
            doc.add_paragraph(str(self.distance[idx]))
            doc.add_heading("\nРезультаты визуального анализа распределения расстояний для эталона {}"
                            .format(std.name), 2)
            doc.add_picture(self.va[idx])
            doc.add_heading("\nРезультаты тестирования нормальности распределения расстояний для эталона {}"
                            .format(std.name), 2)
            report_ntest(self.ntest[idx], doc)
            doc.add_heading("\nРезультаты статистического анализа распределения расстояний для эталона {}"
                            .format(std.name), 2)
            doc.add_paragraph("\tВыборочное среднее = {:.4f}".format(self.stat[idx][0]))
            doc.add_paragraph("\tСтандартное отклонение = {:.4f}".format(self.stat[idx][1]))
            doc.add_paragraph("\tДоверительный интервал = ({:.4f}, {:.4f})".format(*self.stat[idx][2]))


class SampleMulStandards:
    def __init__(self, sample: Sample, stds: list):
        self.sample = sample
        self.sample_name = "Групповой образец" if self.sample.name == "group" else "Образец " + self.sample.name
        self.stds = stds[:]

        self.distance = [[sequence_distance_1(sample.seq_max[factor], std.seq_max) for factor in range(4)]
                         for std in stds]
        self.va = [[plot_image(visual_analysis, factor) for factor in xr] for xr in self.distance]
        self.ntest = [[test_normal(factor, qq=False) for factor in xr] for xr in self.distance]
        self.stat = [[stat_analysis(factor) for factor in xr] for xr in self.distance]

    def get_report(self, doc: Printer):
        doc.add_heading("{} и группа эталонов".format(self.sample_name), 0)

        doc.add_heading("Отчеты по эталонам", 1)
        for idx, std in enumerate(self.stds):
            for factor in range(4):
                doc.add_heading("\nАнализ фактор-образца {}".format(FACTORS[factor]), 2)
                doc.add_paragraph("Последовательность расстояний для образца {} и эталона {}. "
                                  "Количество значений равно = {}".format(FACTORS[factor],
                                                                          std.name, len(self.distance[idx][factor])))
                doc.add_paragraph(str(self.distance[idx][factor]))
                doc.add_heading("\nРезультаты визуального анализа распределения расстояний "
                                "фактор-образца {} и эталона {}".format(FACTORS[factor], std.name), 2)
                doc.add_picture(self.va[idx][factor])
                doc.add_heading("\nРезультаты тестирования нормальности распределения расстояний "
                                "фактор-образца {} и эталона {}".format(FACTORS[factor], std.name), 2)
                report_ntest(self.ntest[idx][factor], doc)
                doc.add_heading("\nРезультаты статистического анализа распределения расстояний "
                                "фактор-образца {} и эталона {}".format(FACTORS[factor], std.name), 2)
                doc.add_paragraph("\tВыборочное среднее = {:.4f}".format(self.stat[idx][factor][0]))
                doc.add_paragraph("\tСтандартное отклонение = {:.4f}".format(self.stat[idx][factor][1]))
                doc.add_paragraph("\tДоверительный интервал = ({:.4f}, {:.4f})".format(*self.stat[idx][factor][2]))


class MulFactorSamplesStandard:
    def __init__(self, samples: list, factor: int, std: Standard):
        self.samples = samples[:]
        self.factor = factor
        self.std = std

        self.distance = [sequence_distance_1(sample.seq_max[factor], std.seq_max) for sample in samples]

        self.max_list = []
        for sample_num in range(len(samples)):
            self.max_list.append(np.mean(self.distance[sample_num][factor]))

        self.va = plot_image(visual_analysis, self.max_list)
        self.ntest = test_normal(self.max_list, qq=False)
        self.stat = stat_analysis(self.max_list)

    def get_report(self, doc: Printer):
        doc.add_heading("Группа образцов. Эталон {}".format(self.std.name), 0)

        factor_name = FACTORS[self.factor].lower()
        doc.add_heading("Распределение средних значений образцов {}".format(factor_name), 2)
        doc.add_paragraph(str_arr(self.max_list))
        doc.add_heading("Результаты  визуального  анализа распределений средних значений фактор-образцов {}"
                        .format(factor_name), 2)
        doc.add_picture(self.va)
        doc.add_heading("Результаты тестирования нормальности распределений средних значений фактор-образцов {}"
                        .format(factor_name), 2)
        report_ntest(self.ntest, doc)
        doc.add_heading("Результаты статистического анализа распределений средних значений фактор-образцов {}"
                        .format(factor_name), 2)
        doc.add_paragraph("\tВыборочное среднее = {:.4f}".format(self.stat[0]))
        doc.add_paragraph("\tСтандартное отклонение = {:.4f}".format(self.stat[1]))
        doc.add_paragraph("\tДоверительный интервал = ({:.4f}, {:.4f})".format(*self.stat[2]))

    def get_report_stat(self, doc: Printer):
        # TODO: Костыль 2, стоит от этого избавиться
        doc.add_heading("Фактор {}. Эталон {}".format(FACTORS[self.factor], self.std.name), 0)

        doc.add_heading("Результат статистического анализа распределения расстояний значений эталона", 1)
        doc.add_paragraph("\tВыборочное среднее = {:.3f}".format(self.stat[0]))
        doc.add_paragraph("\tСтандартное отклонение = {:.3f}".format(self.stat[1]))
        doc.add_paragraph("\tДоверительный интервал = ({:.3f}, {:.3f})".format(*self.stat[2]))

    def get_report_ntest(self, doc: Printer):
        # TODO: Костыль 3, стоит от этого избавиться
        doc.add_heading("Фактор {}. Эталон {}".format(FACTORS[self.factor], self.std.name), 0)
        doc.add_heading("Результаты тестирования нормальности распределения расстояний значений эталона", 1)
        report_ntest(self.ntest, doc)


class MulSamplesStandard:
    def __init__(self, samples: list, std: Standard):
        self.samples = samples[:]
        self.std = std

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
            factor_name = FACTORS[factor].lower()
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
            doc.add_paragraph("\tВыборочное среднее = {:.4f}".format(self.stat[factor][0]))
            doc.add_paragraph("\tСтандартное отклонение = {:.4f}".format(self.stat[factor][1]))
            doc.add_paragraph("\tДоверительный интервал = ({:.4f}, {:.4f})".format(*self.stat[factor][2]))


class MulSamplesMulStandards:
    def __init__(self, samples: list, stds: list):
        self.samples = samples[:]
        self.stds = stds[:]

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
                factor_name = FACTORS[factor].lower()
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
                doc.add_paragraph("\tВыборочное среднее = {:.4f}".format(self.stat[idx][factor][0]))
                doc.add_paragraph("\tСтандартное отклонение = {:.4f}".format(self.stat[idx][factor][1]))
                doc.add_paragraph("\tДоверительный интервал = ({:.4f}, {:.4f})".format(*self.stat[idx][factor][2]))
