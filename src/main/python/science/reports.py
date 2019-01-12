from science import plot_image, Printer, FACTORS
from science.funcs import *
from science.classes import Sample, Standard
from science.test_normal import *


class FactorSampleStandard:
    def __init__(self, sample: Sample, factor: int, std: Standard):
        self.sample = sample
        self.factor = factor
        self.std = std

        self.distance = sequence_distance(sample.seq_max[factor], std.seq_max)
        self.va = plot_image(visual_analysis, self.distance)
        self.ntest = test_normal(self.distance, qq=False)
        self.stat = stat_analysis(self.distance)

    def get_report(self, doc: Printer):
        factor_name = FACTORS[self.factor]
        x, x_seq_max = self.sample.data[self.factor], self.sample.seq_max[self.factor]
        y, y_seq_max = self.std.data, self.std.seq_max

        doc.add_heading("Образец {}, фактор {}. Эталон {}"
                        .format(self.sample.name, factor_name, self.std.name), 0)

        if doc.destination == 'docx':
            doc.add_heading("Список значений эталона", 1)
            doc.add_paragraph("Количество значений равно = {}".format(len(y)))
            doc.add_paragraph(str(y))
            doc.add_heading("Список максимумов эталона:", 1)
            doc.add_paragraph("Количество значений равно = {}".format(len(y_seq_max)))
            doc.add_paragraph(str(y_seq_max))

            doc.add_paragraph("Список значений образца:")
            doc.add_paragraph("Количество значений равно = {}".format(len(x)))
            doc.add_paragraph(str(x))

            doc.add_paragraph("Список максимумов значений образца:")
            doc.add_paragraph("Количество значений равно = {}".format(len(x_seq_max)))
            doc.add_paragraph(str(x))
            doc.add_paragraph('')

            doc.add_heading("Последовательность расстояний от максимумов образца до ближайшего максимума эталона", 1)
            doc.add_paragraph(str(self.distance))

        doc.add_heading("Результат статистического анализа распределения расстояний фактор-образца", 1)
        doc.add_paragraph("\tВыборочное среднее = {:.3f}".format(self.stat[0]))
        doc.add_paragraph("\tСтандартное отклонение = {:.3f}".format(self.stat[1]))
        doc.add_paragraph("\tДоверительный интервал = ({:.3f}, {:.3f})".format(*self.stat[2]))

        doc.add_heading("Результаты тестирования нлрмальности распределения расстояний фактор-образца", 1)
        get_report(self.ntest, doc)

        if doc.destination == 'docx':
            doc.add_heading("Результат визуального анализа распределения расстояний фактор-образца", 1)
            doc.add_picture(self.va)


