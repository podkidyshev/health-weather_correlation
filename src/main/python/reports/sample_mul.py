from science import plot_image, FACTORS
from science.funcs import *
from science.classes import Standard, Sample

from reports import Printer, str_arr
from reports.utils import report_ntest, report_stats


class MulStandardsSample:
    def __init__(self, stds: list, sample: Sample):
        self.stds = stds[:]
        self.sample = sample
        self.sample_name = "Групповой образец" if self.sample.name == "group" else "Образец " + self.sample.name

        self.distance = [[sequence_distance_1(std.seq_max, sample.seq_max[factor]) for factor in range(4)]
                         for std in stds]
        self.va = [[plot_image(visual_analysis, factor) for factor in xr] for xr in self.distance]
        self.ntest = [[test_normal(factor, qq=False) for factor in xr] for xr in self.distance]
        self.stat = [[stat_analysis(factor) for factor in xr] for xr in self.distance]

        self.distance_apl = [[sequence_distance_1(std.seq_max_apl, sample.seq_max0[factor]) for factor in range(4)]
                             for std in stds]
        self.va_apl = [[plot_image(visual_analysis, factor) for factor in xr] for xr in self.distance_apl]
        self.ntest_apl = [[test_normal(factor, qq=False) for factor in xr] for xr in self.distance_apl]
        self.stat_apl = [[stat_analysis(factor) for factor in xr] for xr in self.distance_apl]

    def get_report(self, doc: Printer):
        doc.add_heading("Группа эталонов и {}".format(self.sample_name), 0)

        doc.add_heading("Отчеты по эталонам", 1)
        for idx, std in enumerate(self.stds):
            for factor in range(4):
                doc.add_heading("\nАнализ фактор-образца {}".format(FACTORS[factor]), 2)
                doc.add_paragraph("Последовательность расстояний значений для эталона {} и образца {}."
                                  "Количество значений равно = {}".format(std.name, FACTORS[factor],
                                                                          len(self.distance[idx][factor])))
                doc.add_paragraph(str_arr(self.distance[idx][factor]))
                doc.add_heading("\nРезультаты визуального анализа распределения расстояний значений "
                                "эталона {} фактор-образца {}".format(std.name, FACTORS[factor]), 2)
                doc.add_picture(self.va[idx][factor])
                doc.add_heading("\nРезультаты тестирования нормальности распределения расстояний значений "
                                "эталона {} и фактор-образца {}".format(std.name, FACTORS[factor]), 2)
                report_ntest(self.ntest[idx][factor], doc)
                doc.add_heading("\nРезультаты статистического анализа распределения расстояний значений "
                                "эталона {} и фактор-образца {}".format(std.name, FACTORS[factor]), 2)
                report_stats(self.stat[idx][factor], doc)

                doc.add_paragraph("Последовательность расстояний амплитуд для эталона {} и образца {}."
                                  "Количество значений равно = {}".format(std.name, FACTORS[factor],
                                                                          len_ampl(self.distance_apl[idx][factor])))
                doc.add_paragraph(str_arr(self.distance_apl[idx][factor]))
                doc.add_heading("\nРезультаты визуального анализа распределения расстояний амплитуд "
                                "эталона {} фактор-образца {}".format(std.name, FACTORS[factor]), 2)
                doc.add_picture(self.va_apl[idx][factor])
                doc.add_heading("\nРезультаты тестирования нормальности распределения расстояний амплитуд "
                                "эталона {} и фактор-образца {}".format(std.name, FACTORS[factor]), 2)
                report_ntest(self.ntest_apl[idx][factor], doc)
                doc.add_heading("\nРезультаты статистического анализа распределения расстояний амплитуд "
                                "эталона {} и фактор-образца {}".format(std.name, FACTORS[factor]), 2)
                report_stats(self.stat_apl[idx][factor], doc)


