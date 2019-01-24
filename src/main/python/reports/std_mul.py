from science import plot_image, FACTORS_L
from science.funcs import *
from science.classes import Standard, Sample

from reports import Printer, str_arr, report_error
from reports.utils import report_ntest, report_stats


class StandardMulFactorSamples:
    @report_error("init")
    def __init__(self, std: Standard, samples: list, factor: int):
        self.std = std
        self.samples = samples[:]
        self.factor = factor

        self.distance = [sequence_distance_1(sample.seq_max[self.factor], self.std.seq_max) for sample in self.samples]

        self.max_list = []
        for sample_num in range(len(self.samples)):
            self.max_list.append(np.mean(self.distance[sample_num]))

        self.va = plot_image(visual_analysis, self.max_list)
        self.stat = stat_analysis(self.max_list)
        self.ntest = test_normal(self.max_list, qq=True)

        self.factor_name = FACTORS_L[self.factor]
    
    @report_error("doc")
    def get_report(self, doc: Printer):
        doc.add_heading("Эталон {}. Группа образцов".format(self.std.name), 0)

        doc.add_heading("Распределение средних значений фактор-образцов {}".format(self.factor_name), 2)
        doc.add_paragraph(str_arr(self.max_list))

        doc.add_heading("Результаты визуального анализа распределений средних значений фактор-образцов {}"
                        .format(self.factor_name), 2)
        doc.add_picture(self.va)

        doc.add_heading("Результаты статистического анализа распределений средних значений фактор-образцов {}"
                        .format(self.factor_name), 2)
        report_stats(self.stat, doc)

        doc.add_heading("Результаты тестирования нормальности распределений средних значений фактор-образцов {}"
                        .format(self.factor_name), 2)
        report_ntest(self.ntest, doc)
    
    @report_error("ui")
    def get_report_stat(self, doc: Printer):
        doc.add_heading("Эталон {}. Фактор {}".format(self.std.name, self.factor_name), 0)
        doc.add_heading("Результат статистического анализа распределения расстояний фактор-образцов", 1)
        report_stats(self.stat, doc)
    
    @report_error("ui")
    def get_report_ntest(self, doc: Printer):
        doc.add_heading("Эталон {}. Фактор {}".format(self.std.name, self.factor_name), 0)
        doc.add_heading("Результаты тестирования нормальности распределения расстояний фактор-образцов", 1)
        report_ntest(self.ntest, doc)


class StandardMulSamples:
    @report_error("init")
    def __init__(self, std: Standard, samples: list):
        self.std = std
        self.samples = samples[:]

        self.distance = [[sequence_distance_1(sample.seq_max[factor], self.std.seq_max) for sample in self.samples]
                         for factor in range(4)]

        self.max_list = []
        for factor in range(4):
            max_list_factor = []
            for sample_num in range(len(self.samples)):
                max_list_factor.append(np.mean(self.distance[factor][sample_num]))
            self.max_list.append(max_list_factor)

        self.va = [plot_image(visual_analysis, max_list_factor) for max_list_factor in self.max_list]
        self.stat = [stat_analysis(max_list_factor) for max_list_factor in self.max_list]
        self.ntest = [test_normal(max_list_factor, qq=True) for max_list_factor in self.max_list]
    
    @report_error("doc")
    def get_report(self, doc: Printer):
        doc.add_heading("Эталон {}. Группа образцов".format(self.std.name), 0)

        doc.add_heading("Распределение средних значений", 1)
        for factor, factor_name in enumerate(FACTORS_L):
            doc.add_heading("Распределение средних значений фактор-образцов {}".format(factor_name), 2)
            doc.add_paragraph("Количество значений равно = {}".format(len(self.max_list[factor])))
            doc.add_paragraph(str_arr(self.max_list[factor]))

        doc.add_heading("Результаты визуального анализа", 1)
        for factor, factor_name in enumerate(FACTORS_L):
            doc.add_heading("Результаты  визуального анализа распределений средних значений фактор-образцов {}"
                            .format(factor_name), 2)
            doc.add_picture(self.va[factor])

        doc.add_heading("Результаты статистического анализа распределения расстояний", 1)
        for factor, factor_name in enumerate(FACTORS_L):
            doc.add_heading("Результаты статистического анализа распределений средних значений фактор-образцов {}"
                            .format(factor_name), 2)
            report_stats(self.stat[factor], doc)

        doc.add_heading("Результаты тестирования нормальности", 1)
        for factor, factor_name in enumerate(FACTORS_L):
            doc.add_heading("Результаты тестирования нормальности распределений средних значений фактор-образцов {}"
                            .format(factor_name), 2)
            report_ntest(self.ntest[factor], doc)