class SampleStandard:
    def __init__(self, sample: Sample, std: Standard):
        self.sample = sample
        self.std = std

        self.distance = [sequence_distance(sample.seq_max[factor], std.seq_max) for factor in range(4)]
        self.kde = plot_image(graph_kde, self.distance)
        self.va = [plot_image(visual_analysis, xr) for xr in self.distance]
        self.ntest = [test_normal(xr, qq=False) for xr in self.distance]
        self.stat = [stat_analysis(xr) for xr in self.distance]

        self.distance3 = [sequence_distance_1(sample.seq_max[factor], sample.seq_max[0]) for factor in range(1, 4)]
        self.kde3 = plot_image(graph_kde3, self.distance3)
        self.stat3 = [stat_analysis(xr) for xr in self.distance3]
        self.ntest3 = [test_normal(xr, qq=False) for xr in self.distance3]

    def get_report(self):
        """
print("Построение кривой Гаусса и 4-х ядерных оценок плотности 4-х фактор-образцов для первого пациента и первого эталона")
graph_kde(sequence_distance(sequence_max(sample[0]), sequence_max(standart[0])), sequence_distance(sequence_max(sample_n[0]), sequence_max(standart[0])), sequence_distance(sequence_max(sample_o[0]), sequence_max(standart[0])), sequence_distance(sequence_max(sample_e[0]), sequence_max(standart[0])))

print("Результаты  визуального анализа и тестирования нормальности для фактор-образца без нагрузки для всех пациентов и всех эталонов")

for i in range(n_standart):
    for j in range(n_sample): print("Результаты визуального анализа распределения фактор-образца без нагрузки пациента", j, "для эталона ", i, "\n",visual_analysis(sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))))
    for j in range(n_sample): print("Результаты тестирования нормальности распределения фактор-образца без нагрузки пациента", j, "для эталона ", i, "\n", test_normal(sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))))


print("Результаты статистического  анализа распределения фактор-образца без нагрузки  для всех пациентов и всех эталонов")

for i in range(n_standart):
    for j in range(n_sample): print("Результаты статистического о анализа распределения фактор-образца без нагрузки пациента", j, "для эталона ", i, "\n", "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] =  ", "\n", stat_analys(sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))))

print("Построение 3-х ядерных оценок плотности и кривой Гаусса для сравнения распределения расстояний от фактор-образцов (с физ.нагрузкой, после отдыха, с эмоц.нагрузкой) до исходного стандарта - фактор-образца (без нагрузки) для первого образца")

graph_kde3(sequence_distance1(sequence_max(sample_n[0]), sequence_max(sample[0])), sequence_distance1(sequence_max(sample_o[0]), sequence_max(sample[0])), sequence_distance1(sequence_max(sample_e[0]), sequence_max(sample[0])))

print("Результаты статистического группового анализа распределения расстояний от фактор-образцов (с физ.нагрузкой, после отдыха, с эмоц.нагрузкой) до исходного стандарта - фактор-образца (без нагрузки)  для первого образца")

print("С физической нагрузкой - без нагрузки: [Выборочное среднее, Стандартное отклонение,  Доверительный интервал] = ", "\n", stat_analys(sequence_distance1(sequence_max(sample_n[0]), sequence_max(sample[0]))), "\n", "После отдыха - без нагрузки: [Выборочное среднее, Стандартное отклонение,  Доверительный интервал] = ", "\n", stat_analys(sequence_distance1(sequence_max(sample_o[0]), sequence_max(sample[0]))), "\n", "С эмоциональной нагрузкой - без нагрузки: [Выборочное среднее, Стандартное отклонение,  Доверительный интервал] = ", "\n", stat_analys(sequence_distance1(sequence_max(sample_e[0]), sequence_max(sample[0]))))

"Результаты статистического анализа распределения расстояний от фактор-образцов (с физ.нагрузкой, после отдыха, с эмоц.нагрузкой) до исходного стандарта - фактор-образца (без нагрузки)   для всех образцов"

for i in range(len(sample)):
    print("С физической нагрузкой - без нагрузки образца ", i, "\n", "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] = ", "\n", stat_analys(sequence_distance1(sequence_max(sample_n[i]), sequence_max(sample[i]))), "\n", "После отдыха - без нагрузки образца ", i, "\n", " [Выборочное среднее, Стандартное отклонение,  Доверительный интервал] = ", "\n", stat_analys(sequence_distance1(sequence_max(sample_o[i]), sequence_max(sample[i]))), "\n", "С эмоциональной нагрузкой - без нагрузки образца ", i, "\n", " [Выборочное среднее, Стандартное отклонение,  Доверительный интервал] = ", "\n", stat_analys(sequence_distance1(sequence_max(sample_e[i]), sequence_max(sample[i]))))

"Тестирование нормальности распределения расстояний от факторов (с физ.нагрузкой, после отдыха, с эмоц.нагрузкой) до исходного стандарта - фактор-образца (без нагрузки) для всех образцов"

for i in range(len(sample)):
    print("Результаты тестирования нормальности распределения с физической нагрузкой - без нагрузки образца", i)
    print(test_normal(sequence_distance1(sequence_max(sample_n[0]), sequence_max(sample[0]))))
    print("Результаты тестирования нормальности распределения после отдыха - без нагрузки образца", i)
    print(test_normal(sequence_distance1(sequence_max(sample_o[0]), sequence_max(sample[0]))))
    print("Результаты тестирования нормальности распределения с эмоциональной нагрузкой - без нагрузки образца", i)
    print(test_normal(sequence_distance1(sequence_max(sample_e[0]), sequence_max(sample[0]))))

        """


class MulSamplesStandard:
    def __init__(self, samples: list, std: Standard):
        self.samples = samples[:]
        self.std = std

        self.distance = [[sequence_distance(sample.seq_max[factor], std.seq_max) for factor in range(4)]
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

    def get_report(self):
        """
print("Распределение средних значений пациентов без нагрузки для всех образцов и всех эталонов")

max_sample_list = []
for i in range(n_standart):
    m_list = []
    for j in range(len(sample)): m_list.append(np.mean(sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))))
    max_sample_list.append(m_list)
#print("Распределение средних значений пациентов без нагрузки для всех эталонов", "\n", max_sample_list)

print("Результаты  визуального  анализа распределений средних значений фактор-образца без нагрузки для всех эталонов")

for i in range(n_standart): print("Результаты визуального анализа распределения средних значений фактор-образца без нагрузки для эталона ", i, "\n", visual_analysis1(max_sample_list[i]))

print("Результаты  тестирования нормальности распределений средних значений фактор-образца без нагрузки для всех эталонов")

for i in range(n_standart): test_normal(max_sample_list[i])

print("Результаты статистического анализа  распределений средних значений фактор-образца без нагрузки для всех эталонов")

for i in range(n_standart): print("Результаты визуального анализа распределения средних значений фактор-образца без нагрузки для эталона ", i, "\n", "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] =  ", "\n", stat_analys(max_sample_list[i]))
        """


class FactorSampleMulStandards:
    def __init__(self, sample: Sample, factor: int, stds: list):
        self.sample = sample
        self.factor = factor
        self.stds = stds[:]

        self.distance = [sequence_distance(self.sample.seq_max[factor], std.seq_max) for std in stds]
        self.va = [plot_image(visual_analysis, xr) for xr in self.distance]
        self.ntest = [test_normal(xr, qq=False) for xr in self.distance]
        self.stat = [stat_analysis(xr) for xr in self.distance]

    def get_report(self):
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

print("Результаты тестирования нлрмальности распределения расстояний фактор-образца без нагрузки для всех образцов и всех эталонов")

for i in range(n_standart):
    for j in range(len(sample)): print("Результаты тестирования нормальности распределения расстояний фактор-образца без нагрузки для образца  ", j, "  и эталона  ", i, "\n",
	test_normal(sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))))