class MulStandardsFactorSample:
    def __init__(self, stds: list, sample: Sample, factor: int):
        self.stds = stds[:]
        self.sample = sample
        self.factor = factor

        self.distance = [sequence_distance_1(std.seq_max, sample.seq_max[self.factor]) for std in stds]
        self.va = [plot_image(visual_analysis, xr) for xr in self.distance]
        self.ntest = [test_normal(xr, qq=False) for xr in self.distance]
        self.stat = [stat_analysis(xr) for xr in self.distance]

        self.distance_apl = [sequence_distance_1(std.seq_max_apl, sample.seq_max0[factor]) for std in stds]
        self.va_apl = [plot_image(visual_analysis, xr) for xr in self.distance_apl]
        self.ntest_apl = [test_normal(xr, qq=False) for xr in self.distance_apl]
        self.stat_apl = [stat_analysis(xr) for xr in self.distance_apl]

    def get_report(self, doc: Printer):
        doc.add_heading("Группа эталонов и {}".format(self.sample.display_file(self.factor).lower()), 0)

        doc.add_heading("Последовательности расстояний", 1)
        for std, xr in zip(self.stds, self.distance):
            doc.add_heading("Для эталона {}".format(std.name), 2)
            doc.add_paragraph("Количество значений равно = {}".format(len(xr)))
            doc.add_paragraph(str_arr(xr))
        doc.add_heading("Результаты визуального анализа распределения расстояний", 1)
        for std, va in zip(self.stds, self.va):
            doc.add_heading("Для эталона {}".format(std.name), 2)
            doc.add_picture(va)
        doc.add_heading("Результаты тестирования нормальности распределения расстояний", 1)
        for std, ntest in zip(self.stds, self.ntest):
            doc.add_heading("Для эталона {}".format(std.name), 2)
            report_ntest(ntest, doc)
        doc.add_heading("Результаты статистического анализа распределения расстояний", 1)
        for std, stat in zip(self.stds, self.stat):
            doc.add_heading("Для эталона {}".format(std.name), 2)
            report_stats(stat, doc)

        doc.add_heading("Последовательности расстояний амплитуд", 1)
        for std, xr in zip(self.stds, self.distance):
            doc.add_heading("Для эталона {}".format(std.name), 2)
            doc.add_paragraph("Количество значений равно = {}".format(len(xr)))
            doc.add_paragraph(str_arr(xr))
        doc.add_heading("Результаты визуального анализа распределения расстояний амплитуд", 1)
        for std, va in zip(self.stds, self.va):
            doc.add_heading("Для эталона {}".format(std.name), 2)
            doc.add_picture(va)
        doc.add_heading("Результаты тестирования нормальности распределения расстояний амплитуд", 1)
        for std, ntest in zip(self.stds, self.ntest):
            doc.add_heading("Для эталона {}".format(std.name), 2)
            report_ntest(ntest, doc)
        doc.add_heading("Результаты статистического анализа распределения расстояний амплитуд", 1)
        for std, stat in zip(self.stds, self.stat):
            doc.add_heading("Для эталона {}".format(std.name), 2)
            report_stats(stat, doc)


