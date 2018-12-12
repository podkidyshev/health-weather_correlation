import numpy as np
import scipy.stats as stats
from matplotlib.figure import Figure

import science
import science.test_normal as tn
import science.funcs as funcs
import science.classes as classes


class AllStandards:
    def __init__(self, samples: list, cat: int):
        """
        Анализ по всем эталонам и переданным пациентам в категории cat
        :param samples:
        :param cat:
        """
        self.cat = cat
        self.cat_name = science.CATS[cat]

        error_samples = []
        for sample in samples:
            if not sample.has_cat(cat):
                error_samples.append(sample.name)
        if len(error_samples):
            raise funcs.StatComputingError('Запрошена обработка категории "{}".\n '
                                           'У пациентов {} нет данных в этой категории'.format(self.cat_name,
                                                                                               error_samples))

        self.stds = [std for std in classes.Standard.standards.values()]
        self.stds_count = len(self.stds)
        self.stds_data = [std.data for std in self.stds]
        self.stds_seq_max = [std.seq_max for std in self.stds]

        self.pats = samples[:]
        self.pats_count = len(self.pats)
        self.pats_data = [pat.data[self.cat] for pat in self.pats]
        self.pats_seq_max = [pat.seq_max[self.cat] for pat in self.pats]

        self.pats_data_all = funcs.sum_list(self.pats_data)
        self.pats_seq_max_all = funcs.sequence_max(self.pats_data_all)

        self.distances = [[funcs.sequence_distance(pat_seq_max, std_seq_max, insert_zero=True)
                           for pat_seq_max in self.pats_seq_max]
                          for std_seq_max in self.stds_seq_max]

        self.k = sum(map(lambda sm: sum(sm), self.pats_seq_max))
        self.concats = [funcs.sum_list(self.distances[i]) for i in range(self.stds_count)]
        self.tn_by_day = [tn.test_normal(funcs.sequence_distance(self.pats_seq_max_all,
                                                                 std_seq_max,
                                                                 insert_zero=True),
                                         qq=False)
                          for std_seq_max in self.stds_seq_max]
        self.tn_by_pat = [tn.test_normal(concat, qq=False) for concat in self.concats]

    def get_report(self):
        print("Число эталонов:", len(self.stds_data), "\n", "Список значений эталонов:", "\n", self.stds_data)

        for idx, std_seq_max in enumerate(self.stds_seq_max):
            print("Список максимумов значений эталона", self.stds[idx].name, "\n", std_seq_max,
                  "Всего максимумов:", np.sum(std_seq_max))

        print("Число образцов:", len(self.pats))

        print("Распределения максимумов и расстояний по пациентам для всех эталонов")
        for std_idx, std_seq_max in enumerate(self.stds_seq_max):
            for pat_idx in range(self.pats_count):
                print("Последовательность максимумов образца", self.pats[std_idx].name,
                      "и эталона", self.stds[std_idx].name, std_seq_max, np.sum(std_seq_max))
                print("Последовательность расстояний для образца", self.pats[std_idx].name,
                      "и эталона", self.stds[std_idx].name, self.distances[std_idx][pat_idx],
                      len(self.distances[std_idx][pat_idx]))

        print("k =", self.k)
        for std_idx, concat in enumerate(self.concats):
            print("Распределение расстояний группы пациентов для эталона ", self.stds[pat_idx].name,
                  concat, "Всего значений =", len(concat))

        print("Результаты сравнительного визуального анализа по дням и по пациентам всех образцов со всеми эталонами")
        for std_idx in range(self.stds_count):
            print("Результаты визуального анализа для группового образца по дням и по пациентам для эталона",
                  self.stds[std_idx].name, "\n")
            # TODO: здесь self.stds_count графиков
            # base = plt.figure(figsize=(5, 4), dpi=100)
            # funcs.visual_analysis2(funcs.sequence_distance(funcs.sequence_max(funcs.sum_list(self.samples_data)),
            #                                                self.stds_seq_max[std_idx], insert_zero=True),
            #                      self.concats[std_idx], base)
            print("Результаты тестирования нормальности распределения группового образца по дням для эталона ",
                  self.stds[pat_idx].name, "\n")
            tn.get_report(self.tn_by_day[std_idx])

            print("Результаты тестирования нормальности распределения группового образца по пациентам для эталона",
                  self.stds[pat_idx].name, "\n")
            tn.get_report(self.tn_by_pat[std_idx])

        for std_idx in range(self.stds_count):
            print("Результаты группового анализа по дням для эталона", self.stds[std_idx].name, "\n",
                  "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] =", "\n",
                  funcs.stat_analysis_distances(self.pats_data_all, self.stds_data[std_idx]))
            print("Результаты группового анализа по пациентам для эталона", self.stds[std_idx].name, "\n",
                  "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] =", "\n",
                  funcs.stat_analysis(self.concats[std_idx]))

        # TODO: таблица графиков
        # Групповой анализ всех со всеми.py (324-329)


def test():
    from matplotlib import pyplot as plt
    from science.classes import Patient, Standard
    Standard.from_file("samples/Flow_62.txt")
    Standard.from_file("samples/Kp_62.txt")

    pat1 = Patient.from_file("samples/1_1.xlsx")
    pat2 = Patient.from_file("samples/1_2.xlsx")

    stat = AllStandards([pat1, pat2], 0)
    stat.get_report()


if __name__ == '__main__':
    test()