print("Результаты статистического анализа распределения расстояний фактор-образца без нагрузки для всех образцов и всех эталонов")

for i in range(n_standart):
    for j in range(len(sample)): print("Результат статистическогоанализа распределения расстояний фактор-образца без нагрузки для образца  ", j, "  и эталона  ", i, "\n",  "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] =  ", "\n" , stat_analys(sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))))

        """


class SampleMulStandards:
    def __init__(self, sample: Sample, stds: list):
        self.sample = sample
        self.stds = stds[:]

        self.distance = [[sequence_distance(sample.seq_max[factor], std.seq_max) for factor in range(4)]
                         for std in stds]
        self.va = [[plot_image(visual_analysis, xr[factor]) for factor in range(4)] for xr in self.distance]
        self.ntest = [[test_normal(xr[factor], qq=False) for factor in range(4)] for xr in self.distance]
        self.stat = [[stat_analysis(xr[factor]) for factor in range(4)] for xr in self.distance]

    def get_report(self):
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

print("Результаты тестирования нлрмальности распределения расстояний фактор-образца без нагрузки для всех образцов и всех эталонов")

for i in range(n_standart):
    for j in range(len(sample)): print("Результаты тестирования нормальности распределения расстояний фактор-образца без нагрузки для образца  ", j, "  и эталона  ", i, "\n",
    test_normal(sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))))

print("Результаты статистического анализа распределения расстояний фактор-образца без нагрузки для всех образцов и всех эталонов")

for i in range(n_standart):
    for j in range(len(sample)): print("Результат статистическогоанализа распределения расстояний фактор-образца без нагрузки для образца  ", j, "  и эталона  ", i, "\n",  "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] =  ", "\n" , stat_analys(sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))))

        """


class MulSamplesMulStandards:
    def __init__(self, samples: list, stds: list):
        self.samples = samples[:]
        self.stds = stds[:]

        self.distance = [[[sequence_distance(factor, std.seq_max) for factor in sample.seq_max]
                          for sample in samples] for std in stds]
        self.va = [[[plot_image(visual_analysis, factor) for factor in sample] for sample in xr]
                   for xr in self.distance]
        self.ntest = [[[test_normal(factor, qq=False) for factor in sample] for sample in xr] for xr in self.distance]
        self.stat = [[[stat_analysis(factor) for factor in sample] for sample in xr] for xr in self.distance]

    def get_report(self):
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

print("Результаты тестирования нлрмальности распределения расстояний фактор-образца без нагрузки для всех образцов и всех эталонов")

for i in range(n_standart):
    for j in range(len(sample)): print("Результаты тестирования нормальности распределения расстояний фактор-образца без нагрузки для образца  ", j, "  и эталона  ", i, "\n",
    test_normal(sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))))

print("Результаты статистического анализа распределения расстояний фактор-образца без нагрузки для всех образцов и всех эталонов")

for i in range(n_standart):
    for j in range(len(sample)): print("Результат статистическогоанализа распределения расстояний фактор-образца без нагрузки для образца  ", j, "  и эталона  ", i, "\n",  "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] =  ", "\n" , stat_analys(sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))))

        """


if __name__ == '__main__':
    # тест всех отчетов
    import os

    for group in '123':
        for idx in '123456':
            Sample.from_file('samples/{}_{}.xlsx'.format(group, idx))
    _samples = list(Sample.samples.values())

    for entry in os.listdir('samples'):
        if entry[-4:] == '.txt':
            Standard.from_file('samples/' + entry)
    _stds = list(Standard.standards.values())

    s1 = _samples[0]
    std1 = _stds[0]

    FactorSampleStandard(s1, 0, std1)
    SampleStandard(s1, std1)
    MulSamplesStandard(_samples, std1)
    FactorSampleMulStandards(s1, 0, _stds)
    SampleMulStandards(s1, _stds)
    MulSamplesMulStandards(_samples, _stds)