class MulStandardsFactorSample:
    @report_error("init")
    def __init__(self, stds: list, sample: Sample, factor: int):
        self.stds = stds[:]
        self.sample = sample
        self.factor = factor

        self.distance = [sequence_distance_1(self.sample.seq_max[factor], std.seq_max) for std in self.stds]
        self.va = [plot_image(visual_analysis, xr) for xr in self.distance]
        self.stat = [stat_analysis(xr) for xr in self.distance]
        self.ntest = [test_normal(xr, qq=True) for xr in self.distance]

        self.sample_name = self.sample.display()
        self.factor_name = FACTORS_L[self.factor]

    @report_error("doc")
    def get_report(self, doc: Printer):
        doc.add_heading("Группа эталонов. {} {}".format(self.sample_name, self.factor_name), 0)

        doc.add_heading("Последовательности расстояний от фактор-образца {}".format(self.factor_name), 1)
        for std, xr in zip(self.stds, self.distance):
            doc.add_heading("Последовательность расстояний до эталона {}".format(std.name), 2)
            doc.add_paragraph("Количество значений равно = {}".format(len(xr)))
            doc.add_paragraph(str_arr(xr))

        doc.add_heading(
            "Результаты визуального анализа распределения расстояний от фактор-образца {}".format(self.factor_name), 1)
        for std, va in zip(self.stds, self.va):
            doc.add_heading("Результаты визуального анализа распределения расстояний до эталона {}".format(std.name), 2)
            doc.add_picture(va)

        doc.add_heading(
            "Результаты статистического анализа распределения расстояний от фактор-образца {}".format(self.factor_name),
            1)
        for std, stat in zip(self.stds, self.stat):
            doc.add_heading("Результаты статистического анализа распределения расстояний до эталона {}"
                            .format(std.name), 2)
            report_stats(stat, doc)

        doc.add_heading("Результаты тестирования нормальности распределения расстояний от фактор-образца {}".format(
            self.factor_name), 1)
        for std, ntest in zip(self.stds, self.ntest):
            doc.add_heading("Результаты тестирования нормальности распределения расстояний до эталона {}"
                            .format(std.name), 2)
            report_ntest(ntest, doc)


class MulStandardsSample:
    @report_error("init")
    def __init__(self, stds: list, sample: Sample):
        self.stds = stds[:]
        self.sample = sample

        self.distance = [[sequence_distance_1(self.sample.seq_max[factor], std.seq_max) for factor in range(4)]
                         for std in self.stds]
        self.va = [[plot_image(visual_analysis, factor) for factor in xr] for xr in self.distance]
        self.stat = [[stat_analysis(factor) for factor in xr] for xr in self.distance]
        self.ntest = [[test_normal(factor, qq=True) for factor in xr] for xr in self.distance]

        self.sample_name = self.sample.display()

    @report_error("doc")
    def get_report(self, doc: Printer):
        doc.add_heading("Группа эталонов. {}".format(self.sample_name), 0)

        for factor, factor_name in enumerate(FACTORS_L):
            doc.add_heading("Для фактора {}".format(factor_name), 1)

            doc.add_heading("Последовательности расстояний от фактор-образца {}".format(factor_name), 1)
            for idx, std in enumerate(self.stds):
                doc.add_heading(
                    "Последовательность расстояний от максимумов фактор-образца {} до ближайшего максимума эталона {}"
                        .format(factor_name, std.name), 2)
                # doc.add_paragraph("Количество значений равно = {}".format(len(self.distance[idx][factor])))
                doc.add_paragraph(str_arr(self.distance[idx][factor]))

            doc.add_heading("Результаты визуального анализа распределения расстояний от фактор-образца {}"
                            .format(factor_name), 1)
            for idx, std in enumerate(self.stds):
                doc.add_heading("Результаты визуального анализа распределения расстояний до эталона {}"
                                .format(std.name), 2)
                doc.add_picture(self.va[idx][factor])

            doc.add_heading("Результаты статистического анализа распределения расстояний от фактор-образца {}"
                            .format(factor_name), 1)
            for idx, std in enumerate(self.stds):
                doc.add_heading("Результаты статистического анализа распределения расстояний до эталона {}"
                                .format(std.name), 2)
                report_stats(self.stat[idx][factor], doc)

            doc.add_heading("Результаты тестирования нормальности распределения расстояний от фактор-образца {}"
                            .format(factor_name), 1)
            for idx, std in enumerate(self.stds):
                doc.add_heading("Результаты тестирования нормальности распределения расстояний до эталона {}"
                                .format(std.name), 2)
                report_ntest(self.ntest[idx][factor], doc)


