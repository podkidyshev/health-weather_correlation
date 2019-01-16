from reports import *

from science import plot_image, FACTORS
from science.funcs import *
from science.classes import Standard, Sample


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

        doc.add_heading("Образец {}, фактор-образец {}".format(self.sample_name, FACTORS[self.factor]), 1)
        doc.add_paragraph("Количество значений равно = {}".format(len(self.sample.data[self.factor])))
        doc.add_paragraph(str(self.sample.data[self.factor]))
        doc.add_paragraph("Количество максимумов равно = {}".format(len(self.sample.seq_max[self.factor])))
        doc.add_paragraph(str(self.sample.seq_max[self.factor]))

        doc.add_heading("Отчеты по эталонам", 1)
        for idx, std in enumerate(self.stds):
            doc.add_heading("Эталон {}".format(std.name), 2)
            doc.add_paragraph("Количество значений равно = {}".format(len(std.data)))
            doc.add_paragraph(str(std.data))
            doc.add_paragraph("Количество максимумов равно = {}".format(len(std.seq_max)))
            doc.add_paragraph(str(std.seq_max))

            doc.add_paragraph("Последовательность расстояний для эталона {}. Количество значений равно = {}"
                              .format(std.name, len(self.distance[idx])))
            doc.add_paragraph(str(self.distance[idx]))
            doc.add_heading("\nРезультаты визуального анализа распределения расстояний для эталона {}"
                            .format(std.name), 2)
            doc.add_picture(self.va[idx])
            doc.add_heading("\nРезультаты тестирования нормальности распределения расстояний для эталона {}"
                            .format(std.name), 2)
            ntest_report(self.ntest[idx], doc)
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

        for factor in range(4):
            doc.add_heading("Фактор {}".format(FACTORS[factor]), 2)
            doc.add_paragraph("Количество значений равно = {}".format(len(self.sample.data[factor])))
            doc.add_paragraph(str(self.sample.data[factor]))
            doc.add_paragraph("Количество максимумов равно = {}".format(len(self.sample.seq_max[factor])))
            doc.add_paragraph(str(self.sample.seq_max[factor]))

        doc.add_heading("Отчеты по эталонам", 1)
        for idx, std in enumerate(self.stds):
            doc.add_heading("Эталон {}".format(std.name), 2)
            doc.add_paragraph("Количество значений равно = {}".format(len(std.data)))
            doc.add_paragraph(str(std.data))
            doc.add_paragraph("Количество максимумов равно = {}".format(len(std.seq_max)))
            doc.add_paragraph(str(std.seq_max))

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
                ntest_report(self.ntest[idx][factor], doc)
                doc.add_heading("\nРезультаты статистического анализа распределения расстояний "
                                "фактор-образца {} и эталона {}".format(FACTORS[factor], std.name), 2)
                doc.add_paragraph("\tВыборочное среднее = {:.4f}".format(self.stat[idx][factor][0]))
                doc.add_paragraph("\tСтандартное отклонение = {:.4f}".format(self.stat[idx][factor][1]))
                doc.add_paragraph("\tДоверительный интервал = ({:.4f}, {:.4f})".format(*self.stat[idx][factor][2]))


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

        self.max_graph_kde = plot_image(graph_kde, self.max_list)
        self.max_va = [plot_image(visual_analysis, xr) for xr in self.max_list]
        self.max_list_ntest = [test_normal(max_list_factor, qq=False) for max_list_factor in self.max_list]
        self.stat = [stat_analysis(max_list_factor) for max_list_factor in self.max_list]

    def get_report(self, doc: Printer):
        doc.add_heading("Группа образцов. Эталон {}".format(self.std.name), 0)

        doc.add_heading("Эталон {}".format(self.std.name), 1)
        doc.add_paragraph("Количество значений равно = {}".format(len(self.std.data)))
        doc.add_paragraph(str(self.std.data))
        doc.add_paragraph("Количество максимумов равно = {}".format(len(self.std.seq_max)))
        doc.add_paragraph(str(self.std.seq_max))

        for sample in self.samples:
            doc.add_heading("Образец {}".format(sample.name), 1)
            for factor in range(4):
                doc.add_heading("Фактор-образец {}".format(FACTORS[factor]), 2)
                doc.add_paragraph("Количество значений равно = {}".format(len(sample.data[factor])))
                doc.add_paragraph(str(sample.data))
                doc.add_paragraph("Количество максимумов равно = {}".format(len(sample.seq_max[factor])))
                doc.add_paragraph(str(sample.seq_max[factor]))

        doc.add_heading("Результаты визуального анализа распределений средних значений образцов по всем факторам", 1)
        doc.add_picture(self.max_graph_kde)

        for factor in range(4):
            factor_name = FACTORS[factor].lower()
            doc.add_heading("Для фактора {}".format(factor_name), 1)
            doc.add_heading("Распределение средних значений образцов {}".format(factor_name), 2)
            doc.add_paragraph(str(self.max_list[factor]))
            doc.add_heading("Результаты  визуального  анализа распределений средних значений фактор-образцов {}"
                            .format(factor_name), 2)
            doc.add_picture(self.max_va[factor])
            doc.add_heading("Результаты тестирования нормальности распределений средних значений фактор-образцов {}"
                            .format(factor_name), 2)
            ntest_report(self.max_list_ntest[factor], doc)
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
        self.va = [[[plot_image(visual_analysis, factor) for factor in sample] for sample in xr]
                   for xr in self.distance]
        self.ntest = [[[test_normal(factor, qq=False) for factor in sample] for sample in xr] for xr in self.distance]
        self.stat = [[[stat_analysis(factor) for factor in sample] for sample in xr] for xr in self.distance]

    def get_report(self, doc: Printer):
        """
print("Распределения максимумов и расстояний фактор-образца без нагрузки для всех образцов и всех эталонов")

for i in range(n_standart):
    for j in range(len(sample)):
        print("Последовательность максимумов образца  ", j, "  и эталона  ", i, sequence_max(sample[j]), len_ampl(sequence_max(sample[j])))
        print("Последовательность расстояний для образца  ", j, "  и эталона  ", i, sequence_distance(sequence_max(sample[j]), sequence_max(standart[i])), len(sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))))

print("Результаты визуального анализа распределения расстояний фактор-образца без нагрузки для всех образцов и всех эталонов")

for i in range(n_standart):
    for j in range(len(sample)):
        print("Результаты визуального анализа распределения расстояний фактор-образца без нагрузки для образца  ", j, "  и эталона  ", i, visual_analysis(sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))))

print("Результаты тестирования нормальности распределения расстояний фактор-образца без нагрузки для всех образцов и всех эталонов")

for i in range(n_standart):
    for j in range(len(sample)): print("Результаты тестирования нормальности распределения расстояний фактор-образца без нагрузки для образца  ", j, "  и эталона  ", i, "\n",
    test_normal(sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))))

print("Результаты статистического анализа распределения расстояний фактор-образца без нагрузки для всех образцов и всех эталонов")

for i in range(n_standart):
    for j in range(len(sample)): print("Результат статистическогоанализа распределения расстояний фактор-образца без нагрузки для образца  ", j, "  и эталона  ", i, "\n",  "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] =  ", "\n" , stat_analys(sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))))

        """
