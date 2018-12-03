# -*- coding: utf-8 -*-
# Ввод образцов_послед.максимумов_распред..расстояний_гистограммы
import numpy as np
import scipy.stats as st

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
# noinspection PyUnresolvedReferences

from src.main.python.science import *


matplotlib.use("Qt5Agg")


def init_data(filename_reference: str, filenames_patients: list):
    """
    n = 1000  # объём выборки
    # noinspection PyUnresolvedReferences
    x = np.arange(-3, 4, 0.01)
    # загрузка списка Kp и списков пациентов группы
    """
    name = os.path.splitext(os.path.basename(filenames_patients[0]))[0]

    data_reference = read_sample(filename_reference)
    print("Список Кр-значений:", data_reference, len(data_reference))
    print("Список максимумов Кр-значений:", sequence_max(data_reference), len(sequence_max(data_reference)))

    data_patients = [None] * 4
    data_postfix = [
        "без нагрузки",
        "с физической нагрузкой",
        "после отдыха",
        "с эмоциональной нагрузкой"
    ]

    for idx, (filename_patient, postfix) in enumerate(zip(filenames_patients, data_postfix)):
        if filename_patient is not None:
            data_patient = read_sample(filename_patient)
            data_patients[idx] = data_patient

            print("Список значений пациента {} {}:".format(name, postfix),
                  data_patient,
                  len(data_patient))
            print("Список максимумов значений пациента {} без нагрузки:".format(name),
                  sequence_max(data_patient),
                  len(sequence_max(data_patient)))
            print()

    # вычисление распределения расстояний  от максимумов рядов пациентов до ближайшего максимума Kp
    print("Ряды расстояний и распределения расстояний от максимумов пациента 1_1 до ближайшего максимума Kp")
    # вычисление последовательностей расстояний  от максимумов рядов пациентов до ближайшего максимума Kp

    x_distance = [sequence_distance(sequence_max(d), sequence_max(data_reference))
                  if d is not None else None for d in data_patients]
    x_distrib = [distrib(xi_distance)
                 if xi_distance is not None else None for xi_distance in x_distance]

    for xi_distance, xi_distrib, postfix in zip(x_distance, x_distrib, data_postfix):
        if xi_distance is not None:
            print("Ряд расстояний от максимумов пациента {} {} до ближайшего максимума Kp:".format(name, postfix),
                  xi_distance)
            print("Распределение расстояний (значения от -3 до 3) пациента {} {}".format(name, postfix),
                  xi_distrib)
    print()

    print("Анализ распределений расстояний от максимумов пациента 1_1 до ближайшего максимума Kp")
    for xi_distance, postfix in zip(x_distance, data_postfix):
        if xi_distance is not None:
            print("Анализ распределений расстояний пациента {} {}:".format(name, postfix), "\n",
                  "\tвыборочное среднее = {:.4f}".format(np.mean(xi_distance)), "\n",
                  "\tстандартное отклонение = {:.4f}".format(np.std(xi_distance)), "\n",
                  "\tдоверительный интервал = ({:.4f}, {:.4f})".format(*st.t.interval(0.95,
                                                                                      len(xi_distance) - 1,
                                                                                      loc=np.mean(xi_distance),
                                                                                      scale=st.sem(xi_distance))), "\n")
    return x_distance


def plot(x_distance, base_figure):
    fig, ax = plt.subplots(1, 1)
    # fig = base_figure.subplots(1, 1)

    colors = [
        "blue",
        "red",
        "green",
        "yellow"
    ]
    titles = [
        "синий график - без нагрузки",
        "красный график - с физ.нагрузкой",
        "зеленый график - после отдыха",
        "желтый график - с эмоц.нагрузкой",
        "черный штрихпунктирный график - стандартная кривая Гаусса"
    ]

    values_range = np.linspace(0.9 * np.min(x_distance[0]), 1.1 * np.max(x_distance[0]), 106)
    for xi, c in zip(x_distance, colors):
        if xi is not None:
            plt.plot(values_range, st.gaussian_kde(xi)(values_range), color=c)

    plt.plot(values_range, st.norm.pdf(values_range, 0, 1), '-.k')
    plt.style.use('seaborn-white')

    t = '\n'.join([t for idx, t in enumerate(titles) if idx > 3 or x_distance[idx] is not None])
    # fig.add_axes([-4, 0, 8, 0.5], xlabel='x', ylabel='', title=t)
    ax.set(xlim=(-4, 4), ylim=(0, 0.5), xlabel='x', ylabel='', title=t)


# printer = FakePrint()
# printer.activate()

_x_distance = init_data("samples/Flow_62.txt", ["samples/1_1.txt",
                                                "samples/1_1n.txt",
                                                "samples/1_1o.txt",
                                                "samples/1_1e.txt"])

_base_figure = Figure(figsize=(200, 200), dpi=100)
# _base_figure = plt.figure(figsize=(200, 200), dpi=100)

plot(_x_distance, _base_figure)

plt.show()
# _base_figure.show()

# printer.deactivate()
# for entry in printer.log:
#     print(entry, end='')