class MulStandardsMulFactorSamples:
    @report_error("init")
    def __init__(self, stds: list, samples: list, factor: int):
        self.stds = stds[:]
        self.samples = samples[:]
        self.factor = factor

        self.distance = [[sequence_distance_1(sample.seq_max[self.factor], std.seq_max)
                          for sample in self.samples] for std in self.stds]

        self.max_list = [[np.mean(std[sample_num]) for sample_num in range(len(self.samples))]
                         for std in self.distance]

        self.va = [plot_image(visual_analysis, xr) for xr in self.max_list]
        self.stat = [stat_analysis(xr) for xr in self.max_list]
        self.ntest = [test_normal(xr, qq=True) for xr in self.max_list]

        self.factor_name = FACTORS_L[self.factor]

    @report_error("doc")
    def get_report(self, doc: Printer):
        doc.add_heading("Группа эталонов. {}".format(Sample.display_file_group(self.factor)), 0)

        doc.add_heading("Распределение средних значений фактор-образцов {}".format(self.factor_name), 1)
        for std, ml in zip(self.stds, self.max_list):
            doc.add_heading("Для эталона {}".format(std.name), 2)
            doc.add_paragraph(str_arr(ml))

        doc.add_heading(
            "Результаты визуального анализа распределений средних значений фактор-образцов {}".format(self.factor_name),
            1)
        for std, va in zip(self.stds, self.va):
            doc.add_heading("Для эталона {}".format(std.name), 2)
            doc.add_picture(va)

        doc.add_heading("Результаты статистического анализа распределений средних значений фактор-образцов {}".format(
            self.factor_name), 1)
        for std, stat in zip(self.stds, self.stat):
            doc.add_heading("Для эталона {}".format(std.name), 2)
            report_stats(stat, doc)

        doc.add_heading("Результаты тестирования нормальности распределений средних значений фактор-образцов {}".format(
            self.factor_name), 1)
        for std, ntest in zip(self.stds, self.ntest):
            doc.add_heading("Для эталона {}".format(std.name), 2)
            report_ntest(ntest, doc)


class MulStandardsMulSamples:
    @report_error("init")
    def __init__(self, stds: list, samples: list):
        self.stds = stds[:]
        self.samples = samples[:]

        self.distance = [[[sequence_distance_1(factor, std.seq_max) for factor in sample.seq_max]
                          for sample in self.samples] for std in self.stds]

        self.max_list = [[[np.mean(std[sample_num][factor]) for sample_num in range(len(self.samples))]
                          for factor in range(4)] for std in self.distance]

        self.va = [[plot_image(visual_analysis, factor) for factor in xr] for xr in self.max_list]
        self.stat = [[stat_analysis(factor) for factor in std] for std in self.max_list]
        self.ntest = [[test_normal(factor, qq=True) for factor in std] for std in self.max_list]

    @report_error("doc")
    def get_report(self, doc: Printer):
        doc.add_heading("Группа эталонов. Группа образцов", 0)

        for factor, factor_name in enumerate(FACTORS_L):
            doc.add_heading("Для фактора {}".format(factor_name), 1)

            doc.add_heading("Распределения средних значений фактор-образцов {}".format(factor_name), 1)
            for idx, std in enumerate(self.stds):
                doc.add_heading("Для эталона {}".format(std.name), 2)
                doc.add_paragraph("Количество значений равно = {}".format(len(self.max_list[idx][factor])))
                doc.add_paragraph(str_arr(self.max_list[idx][factor]))

            doc.add_heading("Результаты визуального анализа распределений средних значений фактор-образцов {}"
                            .format(factor_name), 1)
            for idx, std in enumerate(self.stds):
                doc.add_heading("Для эталона {}".format(std.name), 2)
                doc.add_picture(self.va[idx][factor])

            doc.add_heading("Результаты статистического анализа распределений средних значений фактор-образцов {}"
                            .format(factor_name), 1)
            for idx, std in enumerate(self.stds):
                doc.add_heading("Для эталона {}".format(std.name), 2)
                report_stats(self.stat[idx][factor], doc)

            doc.add_heading("Результаты тестирования нормальности распределений средних значений фактор-образцов {}"
                            .format(factor_name), 1)
            for idx, std in enumerate(self.stds):
                doc.add_heading("Для эталона {}".format(std.name), 2)
                report_ntest(self.ntest[idx][factor], doc)
