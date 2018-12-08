# -*- coding: utf-8 -*-
# Ввод образцов_послед.максимумов_распред..расстояний_гистограммы
import numpy as np
import scipy.stats as stats

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from science.classes import Patient, Standard
from science.funcs import sequence_distance, distrib, graph_kde
from science import CATS, nnone, plot_to_image


def std_pat_stat_by_category(std: Standard, pat: Patient, cat: int):
    distance = sequence_distance(pat.data_seq_max[cat], std.seq_max, insert_zero=True)
    return {
        "seq_max": pat.data_seq_max[cat],
        "distance": distance,
        "distrib": distrib(distance),
        'mean': np.mean(distance),
        'std': np.std(distance),
        't-interval': stats.t.interval(0.95, len(distance) - 1, loc=np.mean(distance), scale=stats.sem(distance))
    }


def st_pat_stat(std: Standard, pat: Patient):
    report = [None] * len(CATS)
    for cat, data in nnone(pat.data):
        report[cat] = std_pat_stat_by_category(std, pat, cat)
    return report


class StandardPatientStat:
    def __init__(self, std: Standard, pat: Patient):
        self.std = std
        self.pat = pat
        self.report = st_pat_stat(std, pat)

    def get_report_item(self, item: str):
        return [self.report[idx][item] if self.report[idx] is not None else None for idx in range(len(CATS))]

    def get_report(self):
        # принт должен быть перегружен
        print("Пациент {}. Эталон {}".format(self.pat.name, self.std.name))
        print("Список Кр-значений:", self.std.data, len(self.std.data))
        print("Список максимумов Кр-значений:", self.std.seq_max, len(self.std.seq_max), "\n")

        for cat, report in nnone(self.report):
            print("Список значений пациента {}:".format(CATS[cat][1]),
                  self.pat.data[cat], len(self.pat.data[cat]))
            print("Список максимумов значений пациента {}:".format(CATS[cat][1]),
                  report["seq_max"], len(report["seq_max"]), "\n")

        # вычисление распределения расстояний от максимумов рядов пациентов до ближайшего максимума Kp
        print("Ряды расстояний и распределения расстояний от максимумов пациента до ближайшего максимума эталона", "\n")
        # вычисление последовательностей расстояний  от максимумов рядов пациентов до ближайшего максимума Kp

        for cat, report in nnone(self.report):
            print("Ряд расстояний от максимумов пациента {} до ближайшего максимума эталона:".format(CATS[cat][1]),
                  report["distance"])
            print("Распределение расстояний (значения от -3 до 3) пациента {}".format(CATS[cat][1]),
                  report["distrib"], "\n")

        print("Анализ распределений расстояний от максимумов пациента до ближайшего максимума эталона", "\n")
        for cat, report in nnone(self.report):
            print("Анализ распределений расстояний пациента {}:".format(CATS[cat][1]))
            print("\tвыборочное среднее = {:.4f}".format(report["mean"]))
            print("\tстандартное отклонение = {:.4f}".format(report["std"]))
            print("\tдоверительный интервал = ({:.4f}, {:.4f})".format(*report["t-interval"]), "\n")

        print('График анализа:')
        # TODO: здесь будет график по категориям + кривая Гаусса
        # base = plt.figure(figsize=(5, 4), dpi=100)
        # graph_kde(list(map(lambda idx: stat.report[idx]["distance"], range(len(CATS)))), base)
        # img = plot_to_image()
        # img.save('test1.png')


def test():
    import matplotlib
    # matplotlib.use("Qt5Agg")
    matplotlib.rcParams.update({'font.size': 8})

    std = Standard.from_file('samples\\Flow_62.txt')
    pat = Patient('1_1')
    for cat_s, cat_l in CATS:
        pat.add_category(cat_s, "samples/1_1{}.txt".format(cat_s))

    stat = StandardPatientStat(std, pat)
    stat.get_report()
    base = plt.figure(1)
    graph_kde(stat.get_report_item("distance"), base)
    # img = plot_to_image()
    # img.save('test.png')
    plt.show()


if __name__ == '__main__':
    test()