class StandardMulFactorSamples:
    def __init__(self, std: Standard, samples: list, factor: int):
        self.std = std
        self.samples = samples[:]
        self.factor = factor

        self.distance = [sequence_distance_1(std.seq_max, sample.seq_max[factor]) for sample in samples]

        self.max_list = []
        for sample_num in range(len(samples)):
            self.max_list.append(np.mean(self.distance[sample_num][factor]))

        self.va = plot_image(visual_analysis, self.max_list)
        self.ntest = test_normal(self.max_list, qq=False)
        self.stat = stat_analysis(self.max_list)

        self.distance_apl = [sequence_distance_1(std.seq_max_apl, sample.seq_max0[factor]) for sample in samples]

        self.max_list_apl = []
        for sample_num in range(len(samples)):
            self.max_list_apl.append(np.mean(self.distance_apl[sample_num][factor]))

        self.va_apl = plot_image(visual_analysis, self.max_list_apl)
        self.ntest_apl = test_normal(self.max_list_apl, qq=False)
        self.stat_apl = stat_analysis(self.max_list_apl)

    def get_report(self, doc: Printer):
        doc.add_heading("Эталон {}. Группа образцов".format(self.std.name), 0)

        factor_name = FACTORS[self.factor].lower()
        doc.add_heading("Распределение средних значений эталона {} для образцов {}".format(self.std.name, factor_name), 2)
        doc.add_paragraph(str_arr(self.max_list))
        doc.add_heading("Результаты  визуального  анализа распределений средних значений эталона {} для фактор-образцов {}"
                        .format(self.std.name, factor_name), 2)
        doc.add_picture(self.va)
        doc.add_heading("Результаты тестирования нормальности распределений средних значений эталона {} для фактор-образцов {}"
                        .format(self.std.name, factor_name), 2)
        report_ntest(self.ntest, doc)
        doc.add_heading("Результаты статистического анализа распределений средних значений эталона {} для фактор-образцов {}"
                        .format(self.std.name, factor_name), 2)
        report_stats(self.stat, doc)

        doc.add_heading("Распределение средних амплитуд эталона {} для образцов {}"
                        .format(self.std.name, factor_name), 2)
        doc.add_paragraph(str_arr(self.max_list_apl))
        doc.add_heading(
            "Результаты  визуального  анализа распределений средних амплитуд эталона {} для фактор-образцов {}"
            .format(self.std.name, factor_name), 2)
        doc.add_picture(self.va_apl)
        doc.add_heading(
            "Результаты тестирования нормальности распределений средних амплитуд эталона {} для фактор-образцов {}"
            .format(self.std.name, factor_name), 2)
        report_ntest(self.ntest_apl, doc)
        doc.add_heading(
            "Результаты статистического анализа распределений средних амплитуд эталона {} для фактор-образцов {}"
            .format(self.std.name, factor_name), 2)
        report_stats(self.stat_apl, doc)

    def get_report_stat(self, doc: Printer):
        # TODO: Костыль 2, стоит от этого избавиться
        doc.add_heading("Фактор {}. Эталон {}".format(FACTORS[self.factor], self.std.name), 0)

        doc.add_heading("Результат статистического анализа распределения расстояний значений эталона", 1)
        report_stats(self.stat, doc)

    def get_report_ntest(self, doc: Printer):
        # TODO: Костыль 3, стоит от этого избавиться
        doc.add_heading("Фактор {}. Эталон {}".format(FACTORS[self.factor], self.std.name), 0)
        doc.add_heading("Результаты тестирования нормальности распределения расстояний значений эталона", 1)
        report_ntest(self.ntest, doc)

    def get_report_stat_apl(self, doc: Printer):
        # TODO: Костыль 4, стоит от этого избавиться
        doc.add_heading("Фактор {}. Эталон {}".format(FACTORS[self.factor], self.std.name), 0)

        doc.add_heading("Результат статистического анализа распределения расстояний амплитуд эталона", 1)
        report_stats(self.stat_apl, doc)

    def get_report_ntest_apl(self, doc: Printer):
        # TODO: Костыль 5, стоит от этого избавиться
        doc.add_heading("Фактор {}. Эталон {}".format(FACTORS[self.factor], self.std.name), 0)
        doc.add_heading("Результаты тестирования нормальности распределения расстояний амплитуд эталона", 1)
        report_ntest(self.ntest_apl, doc)


