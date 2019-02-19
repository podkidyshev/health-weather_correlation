# Ведущий ряд - образец
# Писать в заголовке ведущий ряд - ведомый ряд
from reports import Printer, str_arr, report_error
from reports.utils import report_ntest, report_stats

from science import plot_image, FACTORS, FACTORS_L
from science.funcs import *
from science.classes import Standard, Sample


class FactorSampleStandard:
    @report_error("init")
    def __init__(self, sample: Sample, factor: int, std: Standard):
        self.sample = sample
        self.factor = factor
        self.std = std

        self.distance = sequence_distance_1(self.std.seq_max0, self.sample.seq_max0[factor])
        self.va = plot_image(visual_analysis, self.distance)
        self.stat = stat_analysis(self.distance)
        self.ntest = test_normal(self.distance, qq=True)

        self.distance_apl = sequence_distance_1(self.std.seq_max_apl, self.sample.seq_max0[factor])
        self.va_apl = plot_image(visual_analysis, self.distance_apl)
        self.stat_apl = stat_analysis(self.distance_apl)
        self.ntest_apl = test_normal(self.distance_apl, qq=True)

        self.sample_name = self.sample.display()
        self.factor_name = FACTORS_L[self.factor]

    @report_error("doc")
    def get_report(self, doc: Printer):
        doc.add_heading("{} {}. Эталон {}".format(self.sample_name, self.factor_name, self.std.name), 0)

        # Значения
        doc.add_heading("Последовательность расстояний от максимумов значений эталона до максимумов фактор-образца", 1)
        doc.add_paragraph(str_arr(self.distance))

        doc.add_heading("Результат визуального анализа распределения расстояний от максимумов значений эталона", 1)
        doc.add_picture(self.va)

        doc.add_heading("Результат статистического анализа распределения расстояний от максимумов значений эталона", 1)
        report_stats(self.stat, doc)

        doc.add_heading("Результаты тестирования нормальности распределения расстояний от максимумов значений эталона",
                        1)
        report_ntest(self.ntest, doc)

        # Амплитуды
        doc.add_heading(
            "Последовательность расстояний от максимумов амплитуд значений эталона до максимумов фактор-образца", 1)
        doc.add_paragraph(str_arr(self.distance_apl))

        doc.add_heading(
            "Результат визуального анализа распределения расстояний от максимумов амплитуд значений эталона", 1)
        doc.add_picture(self.va_apl)

        doc.add_heading(
            "Результат статистического анализа распределения расстояний от максимумов амплитуд значений эталона", 1)
        report_stats(self.stat_apl, doc)

        doc.add_heading(
            "Результаты тестирования нормальности распределения расстояний от максимумов амплитуд значений эталона", 1)
        report_ntest(self.ntest_apl, doc)

    @report_error("ui")
    def get_report_stat(self, doc: Printer):
        doc.add_heading("Фактор {}. Эталон {}".format(self.factor_name, self.std.name), 0)
        doc.add_heading("Результат статистического анализа распределения расстояний от максимумов значений эталона", 1)
        report_stats(self.stat, doc)

    @report_error("ui")
    def get_report_ntest(self, doc: Printer):
        doc.add_heading("Фактор {}. Эталон {}".format(self.factor_name, self.std.name), 0)
        doc.add_heading("Результаты тестирования нормальности распределения расстояний от максимумов значений эталона",
                        1)
        report_ntest(self.ntest, doc)

    @report_error("ui")
    def get_report_stat_apl(self, doc: Printer):
        doc.add_heading("Фактор {}. Эталон {}".format(self.factor_name, self.std.name), 0)
        doc.add_heading(
            "Результат статистического анализа распределения расстояний от максимумов амплитуд значений эталона", 1)
        report_stats(self.stat_apl, doc)

    @report_error("ui")
    def get_report_ntest_apl(self, doc: Printer):
        doc.add_heading("Фактор {}. Эталон {}".format(self.factor_name, self.std.name), 0)
        doc.add_heading(
            "Результаты тестирования нормальности распределения расстояний от максимумов амплитуд значений эталона", 1)
        report_ntest(self.ntest_apl, doc)


