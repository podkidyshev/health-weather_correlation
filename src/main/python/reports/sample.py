from reports import Printer, str_arr
from reports.utils import report_ntest, report_stats

from science import plot_image, FACTORS, FACTORS_L
from science.funcs import *
from science.classes import Standard, Sample


class FactorSampleStandard:
    def __init__(self, sample: Sample, factor: int, std: Standard):
        self.sample = sample
        self.factor = factor
        self.std = std

        self.distance = sequence_distance_1(self.std.seq_max, self.sample.seq_max[factor])
        self.va = plot_image(visual_analysis, self.distance)
        self.ntest = test_normal(self.distance, qq=False)
        self.stat = stat_analysis(self.distance)

        self.distance_apl = sequence_distance_1(self.std.seq_max_apl, self.sample.seq_max0[factor])
        self.va_apl = plot_image(visual_analysis, self.distance_apl)
        self.ntest_apl = test_normal(self.distance_apl, qq=False)
        self.stat_apl = stat_analysis(self.distance_apl)

        self.sample_name = sample.display()
        self.factor_name = FACTORS_L[self.factor]

    def get_report(self, doc: Printer):
        x, x_seq_max = self.sample.data[self.factor], self.sample.seq_max[self.factor]
        y, y_seq_max, y_seq_max_apl = self.std.data, self.std.seq_max, self.std.seq_max_apl

        doc.add_heading("{}, фактор {}. Эталон {}"
                        .format(self.sample_name, self.factor_name, self.std.name), 0)

        if doc.destination == 'doc':
            doc.add_heading("Список значений эталона", 1)
            doc.add_paragraph("Количество значений равно = {}".format(len(y)))
            doc.add_paragraph(str_arr(y))

            doc.add_heading("Список максимумов значений эталона:", 1)
            doc.add_paragraph("Количество значений равно = {}".format(len(y_seq_max)))
            doc.add_paragraph(str_arr(y_seq_max))

            doc.add_heading("Список максимумов амплитуд эталона:", 1)
            doc.add_paragraph("Количество амлитуд равно = {}".format(len_ampl(y_seq_max_apl)))
            doc.add_paragraph(str_arr(y_seq_max_apl))
            doc.add_paragraph('')

            doc.add_paragraph("Список значений фактор-образца {}:".format(self.factor_name))
            doc.add_paragraph("Количество значений равно = {}".format(len(x)))
            doc.add_paragraph(str_arr(x))

            doc.add_paragraph("Список максимумов значений фактор-образца {}:".format(self.factor_name))
            doc.add_paragraph("Количество значений равно = {}".format(len(x_seq_max)))
            doc.add_paragraph(str_arr(x_seq_max))
            doc.add_paragraph('')

            doc.add_heading("Последовательность расстояний от максимумов значений эталона "
                            "до максимумов фактор-образца {}".format(self.factor_name), 1)
            doc.add_paragraph(str_arr(self.distance))

            doc.add_heading("Последовательность расстояний от максимумов амплитуд значений эталона "
                            "до максимумов фактор-образца {}".format(self.factor_name), 1)
            doc.add_paragraph(str_arr(self.distance_apl))

        self.get_report_info(doc)
        self.get_report_info_apl(doc)

        if doc.destination == 'doc':
            doc.add_heading("Результат визуального анализа распределения расстояний значений эталона", 1)
            doc.add_picture(self.va)

            doc.add_heading("Результат визуального анализа распределения расстояний амплитуд эталона", 1)
            doc.add_picture(self.va_apl)

    def get_report_stat(self, doc: Printer):
        # TODO: Костыль 2, стоит от этого избавиться
        doc.add_heading("Фактор {}. Эталон {}".format(self.factor_name, self.std.name), 0)

        doc.add_heading("Результат статистического анализа распределения расстояний значений эталона", 1)
        report_stats(self.stat, doc)

    def get_report_ntest(self, doc: Printer):
        # TODO: Костыль 3, стоит от этого избавиться
        doc.add_heading("Фактор {}. Эталон {}".format(self.factor_name, self.std.name), 0)

        doc.add_heading("Результаты тестирования нормальности распределения расстояний значений эталона", 1)
        report_ntest(self.ntest, doc)

    def get_report_info(self, doc: Printer):
        self.get_report_stat(doc)
        self.get_report_ntest(doc)

    def get_report_stat_apl(self, doc: Printer):
        # TODO: Костыль 4, стоит от этого избавиться
        doc.add_heading("Фактор {}. Эталон {}".format(self.factor_name, self.std.name), 0)

        doc.add_heading("Результат статистического анализа распределения расстояний амплитуд эталона", 1)
        report_stats(self.stat_apl, doc)

    def get_report_ntest_apl(self, doc: Printer):
        # TODO: Костыль 5, стоит от этого избавиться
        doc.add_heading("Фактор {}. Эталон {}".format(self.factor_name, self.std.name), 0)

        doc.add_heading("Результаты тестирования нормальности распределения расстояний амплитуд эталона", 1)
        report_ntest(self.ntest_apl, doc)

    def get_report_info_apl(self, doc: Printer):
        self.get_report_stat_apl(doc)
        self.get_report_ntest_apl(doc)