class StandardMulSamples:
    def __init__(self, std: Standard, samples: list):
        self.std = std
        self.samples = samples[:]

        self.distance = [[sequence_distance_1(std.seq_max, sample.seq_max[factor]) for factor in range(4)]
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

        self.distance_apl = [[sequence_distance_1(std.seq_max_apl, sample.seq_max0[factor]) for factor in range(4)]
                             for sample in samples]

        self.max_list_apl = []
        for factor in range(4):
            max_list_factor = []
            for sample_num in range(len(samples)):
                max_list_factor.append(np.mean(self.distance_apl[sample_num][factor]))
            self.max_list_apl.append(max_list_factor)

        self.va_apl = [plot_image(visual_analysis, xr) for xr in self.max_list_apl]
        self.ntest_apl = [test_normal(max_list_factor, qq=False) for max_list_factor in self.max_list_apl]
        self.stat_apl = [stat_analysis(max_list_factor) for max_list_factor in self.max_list_apl]

    def get_report(self, doc: Printer):
        doc.add_heading("Эталон {}. Группа образцов".format(self.std.name), 0)

        for factor in range(4):
            factor_name = FACTORS[factor].lower()
            doc.add_heading("Для фактора {}".format(factor_name), 1)
            doc.add_heading(
                "Распределение средних значений эталона {} для образцов {}".format(self.std.name, factor_name), 2)
            doc.add_paragraph(str_arr(self.max_list[factor]))
            doc.add_heading(
                "Результаты  визуального анализа распределений средних значений эталона {} для фактор-образцов {}"
                .format(self.std.name, factor_name), 2)
            doc.add_picture(self.va[factor])
            doc.add_heading(
                "Результаты тестирования нормальности распределений средних значений эталона {} для фактор-образцов {}"
                .format(self.std.name, factor_name), 2)
            report_ntest(self.ntest[factor], doc)
            doc.add_heading(
                "Результаты статистического анализа распределений средних значений эталона {} для фактор-образцов {}"
                .format(self.std.name, factor_name), 2)
            doc.add_paragraph("\tВыборочное среднее = {:.2f}".format(self.stat[factor][0]))
            doc.add_paragraph("\tСтандартное отклонение = {:.2f}".format(self.stat[factor][1]))
            doc.add_paragraph("\tДоверительный интервал = ({:.2f}, {:.2f})".format(*self.stat[factor][2]))

            doc.add_heading(
                "Распределение средних амплитуд эталона {} для образцов {}".format(self.std.name, factor_name), 2)
            doc.add_paragraph(str_arr(self.max_list_apl[factor]))
            doc.add_heading(
                "Результаты  визуального анализа распределений средних амплитуд эталона {} для фактор-образцов {}"
                    .format(self.std.name, factor_name), 2)
            doc.add_picture(self.va_apl[factor])
            doc.add_heading(
                "Результаты тестирования нормальности распределений средних амплитуд эталона {} для фактор-образцов {}"
                    .format(self.std.name, factor_name), 2)
            report_ntest(self.ntest_apl[factor], doc)
            doc.add_heading(
                "Результаты статистического анализа распределений средних амплитуд эталона {} для фактор-образцов {}"
                    .format(self.std.name, factor_name), 2)
            report_stats(self.stat_apl[factor], doc)


class MulStandardsMulSamples:
    def __init__(self, stds: list, samples: list):
        self.stds = stds[:]
        self.samples = samples[:]

        self.distance = [[[sequence_distance_1(std.seq_max, factor) for factor in sample.seq_max]
                          for sample in samples] for std in stds]

        self.max_list = [[[np.mean(std[sample_num][factor]) for sample_num in range(len(self.samples))]
                          for factor in range(4)] for std in self.distance]

        self.va = [[plot_image(visual_analysis, factor) for factor in xr] for xr in self.max_list]
        self.ntest = [[test_normal(factor, qq=False) for factor in std] for std in self.max_list]
        self.stat = [[stat_analysis(factor) for factor in std] for std in self.max_list]

        self.distance_apl = [[[sequence_distance_1(std.seq_max_apl, factor) for factor in sample.seq_max0]
                              for sample in samples] for std in stds]

        self.max_list_apl = [[[np.mean(std[sample_num][factor]) for sample_num in range(len(self.samples))]
                              for factor in range(4)] for std in self.distance_apl]

        self.va_apl = [[plot_image(visual_analysis, factor) for factor in xr] for xr in self.max_list_apl]
        self.ntest_apl = [[test_normal(factor, qq=False) for factor in std] for std in self.max_list_apl]
        self.stat_apl = [[stat_analysis(factor) for factor in std] for std in self.max_list_apl]

    def get_report(self, doc: Printer):
        doc.add_heading("Группа эталонов. Группа образцов", 0)

        for idx, std in enumerate(self.stds):
            for factor in range(4):
                factor_name = FACTORS[factor].lower()
                doc.add_heading("Для эталона {} и фактора {}".format(std.name, factor_name), 1)
                doc.add_heading(
                    "Распределение средних значений эталона {} для фактора {}".format(std.name, factor_name), 2)
                doc.add_paragraph(str_arr(self.max_list[idx][factor]))
                doc.add_heading(
                    "Результаты  визуального  анализа распределений средних значений эталона {} для фактор-образцов {}"
                    .format(std.name, factor_name), 2)
                doc.add_picture(self.va[idx][factor])
                doc.add_heading(
                    "Результаты тестирования нормальности распределений средних значений эталона {} для фактор-образцов {}"
                    .format(std.name, factor_name), 2)
                report_ntest(self.ntest[idx][factor], doc)
                doc.add_heading(
                    "Результаты статистического анализа распределений средних значений эталона {} для фактор-образцов {}"
                    .format(std.name, factor_name), 2)
                report_stats(self.stat[idx][factor], doc)

                doc.add_heading(
                    "Распределение средних амплитуд эталона {} для фактора {}".format(std.name, factor_name), 2)
                doc.add_paragraph(str_arr(self.max_list_apl[idx][factor]))
                doc.add_heading(
                    "Результаты  визуального  анализа распределений средних амплитуд эталона {} для фактор-образцов {}"
                    .format(std.name, factor_name), 2)
                doc.add_picture(self.va_apl[idx][factor])
                doc.add_heading(
                    "Результаты тестирования нормальности распределений средних амплитуд эталона {} для фактор-образцов {}"
                    .format(std.name, factor_name), 2)
                report_ntest(self.ntest_apl[idx][factor], doc)
                doc.add_heading(
                    "Результаты статистического анализа распределений средних амплитуд эталона {} для фактор-образцов {}"
                    .format(std.name, factor_name), 2)
                report_stats(self.stat_apl[idx][factor], doc)
