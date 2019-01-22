from reports.utils import *

from science import plot_image, FACTORS_L
from science.funcs import *
from science.classes import Standard, Sample


class FactorSampleStandard:
    def __init__(self, sample: Sample, factor: int, std: Standard):
        self.sample = sample
        self.factor = factor
        self.std = std

        self.distance = sequence_distance_1(sample.seq_max[factor], std.seq_max)
        self.va = plot_image(visual_analysis, self.distance)
        self.ntest = test_normal(self.distance, qq=False)
        self.stat = stat_analysis(self.distance)

        self.sample_name = self.sample.display()
        self.factor_name = FACTORS_L[self.factor]

    def get_report(self, doc: Printer):
        doc.add_heading("{}, фактор {}. Эталон {}".format(self.sample_name, self.factor_name, self.std.name), 0)

        doc.add_heading("Последовательность расстояний от максимумов образца до ближайшего максимума эталона", 1)
        doc.add_paragraph(str_arr(self.distance))

        doc.add_heading("Результат статистического анализа распределения расстояний фактор-образца", 1)
        report_stats(self.stat, doc)

        doc.add_heading("Результаты тестирования нормальности распределения расстояний фактор-образца", 1)
        report_ntest(self.ntest, doc)

        doc.add_heading("Результат визуального анализа распределения расстояний фактор-образца", 1)
        doc.add_picture(self.va)

    def get_report_stat(self, doc: Printer):
        doc.add_heading("{}, фактор {}. Эталон {}".format(self.sample_name, self.factor_name, self.std.name), 0)
        doc.add_heading("Результат статистического анализа распределения расстояний значений эталона", 1)
        report_stats(self.stat, doc)

    def get_report_ntest(self, doc: Printer):
        doc.add_heading("{}, фактор {}. Эталон {}".format(self.sample_name, self.factor_name, self.std.name), 0)
        doc.add_heading("Результаты тестирования нормальности распределения расстояний значений эталона", 1)
        report_ntest(self.ntest, doc)


class SampleStandard:
    def __init__(self, sample: Sample, std: Standard):
        self.sample = sample
        self.std = std

        self.distance = [sequence_distance_1(seq_max, std.seq_max) for seq_max in sample.seq_max]
        self.kde = plot_image(graph_kde, self.distance)
        self.va = [plot_image(visual_analysis, xr) for xr in self.distance]
        self.ntest = [test_normal(xr, qq=False) for xr in self.distance]
        self.stat = [stat_analysis(xr) for xr in self.distance]

        self.distance3 = [sequence_distance_1(sample.seq_max[factor], sample.seq_max[0]) for factor in range(1, 4)]
        self.kde3 = plot_image(graph_kde3, self.distance3)
        self.stat3 = [stat_analysis(xr) for xr in self.distance3]
        self.ntest3 = [test_normal(xr, qq=False) for xr in self.distance3]

        self.sample_name = self.sample.display()

    def get_report(self, doc: Printer):
        doc.add_heading("{}. Эталон {}".format(self.sample_name, self.std.name), 0)

        doc.add_heading("Ряды расстояний и распределения расстояний от максимумов образца до ближайшего максимума "
                        "эталона", 1)
        for factor, xr in zip(FACTORS_L, self.distance):
            doc.add_paragraph("Ряд расстояний от максимумов образца {} до ближайшего максимума эталона:".format(factor))
            doc.add_paragraph(str_arr(xr))

        doc.add_heading("Кривая Гаусса и 4-х ядерных оценок плотности 4-х фактор-образцов", 1)
        doc.add_picture(self.kde)

        doc.add_heading("Результаты визуального анализа", 1)
        for factor, va, in zip(FACTORS_L, self.va):
            doc.add_heading("Результаты визуального анализа образца {}".format(factor), 2)
            doc.add_picture(va)

        doc.add_heading("Результаты тестирования нормальности", 1)
        for factor, ntest in zip(FACTORS_L, self.ntest):
            doc.add_heading("Результаты тестирования нормальности образца {}".format(factor), 2)
            report_ntest(ntest, doc)

        doc.add_heading("Результаты статистического анализа распределения расстояний для образца", 1)
        for factor, stat in zip(FACTORS_L, self.stat):
            doc.add_heading("Результаты статистического анализа распределения расстояний образца {}"
                            .format(factor), 2)
            report_stats(stat, doc)

        doc.add_heading("Ядерные оценки плотности и кривая Гаусса для сравнения распределения расстояний "
                        "от фактор-образцов (с физической нагрузкой, после отдыха, с эмоциональной нагрузкой) до "
                        "исходного стандарта – фактор-образца без нагрузки", 1)
        doc.add_picture(self.kde3)

        self.get_report_stat3(doc)
        self.get_report_ntest3(doc)

    def get_report_stat3(self, doc: Printer):
        doc.add_heading("Результаты статистического анализа распределения расстояний от фактор-образцов "
                        "(с физической нагрузкой, после отдыха, с эмоциональной нагрузкой) до исходного стандарта – "
                        "фактор-образца без нагрузки", 1)
        for factor, stat in zip(FACTORS_L, self.stat3):
            doc.add_heading("Результаты статистического группового анализа распределения расстояний от фактора {}"
                            .format(factor), 2)
            report_stats(stat, doc)

    def get_report_ntest3(self, doc: Printer):
        doc.add_heading("Тестирование нормальности распределения расстояний от фактор-образцов "
                        "(с физической нагрузкой, после отдыха, с эмоциональной нагрузкой) до исходного стандарта – "
                        "фактор-образца без нагрузки", 1)
        for factor, ntest in zip(FACTORS_L, self.ntest3):
            doc.add_heading("Тестирование нормальности распределения расстояний от фактора {}"
                            .format(factor), 2)
            report_ntest(ntest, doc)
