# -*- coding: utf-8 -*-
# Ввод образцов_послед.максимумов_распред..расстояний_гистограммы
import numpy as np
import scipy.stats as stats

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from science.classes import Patient, Standard, CATEGORIES_SHORT as categories
from science import *


def std_pat_stat_by_category(std: Standard, pat: Patient, category: str):
    distance = sequence_distance(pat.categories_seq_max[category], std.seq_max)
    return {
        'seq_max': pat.categories_seq_max[category],
        "distance": distance,
        "distrib": distrib(distance),
        'mean': np.mean(distance),
        'std': np.std(distance),
        't-interval': stats.t.interval(0.95, len(distance) - 1, loc=np.mean(distance), scale=stats.sem(distance))
    }


def st_pat_stat(std: Standard, pat: Patient):
    report = {}
    for cat, pat_data in pat.categories.items():
        if pat_data is not None:
            report[cat] = std_pat_stat_by_category(std, pat, cat)
    return report


class StandardPatientStat:
    def __init__(self, std: Standard, pat: Patient):
        self.std = std
        self.pat = pat
        self.by_category = st_pat_stat(std, pat)

    def plot_gaussian(self, base: Figure):
        fig = base.subplots(1, 1)

        colors = {"blue": "синий", "red": "красный", "green": "зеленый", "yellow": "желтый"}
        titles = ["{} график – {}".format(colors[c], categories[cat])
                  for c, cat in zip(colors, self.pat.categories) if self.pat.has_category(cat)]
        titles.append("черный штрихпунктирный график – стандартная кривая Гаусса")

        distance = self.by_category[list(self.by_category.keys())[0]]["distance"]  # произвольная дистанция
        values_range = np.linspace(0.9 * np.min(distance), 1.1 * np.max(distance), 106)
        for cat, c in zip(self.by_category, colors):
            fig.plot(values_range, stats.gaussian_kde(self.by_category[cat]["distance"])(values_range), color=c)

        fig.plot(values_range, stats.norm.pdf(values_range, 0, 1), '-.k')
        plt.style.use('seaborn-white')

        title = '\n'.join([titles[idx] + ', ' + titles[idx + 1] if idx < len(titles) - 1 else titles[idx]
                           for idx in range(0, len(titles), 2)])
        fig.set_title(title)

    def report(self):
        # принт должен быть перегружен
        print("Пациент {}. Эталон {}".format(self.pat.name, self.std.name))
        print("Список Кр-значений:", self.std.data, len(self.std.data))
        print("Список максимумов Кр-значений:", self.std.seq_max, len(self.std.seq_max), "\n")

        for cat in self.by_category:
            print("Список значений пациента {}:".format(categories[cat]),
                  self.pat.categories[cat], len(self.pat.categories[cat]))
            print("Список максимумов значений пациента {}:".format(categories[cat]),
                  self.pat.categories_seq_max[cat], len(self.pat.categories_seq_max[cat]), "\n")

        # вычисление распределения расстояний от максимумов рядов пациентов до ближайшего максимума Kp
        print("Ряды расстояний и распределения расстояний от максимумов пациента до ближайшего максимума эталона", "\n")
        # вычисление последовательностей расстояний  от максимумов рядов пациентов до ближайшего максимума Kp

        for cat in self.by_category:
            print("Ряд расстояний от максимумов пациента {} до ближайшего максимума эталона:".format(categories[cat]),
                  self.by_category[cat]["distance"])
            print("Распределение расстояний (значения от -3 до 3) пациента {}".format(categories[cat]),
                  self.by_category[cat]["distrib"], "\n")

        print("Анализ распределений расстояний от максимумов пациента до ближайшего максимума эталона", "\n")
        for cat in self.by_category:
            print("Анализ распределений расстояний пациента {}:".format(categories[cat]))
            print("\tвыборочное среднее = {:.4f}".format(self.by_category[cat]["mean"]))
            print("\tстандартное отклонение = {:.4f}".format(self.by_category[cat]["std"]))
            print("\tдоверительный интервал = ({:.4f}, {:.4f})".format(*self.by_category[cat]["t-interval"]), "\n")

        print('График анализа:')
        # TODO: здесь будет график по категориям + кривая Гаусса


def test():
    # import matplotlib
    # matplotlib.use("Qt5Agg")
    std = Standard.from_file('samples\\Flow_62.txt')
    pat = Patient('1_1')
    for cat in categories:
        pat.add_category(cat, "samples/1_1{}.txt".format(cat))

    stat = StandardPatientStat(std, pat)
    stat.report()
    base = plt.figure()
    stat.plot_gaussian(base)
    plt.show()


if __name__ == '__main__':
    test()
