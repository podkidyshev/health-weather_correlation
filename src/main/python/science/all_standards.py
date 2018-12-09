import numpy as np
import scipy.stats as stats
from matplotlib.figure import Figure

import science
import science.test_normal as tn
import science.funcs as funcs
import science.classes as classes


class AllStandards:
    def __init__(self, samples: list, cat: str):
        """
        Анализ по всем эталонам и переданным пациентам в категории cat
        :param samples:
        :param cat:
        """
        cat_index = science.cat_index(cat)
        cat_short = science.CATS[cat_index][0]
        cat_full = science.CATS[cat_index][1]

        error_samples = []
        for sample in samples:
            if not sample.has_category(cat):
                error_samples.append(sample.name)
        if len(error_samples):
            raise funcs.StatComputingError('Запрошена обработка категории "{}".\n '
                                           'У пациентов {} нет данных в этой категории'.format(cat_full, error_samples))

        self.cat_name = cat
        self.cat = cat_index

        self.stds = [std for std in classes.Standard.standards.values()]
        self.stds_count = len(self.stds)
        self.stds_data = [std.data for std in self.stds]
        self.stds_seq_max = [std.seq_max for std in self.stds]

        self.samples = samples[:]
        self.samples_count = len(self.samples)
        self.samples_data = [pat.data[self.cat] for pat in self.samples]
        self.samples_seq_max = [pat.data_seq_max[self.cat] for pat in self.samples]

        self.samples_data_all = funcs.sum_list(self.samples_data)
        self.samples_seq_max_all = funcs.sequence_max(self.samples_data_all)

        self.distances = [[funcs.sequence_distance(sample_seq_max, std_seq_max, insert_zero=True)
                           for sample_seq_max in self.samples_seq_max]
                          for std_seq_max in self.stds_seq_max]

        self.k = sum(map(lambda sm: sum(sm), self.samples_seq_max))
        self.concats = [funcs.sum_list(self.distances[i]) for i in range(self.stds_count)]
        self.tn_by_day = [tn.test_normal(funcs.sequence_distance(self.samples_seq_max_all,
                                                                 std_seq_max,
                                                                 insert_zero=True),
                                         qq=False)
                          for std_seq_max in self.stds_seq_max]
        self.tn_by_sample = [tn.test_normal(concat, qq=False) for concat in self.concats]

    def get_report(self):
        print("Число эталонов:", len(self.stds_data), "\n", "Список значений эталонов:", "\n", self.stds_data)

        for idx, std_seq_max in enumerate(self.stds_seq_max):
            print("Список максимумов значений эталона", self.stds[idx].name, "\n", std_seq_max,
                  "Всего максимумов:", np.sum(std_seq_max))

        print("Число образцов:", len(self.samples))

        print("Распределения максимумов и расстояний по пациентам для всех эталонов")
        for std_num, std_seq_max in enumerate(self.stds_seq_max):
            for sample_num, sample_seq_max in enumerate(self.samples_seq_max):
                print("Последовательность максимумов образца", self.samples[std_num].name,
                      "и эталона", self.stds[std_num].name,
                      std_seq_max, np.sum(std_seq_max))
                print("Последовательность расстояний для образца", self.samples[std_num].name,
                      "и эталона", self.stds[std_num].name,
                      self.distances[std_num][sample_num],
                      len(self.distances[std_num][sample_num]))

        print("k =", self.k)
        for std_num, concat in enumerate(self.concats):
            print("Распределение расстояний группы пациентов для эталона ", self.stds[sample_num].name,
                  concat, "Всего значений =", len(concat))

        print("Результаты сравнительного визуального анализа по дням и по пациентам всех образцов со всеми эталонами")
        for std_num in range(self.stds_count):
            print("Результаты визуального анализа для группового образца по дням и по пациентам для эталона",
                  self.stds[std_num].name, "\n")
            # TODO: здесь self.stds_count графиков
            # base = plt.figure(figsize=(5, 4), dpi=100)
            # funcs.visual_analysis2(funcs.sequence_distance(funcs.sequence_max(funcs.sum_list(self.samples_data)),
            #                                                self.stds_seq_max[std_num], insert_zero=True),
            #                      self.concats[std_num], base)
            print("Результаты тестирования нормальности распределения группового образца по дням для эталона ",
                  self.stds[sample_num].name, "\n")
            tn.get_report(self.tn_by_day[std_num])

            print("Результаты тестирования нормальности распределения группового образца по пациентам для эталона",
                  self.stds[sample_num].name, "\n")
            tn.get_report(self.tn_by_sample[std_num])

        for std_num in range(self.stds_count):
            print("Результаты группового анализа по дням для эталона", self.stds[std_num].name, "\n",
                  "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] =", "\n",
                  funcs.stat_analysis_distances(self.samples_data_all, self.stds_data[std_num]))
            print("Результаты группового анализа по пациентам для эталона", self.stds[std_num].name, "\n",
                  "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] =", "\n",
                  funcs.stat_analysis(self.concats[std_num]))

        # TODO: таблица графиков

    def graph_normal(self, std_num, sample_num, base: Figure):
        data = self.distances[std_num][sample_num]
        fig = base.subplots(1, 1)
        rng = np.linspace(-4, 4, 100)
        fig.hist(data, bins=7, range=(-3, 4), normed=True, alpha=0.5, histtype='stepfilled',
                 color='steelblue', edgecolor='none')
        fig.plot(rng, stats.norm.pdf(rng, np.mean(data), np.std(data)))
        fig.plot(rng, stats.gaussian_kde(data)(rng))

    def graph_normal_density(self, std_num, sample_num, base: Figure):
        data = self.distances[std_num][sample_num]
        fig = base.subplots(2)
        rng = np.linspace(-4, 4, 100)
        fig[0].hist(data, bins=7, range=(-3, 4), normed=True, alpha=0.5,
                    histtype='stepfilled', color='steelblue', edgecolor='none')
        fig[0].plot(rng, stats.norm.pdf(rng, np.mean(data), np.std(data)))

        fig[1].plot(rng, stats.norm.pdf(rng, np.mean(data), np.std(data)))
        fig[1].plot(rng, stats.gaussian_kde(data)(rng))


def test():
    from matplotlib import pyplot as plt
    from science.classes import Patient, Group, Standard
    Standard.from_file("samples/Flow_62.txt")
    Standard.from_file("samples/Kp_62.txt")

    Group('1')
    pat1 = Patient('1', '1')
    pat1.add_category("", "samples/1_1.txt")
    pat1.add_category("n", "samples/1_1n.txt")

    pat2 = Patient('2', '1')
    pat2.add_category("", "samples/1_2.txt")
    pat2.add_category("n", "samples/1_2n.txt")

    stat = AllStandards([pat1, pat2], "")
    stat.get_report()

    base00 = plt.figure(1)
    stat.graph_normal(0, 0, base00)

    base00d = plt.figure(2)
    stat.graph_normal_density(0, 0, base00d)

    base10 = plt.figure(3)
    stat.graph_normal(1, 0, base10)

    base10d = plt.figure(4)
    stat.graph_normal_density(1, 0, base10d)

    plt.show()


if __name__ == '__main__':
    test()
