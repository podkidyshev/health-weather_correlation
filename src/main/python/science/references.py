# -*- coding: utf-8 -*-
# Ввод эталонов_послед.максимумов
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

from science import *


fig, ax = plt.subplots(1, 1)
n = 1000  # объём выборки
# noinspection PyUnresolvedReferences
x = np.arange(-3, 4, 0.01)


def distances_distribution(data_reference: list, data_patients: dict):
    report = {}

    # загрузка списка Kp и списков пациентов группы
    with open("samples/1_1.txt") as file:
        data1 = [row.strip() for row in file]
    data1 = list(map(float, data1))
    print("Список значений пациента 1_1:", data1, len(data1))
    print("Список максимумов значений пациента 1_1:", sequence_max(data1), len(sequence_max(data1)))

    with open("samples/1_2.txt") as file:
        data2 = [row.strip() for row in file]
    data2 = list(map(float, data2))
    print("Список значений пациента 1_2:", data2)
    print("Список максимумов значений пациента 1_2:", sequence_max(data2), len(sequence_max(data2)))

    with open("samples/1_3.txt") as file:
        data3 = [row.strip() for row in file]
    data3 = list(map(float, data3))
    print("Список значений пациента 1_3:", data3)
    print("Список максимумов значений пациента 1_3:", sequence_max(data3), len(sequence_max(data3)))

    with open("samples/1_4.txt") as file:
        data4 = [row.strip() for row in file]
    data4 = list(map(float, data4))
    print("Список значений пациента 1_4:", data4)
    print("Список максимумов значений пациента 1_4:", sequence_max(data4), len(sequence_max(data4)))

    with open("samples/1_5.txt") as file:
        data5 = [row.strip() for row in file]
    data5 = list(map(float, data5))
    print("Список значений пациента 1_5:", data5)
    print("Список максимумов значений пациента 1_5:", sequence_max(data5), len(sequence_max(data5)))

    with open("samples/1_6.txt") as file:
        data6 = [row.strip() for row in file]
    data6 = list(map(float, data6))
    print("Список значений пациента 1_6:", data6)
    print("Список максимумов значений пациента 1_6:", sequence_max(data6), len(sequence_max(data6)))

    # вычисление распределения расстояний  от максимумов рядов пациентов до ближайшего максимума Kp
    print("Распределение расстояний от максимумов пациентов без нагрузки до ближайшего максимума Kp")
    xr1 = sequence_distance(sequence_max(data1), sequence_max(data_reference))
    print("Пациент 1_1:", xr1, len(xr1), "выборочное среднее =", np.mean(xr1), "стандартное отклонение =", np.std(xr1),
          "\n", "радиус интервала =", 2.10 * np.std(xr1) / sqrt(len(xr1) - 1), "Доверительный интервал:",
          [np.mean(xr1) - 2.10 * np.std(xr1) / sqrt(len(xr1) - 1), np.mean(xr1) + 2.10 * np.std(xr1) / sqrt(len(xr1) - 1)])
    xr2 = sequence_distance(sequence_max(data2), sequence_max(data_reference))
    print("Пациент 1_2:", xr2, len(xr2), "выборочное среднее =", np.mean(xr2), "стандартное отклонение =", np.std(xr2),
          "\n", "радиус интервала =", 2.13 * np.std(xr2) / sqrt(len(xr2) - 1), "Доверительный интервал:",
          [np.mean(xr2) - 2.13 * np.std(xr2) / sqrt(len(xr2) - 1), np.mean(xr2) + 2.13 * np.std(xr2) / sqrt(len(xr2) - 1)])
    xr3 = sequence_distance(sequence_max(data3), sequence_max(data_reference))
    print("Пациент 1_3:", xr3, len(xr3), "выборочное среднее =", np.mean(xr3), "стандартное отклонение =", np.std(xr3),
          "\n", "радиус интервала =", 2.09 * np.std(xr3) / sqrt(len(xr3) - 1), "Доверительный интервал:",
          [np.mean(xr3) - 2.09 * np.std(xr3) / sqrt(len(xr3) - 1), np.mean(xr3) + 2.09 * np.std(xr3) / sqrt(len(xr3) - 1)])
    xr4 = sequence_distance(sequence_max(data4), sequence_max(data_reference))
    print("Пациент 1_4:", xr4, len(xr4), "выборочное среднее =", np.mean(xr4), "стандартное отклонение =", np.std(xr4),
          "\n", "радиус интервала =", 2.18 * np.std(xr4) / sqrt(len(xr4) - 1), "Доверительный интервал:",
          [np.mean(xr4) - 2.18 * np.std(xr4) / sqrt(len(xr4) - 1), np.mean(xr4) + 2.18 * np.std(xr4) / sqrt(len(xr4) - 1)])
    xr5 = sequence_distance(sequence_max(data5), sequence_max(data_reference))
    print("Пациент 1_5:", xr5, len(xr5), "выборочное среднее =", np.mean(xr5), "стандартное отклонение =", np.std(xr5),
          "\n", "радиус интервала =", 2.09 * np.std(xr5) / sqrt(len(xr5) - 1), "Доверительный интервал:",
          [np.mean(xr5) - 2.09 * np.std(xr5) / sqrt(len(xr5) - 1), np.mean(xr5) + 2.09 * np.std(xr5) / sqrt(len(xr5) - 1)])
    xr6 = sequence_distance(sequence_max(data6), sequence_max(data_reference))
    print("Пациент 1_6:", xr6, len(xr6), "выборочное среднее =", np.mean(xr6), "стандартное отклонение =", np.std(xr6),
          "\n", "радиус интервала =", 2.14 * np.std(xr6) / sqrt(len(xr6) - 1), "Доверительный интервал:",
          [np.mean(xr6) - 2.14 * np.std(xr6) / sqrt(len(xr6) - 1), np.mean(xr6) + 2.14 * np.std(xr6) / sqrt(len(xr6) - 1)])

    # вычисление распределений расстояний  от максимумов рядов пациентов до ближайшего максимума Kp
    x1 = distrib(sequence_distance(sequence_max(data1), sequence_max(data_reference)))
    x2 = distrib(sequence_distance(sequence_max(data2), sequence_max(data_reference)))
    x3 = distrib(sequence_distance(sequence_max(data3), sequence_max(data_reference)))
    x4 = distrib(sequence_distance(sequence_max(data4), sequence_max(data_reference)))
    x5 = distrib(sequence_distance(sequence_max(data5), sequence_max(data_reference)))
    x6 = distrib(sequence_distance(sequence_max(data6), sequence_max(data_reference)))
    print("Сгруппированные распределения расстояний от максимумов пациентов без нагрузки до ближайшего максимума Kp")
    print(x1, "объем выборки =", len(xr1))
    print(x2, "объем выборки =", len(xr2))
    print(x3, "объем выборки =", len(xr3))
    print(x4, "объем выборки =", len(xr4))
    print(x5, "объем выборки =", len(xr5))
    print(x6, "объем выборки =", len(xr6))

    # вычисление группового распределения расстояний  от максимумов рядов пациентов до ближайшего максимума Kp
    xr_group = xr1 + xr2 + xr3 + xr4 + xr5 + xr6
    print("Распределение расстояний от максимумов всех пациентов без нагрузки до ближайшего максимума Kp")
    print(xr_group, len(xr_group))
    print("выборочное среднее =", np.mean(xr_group), "стандартное отклонение =", np.std(xr_group))

    # вычисление общего объема выборок
    vol = sum(sequence_max(data1)) + sum(sequence_max(data2)) + sum(sequence_max(data3)) + sum(sequence_max(data4)) + sum(
        sequence_max(data5)) + sum(sequence_max(data6))
    print("Сгруппированное распределение расстояний от максимумов "
          "первой группы пациентов без нагрузки до ближайшего максимума Kp")
    print(distrib(xr_group), "объем выборки =", vol, "\n", "радиус интервала =", 1.96 * np.std(xr_group) / sqrt(vol),
          "Доверительный интервал:", [np.mean(xr_group) - 1.96 * np.std(xr_group) / sqrt(vol),
                                      np.mean(xr_group) + 1.96 * np.std(xr_group) / sqrt(vol)])


def plot(xr_group):
    # pn=norm.cdf(x, 0, 1)#нормальное интегральное  распределение
    # ax.plot(x,pn, lw=5, alpha=0.6, label='norm cdf')
    pii = norm.pdf(x, 0.6, 1.6)
    ax.plot(x, pii, lw=5, alpha=0.6, label='norm pdf')
    # print(norm.cdf(x, -0.1, 1) - 0.5)
    plt.style.use('seaborn-white')
    plt.hist(xr_group, bins=7, range=(-3, 4), normed=True, alpha=0.5,
             histtype='stepfilled', color='steelblue',
             edgecolor='none')
    # plt.hist(xr_group, alpha=0.5)
    plt.show()


def test():
    pass


if __name__ == '__main__':
    test()