class SampleStandard:
    @report_error("init")
    def __init__(self, sample: Sample, std: Standard):
        self.sample = sample
        self.std = std

        self.distance = [sequence_distance_1(self.std.seq_max0, seq_max0) for seq_max0 in self.sample.seq_max0]
        self.va = [plot_image(visual_analysis, xr) for xr in self.distance]
        self.stat = [stat_analysis(xr) for xr in self.distance]
        self.ntest = [test_normal(xr, qq=True) for xr in self.distance]

        self.distance_apl = [sequence_distance_1(self.std.seq_max_apl, seq_max0) for seq_max0 in self.sample.seq_max0]
        self.va_apl = [plot_image(visual_analysis, xr) for xr in self.distance_apl]
        self.stat_apl = [stat_analysis(xr) for xr in self.distance_apl]
        self.ntest_apl = [test_normal(xr, qq=True) for xr in self.distance_apl]

        self.sample_name = self.sample.display()

    @report_error("doc")
    def get_report(self, doc: Printer):
        doc.add_heading("{}. Эталон {}".format(self.sample_name, self.std.name), 0)

        # Значения
        doc.add_heading("Ряды расстояний и распределения расстояний от максимумов значений эталона до ближайшего "
                        "максимума образца", 1)
        for factor, xr in zip(FACTORS_L, self.distance):
            doc.add_paragraph(
                "Ряд расстояний от максимумов значений эталона до ближайшего максимума фактор-образца {}:".format(factor))
            doc.add_paragraph(str_arr(xr))

        doc.add_heading("Результат визуального анализа распределения расстояний от максимумов значений эталона", 1)
        for factor, va in zip(FACTORS_L, self.va):
            doc.add_heading("Результаты визуального анализа до ближайшего максимума фактор-образца {}".format(factor), 2)
            doc.add_picture(va)

        doc.add_heading("Результаты статистического анализа распределения расстояний от максимумов значений эталона", 1)
        for factor, stat in zip(FACTORS_L, self.stat):
            doc.add_heading(
                "Результаты статистического анализа до ближайшего максимума фактор-образца {}".format(factor), 2)
            report_stats(stat, doc)

        doc.add_heading("Результаты тестирования нормальности распределения расстояний от максимумов значений эталона", 1)
        for factor, ntest in zip(FACTORS_L, self.ntest):
            doc.add_heading("Результаты тестирования нормальности до ближайшего максимума фактор-образца {}".format(factor), 2)
            report_ntest(ntest, doc)

        # Амплитуды
        doc.add_heading("Ряды расстояний и распределения расстояний от максимумов амплитуд значений эталона до "
            "ближайшего максимума образца", 1)
        for factor, xr in zip(FACTORS_L, self.distance_apl):
            doc.add_paragraph(
                "Ряд расстояний от максимумов амплитуд значений эталона до ближайшего максимума фактор-образца {}:".format(factor))
            doc.add_paragraph(str_arr(xr))

        doc.add_heading("Результат визуального анализа распределения расстояний от максимумов амплитуд значений эталона", 1)
        for factor, va_apl in zip(FACTORS_L, self.va_apl):
            doc.add_heading("Результаты визуального анализа до ближайшего максимума фактор-образца {}".format(factor),
                            2)
            doc.add_picture(va_apl)

        doc.add_heading("Результаты статистического анализа распределения расстояний от максимумов амплитуд значений эталона", 1)
        for factor, stat_apl in zip(FACTORS_L, self.stat_apl):
            doc.add_heading("Результаты статистического анализа до ближайшего максимума фактор-образца {}".format(factor), 2)
            report_stats(stat_apl, doc)

            doc.add_heading(
                "Результаты тестирования нормальности распределения расстояний от максимумов амплитуд значений эталона", 1)
        for factor, ntest_apl in zip(FACTORS_L, self.ntest_apl):
            doc.add_heading("Результаты тестирования нормальности до ближайшего максимума фактор-образца {}".format(factor), 2)
            report_ntest(ntest_apl, doc)