class SampleStandard:
    def __init__(self, sample: Sample, std: Standard):
        self.sample = sample
        self.std = std

        self.distance = [sequence_distance_1(self.std.seq_max, seq_max) for seq_max in self.sample.seq_max]
        self.va = [plot_image(visual_analysis, xr) for xr in self.distance]
        self.ntest = [test_normal(xr, qq=False) for xr in self.distance]
        self.stat = [stat_analysis(xr) for xr in self.distance]

        self.distance_apl = [sequence_distance_1(self.std.seq_max_apl, seq_max0) for seq_max0 in self.sample.seq_max0]
        self.va_apl = [plot_image(visual_analysis, xr) for xr in self.distance_apl]
        self.ntest_apl = [test_normal(xr, qq=False) for xr in self.distance_apl]
        self.stat_apl = [stat_analysis(xr) for xr in self.distance_apl]

        self.sample_name = sample.display()

    def get_report(self, doc: Printer):
        doc.add_heading("{}. Эталон {}".format(self.sample_name, self.std.name), 0)

        doc.add_heading("Список значений эталона", 1)
        doc.add_paragraph("Количество значений равно = {}".format(len(self.std.data)))
        doc.add_paragraph(str_arr(self.std.data))

        doc.add_heading("Список максимумов эталона:", 1)
        doc.add_paragraph("Количество значений равно = {}".format(len(self.std.seq_max)))
        doc.add_paragraph(str_arr(self.std.seq_max))

        doc.add_heading("Список максимумов амплитуд эталона:", 1)
        doc.add_paragraph("Количество значений равно = {}".format(len_ampl(self.std.seq_max_apl)))
        doc.add_paragraph(str_arr(self.std.seq_max_apl))
        doc.add_paragraph('')

        for factor, y, y_seq_max in zip(range(4), self.sample.data, self.sample.seq_max):
            doc.add_paragraph("Список значений образца {}:".format(FACTORS[factor]))
            doc.add_paragraph("Количество значений равно = {}".format(len(y)))
            doc.add_paragraph(str_arr(y))

            doc.add_paragraph("Список максимумов значений образца {}:".format(FACTORS[factor]))
            doc.add_paragraph("Количество значений равно = {}".format(len(y_seq_max)))
            doc.add_paragraph(str_arr(y_seq_max))
            doc.add_paragraph('')

        doc.add_heading("Ряды расстояний и распределения расстояний от максимумов значений "
                        "и амплитуд эталона до ближайших максимумов образцов", 1)
        for factor, xr, xr_apl in zip(FACTORS, self.distance, self.distance_apl):
            doc.add_paragraph(
                "Ряд расстояний от максимумов значений эталона до ближайшего максимума образца {}:".format(
                    factor.lower()))
            doc.add_paragraph(str_arr(xr))

            doc.add_paragraph(
                "Ряд расстояний от максимумов амплитуд эталона до ближайшего максимума образца {}:".format(
                    factor.lower()))
            doc.add_paragraph(str_arr(xr_apl))
            doc.add_paragraph('')

        doc.add_heading("Результаты визуального анализа и тестирования нормальности", 1)
        for factor, va, ntest, va_apl, ntest_apl in zip(FACTORS, self.va, self.ntest, self.va_apl, self.ntest_apl):
            doc.add_paragraph("Результаты визуального анализа значений эталона для образца {}".format(factor.lower()))
            doc.add_picture(va)
            report_ntest(ntest, doc)

            doc.add_paragraph("Результаты визуального анализа амплитуд эталона для образца {}".format(factor.lower()))
            doc.add_picture(va_apl)
            report_ntest(ntest_apl, doc)

        doc.add_heading("Результаты статистического анализа распределения образца", 1)
        for factor, stat, stat_apl in zip(FACTORS, self.stat, self.stat_apl):
            doc.add_paragraph("Результаты статистического анализа распределения значений эталона для образца {}"
                              .format(factor.lower()))
            report_stats(stat, doc)

            doc.add_paragraph(
                "Результаты статистического анализа распределения амплитуд эталона для образца {}".format(
                    factor.lower()))
            report_stats(stat_apl, doc)
