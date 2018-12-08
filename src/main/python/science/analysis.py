# -*- coding: utf-8 -*-
from numpy import *
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from scipy.stats import logistic, uniform, norm, pearsonr
from numpy import sqrt, pi, e
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.weightstats import zconfint
from numpy.random import seed
from numpy.random import randn
from scipy.stats import shapiro
from scipy.stats import normaltest
from scipy.stats import anderson
import scipy.stats as stats

fig, ax = plt.subplots(1, 1)


# Загрузка списка эталонов

standart = []
n_standart = 0
with open("Kp_62.txt") as file:
    standart.append(list(map(float, [row.strip() for row in file])))
    n_standart += 1
with open("Скор.ветра_62.txt") as file:
    standart.append(list(map(float, [row.strip() for row in file])))
    n_standart += 1
with open("T_62.txt") as file:
    standart.append(list(map(float, [row.strip() for row in file])))
    n_standart += 1
with open("f_62.txt") as file:
    standart.append(list(map(float, [row.strip() for row in file])))
    n_standart += 1
with open("Po_62.txt") as file:
    standart.append(list(map(float, [row.strip() for row in file])))
    n_standart += 1
with open("BX_62.txt") as file:
    standart.append(list(map(float, [row.strip() for row in file])))
    n_standart += 1
with open("BY_62.txt") as file:
    standart.append(list(map(float, [row.strip() for row in file])))
    n_standart += 1
with open("BZ_62.txt") as file:
    standart.append(list(map(float, [row.strip() for row in file])))
    n_standart += 1
with open("SW_62.txt") as file:
    standart.append(list(map(float, [row.strip() for row in file])))
    n_standart += 1
with open("SWP_62.txt") as file:
    standart.append(list(map(float, [row.strip() for row in file])))
    n_standart += 1
with open("Flow_62.txt") as file:
    standart.append(list(map(float, [row.strip() for row in file])))
    n_standart += 1

# print("Число эталонов:", n_standart , "\n", "Список значений эталонов:", "\n",  standart)

# for i in range(n_standart):
#    print("Список максимумов значений эталона", i , "\n", sequence_max(standart[i]), "Всего максимумов:", sum(sequence_max(standart[i])))

# Загрузка списка образцов

# Данные пациентов без нагрузки

sample = []
n_sample = 0
with open("1_1.txt") as file:
    sample.append(list(map(float, [row.strip() for row in file])))
    n_sample += 1

with open("1_2.txt") as file:
    sample.append(list(map(float, [row.strip() for row in file])))
    n_sample += 1

with open("1_3.txt") as file:
    sample.append(list(map(float, [row.strip() for row in file])))
    n_sample += 1

with open("1_4.txt") as file:
    sample.append(list(map(float, [row.strip() for row in file])))
    n_sample += 1

with open("1_5.txt") as file:
    sample.append(list(map(float, [row.strip() for row in file])))
    n_sample += 1

with open("1_6.txt") as file:
    sample.append(list(map(float, [row.strip() for row in file])))
    n_sample += 1

with open("2_1.txt") as file:
    sample.append(list(map(float, [row.strip() for row in file])))
    n_sample += 1

with open("2_2.txt") as file:
    sample.append(list(map(float, [row.strip() for row in file])))
    n_sample += 1

with open("2_3.txt") as file:
    sample.append(list(map(float, [row.strip() for row in file])))
    n_sample += 1

with open("2_4.txt") as file:
    sample.append(list(map(float, [row.strip() for row in file])))
    n_sample += 1

with open("2_5.txt") as file:
    sample.append(list(map(float, [row.strip() for row in file])))
    n_sample += 1

with open("2_6.txt") as file:
    sample.append(list(map(float, [row.strip() for row in file])))
    n_sample += 1

with open("3_1.txt") as file:
    sample.append(list(map(float, [row.strip() for row in file])))
    n_sample += 1

with open("3_2.txt") as file:
    sample.append(list(map(float, [row.strip() for row in file])))
    n_sample += 1

with open("3_3.txt") as file:
    sample.append(list(map(float, [row.strip() for row in file])))
    n_sample += 1

with open("3_4.txt") as file:
    sample.append(list(map(float, [row.strip() for row in file])))
    n_sample += 1

with open("3_5.txt") as file:
    sample.append(list(map(float, [row.strip() for row in file])))
    n_sample += 1

with open("3_6.txt") as file:
    sample.append(list(map(float, [row.strip() for row in file])))
    n_sample += 1

# Данные пациентов с физической нагрузкой

sample_n = []
n_sample_n = 0
with open("1_1n.txt") as file:
    sample_n.append(list(map(float, [row.strip() for row in file])))
    n_sample_n += 1

with open("1_2n.txt") as file:
    sample_n.append(list(map(float, [row.strip() for row in file])))
    n_sample_n += 1

with open("1_3n.txt") as file:
    sample_n.append(list(map(float, [row.strip() for row in file])))
    n_sample_n += 1

with open("1_4n.txt") as file:
    sample_n.append(list(map(float, [row.strip() for row in file])))
    n_sample_n += 1

with open("1_5n.txt") as file:
    sample_n.append(list(map(float, [row.strip() for row in file])))
    n_sample_n += 1

with open("1_6n.txt") as file:
    sample_n.append(list(map(float, [row.strip() for row in file])))
    n_sample_n += 1

with open("2_1n.txt") as file:
    sample_n.append(list(map(float, [row.strip() for row in file])))
    n_sample_n += 1

with open("2_2n.txt") as file:
    sample_n.append(list(map(float, [row.strip() for row in file])))
    n_sample_n += 1

with open("2_3n.txt") as file:
    sample_n.append(list(map(float, [row.strip() for row in file])))
    n_sample_n += 1

with open("2_4n.txt") as file:
    sample_n.append(list(map(float, [row.strip() for row in file])))
    n_sample_n += 1

with open("2_5n.txt") as file:
    sample_n.append(list(map(float, [row.strip() for row in file])))
    n_sample_n += 1

with open("2_6n.txt") as file:
    sample_n.append(list(map(float, [row.strip() for row in file])))
    n_sample_n += 1

with open("3_1n.txt") as file:
    sample_n.append(list(map(float, [row.strip() for row in file])))
    n_sample_n += 1

with open("3_2n.txt") as file:
    sample_n.append(list(map(float, [row.strip() for row in file])))
    n_sample_n += 1

with open("3_3n.txt") as file:
    sample_n.append(list(map(float, [row.strip() for row in file])))
    n_sample_n += 1

with open("3_4n.txt") as file:
    sample_n.append(list(map(float, [row.strip() for row in file])))
    n_sample_n += 1

with open("3_5n.txt") as file:
    sample_n.append(list(map(float, [row.strip() for row in file])))
    n_sample_n += 1

with open("3_6n.txt") as file:
    sample_n.append(list(map(float, [row.strip() for row in file])))
    n_sample_n += 1

# Данные пациентов с эмоциональной нагрузкой

sample_e = []
n_sample_e = 0
with open("1_1e.txt") as file:
    sample_e.append(list(map(float, [row.strip() for row in file])))
    n_sample_e += 1

with open("1_2e.txt") as file:
    sample_e.append(list(map(float, [row.strip() for row in file])))
    n_sample_e += 1

with open("1_3e.txt") as file:
    sample_e.append(list(map(float, [row.strip() for row in file])))
    n_sample_e += 1

with open("1_4e.txt") as file:
    sample_e.append(list(map(float, [row.strip() for row in file])))
    n_sample_e += 1

with open("1_5e.txt") as file:
    sample_e.append(list(map(float, [row.strip() for row in file])))
    n_sample_e += 1

with open("1_6e.txt") as file:
    sample_e.append(list(map(float, [row.strip() for row in file])))
    n_sample_e += 1

with open("2_1e.txt") as file:
    sample_e.append(list(map(float, [row.strip() for row in file])))
    n_sample_e += 1

with open("2_2e.txt") as file:
    sample_e.append(list(map(float, [row.strip() for row in file])))
    n_sample_e += 1

with open("2_3e.txt") as file:
    sample_e.append(list(map(float, [row.strip() for row in file])))
    n_sample_e += 1

with open("2_4e.txt") as file:
    sample_e.append(list(map(float, [row.strip() for row in file])))
    n_sample_e += 1

with open("2_5e.txt") as file:
    sample_e.append(list(map(float, [row.strip() for row in file])))
    n_sample_e += 1

with open("2_6e.txt") as file:
    sample_e.append(list(map(float, [row.strip() for row in file])))
    n_sample_e += 1

with open("3_1e.txt") as file:
    sample_e.append(list(map(float, [row.strip() for row in file])))
    n_sample_e += 1

with open("3_2e.txt") as file:
    sample_e.append(list(map(float, [row.strip() for row in file])))
    n_sample_e += 1

with open("3_3e.txt") as file:
    sample_e.append(list(map(float, [row.strip() for row in file])))
    n_sample_e += 1

with open("3_4e.txt") as file:
    sample_e.append(list(map(float, [row.strip() for row in file])))
    n_sample_e += 1

with open("3_5e.txt") as file:
    sample_e.append(list(map(float, [row.strip() for row in file])))
    n_sample_e += 1

with open("3_6e.txt") as file:
    sample_e.append(list(map(float, [row.strip() for row in file])))
    n_sample_e += 1

# Данные пациентов после отдыха

sample_o = []
n_sample_o = 0
with open("1_1o.txt") as file:
    sample_o.append(list(map(float, [row.strip() for row in file])))
    n_sample_o += 1

with open("1_2o.txt") as file:
    sample_o.append(list(map(float, [row.strip() for row in file])))
    n_sample_o += 1

with open("1_3o.txt") as file:
    sample_o.append(list(map(float, [row.strip() for row in file])))
    n_sample_o += 1

with open("1_4o.txt") as file:
    sample_o.append(list(map(float, [row.strip() for row in file])))
    n_sample_o += 1

with open("1_5o.txt") as file:
    sample_o.append(list(map(float, [row.strip() for row in file])))
    n_sample_o += 1

with open("1_6o.txt") as file:
    sample_o.append(list(map(float, [row.strip() for row in file])))
    n_sample_o += 1

with open("2_1o.txt") as file:
    sample_o.append(list(map(float, [row.strip() for row in file])))
    n_sample_o += 1

with open("2_2o.txt") as file:
    sample_o.append(list(map(float, [row.strip() for row in file])))
    n_sample_o += 1

with open("2_3o.txt") as file:
    sample_o.append(list(map(float, [row.strip() for row in file])))
    n_sample_o += 1

with open("2_4o.txt") as file:
    sample_o.append(list(map(float, [row.strip() for row in file])))
    n_sample_o += 1

with open("2_5o.txt") as file:
    sample_o.append(list(map(float, [row.strip() for row in file])))
    n_sample_o += 1

with open("2_6o.txt") as file:
    sample_o.append(list(map(float, [row.strip() for row in file])))
    n_sample_o += 1

with open("3_1o.txt") as file:
    sample_o.append(list(map(float, [row.strip() for row in file])))
    n_sample_o += 1

with open("3_2o.txt") as file:
    sample_o.append(list(map(float, [row.strip() for row in file])))
    n_sample_o += 1

with open("3_3o.txt") as file:
    sample_o.append(list(map(float, [row.strip() for row in file])))
    n_sample_o += 1

with open("3_4o.txt") as file:
    sample_o.append(list(map(float, [row.strip() for row in file])))
    n_sample_o += 1

with open("3_5o.txt") as file:
    sample_o.append(list(map(float, [row.strip() for row in file])))
    n_sample_o += 1

with open("3_6o.txt") as file:
    sample_o.append(list(map(float, [row.strip() for row in file])))
    n_sample_o += 1

"Построение 4-х ядерных оценок плотности и кривой Гаусса для распределения расстояний от факторов (с физ.нагрузкой, после отдыха, с эмоц.нагрузкой) до исходного стандарта для отдельных образцов"

# graph_kde_all(sample, sample_n, sample_o, sample_e, standart[0])

# visual_analysis(sequence_distance1(sequence_max(sample_n[0]), sequence_max(sample[0])))
# visual_analysis(sequence_distance1(sequence_max(sample_o[0]), sequence_max(sample[0])))
# visual_analysis(sequence_distance1(sequence_max(sample_e[0]), sequence_max(sample[0])))

"Построение 3-х ядерных оценок плотности и кривой Гаусса для сравнения распределения расстояний от факторов (с физ.нагрузкой, после отдыха, с эмоц.нагрузкой) до исходного стандарта для отдельных образцов"

# graph_kde3(sequence_distance1(sequence_max(sample_n[0]), sequence_max(sample[0])), sequence_distance1(sequence_max(sample_o[0]), sequence_max(sample[0])), sequence_distance1(sequence_max(sample_e[0]), sequence_max(sample[0])))

"Результаты статистического группового анализа распределения расстояний от факторов (с физ.нагрузкой, после отдыха, с эмоц.нагрузкой) до исходного стандарта для отдельных образцов"

# print("С физической нагрузкой - без нагрузки: [Выборочное среднее, Стандартное отклонение,  Доверительный интервал] = ", "\n", stat_analys(sequence_distance1(sequence_max(sample_n[0]), sequence_max(sample[0]))), "\n", "После отдыха - без нагрузки: [Выборочное среднее, Стандартное отклонение,  Доверительный интервал] = ", "\n", stat_analys(sequence_distance1(sequence_max(sample_o[0]), sequence_max(sample[0]))), "\n", "С эмоциональной нагрузкой - без нагрузки: [Выборочное среднее, Стандартное отклонение,  Доверительный интервал] = ", "\n", stat_analys(sequence_distance1(sequence_max(sample_e[0]), sequence_max(sample[0]))))

"Результаты статистического анализа распределения расстояний от факторов (с физ.нагрузкой, после отдыха, с эмоц.нагрузкой) до исходного стандарта для всех образцов"

for i in range(len(sample)):
    print("С физической нагрузкой - без нагрузки образца ", i, "\n",
          "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] = ", "\n",
          stat_analys(sequence_distance1(sequence_max(sample_n[i]), sequence_max(sample[i]))), "\n",
          "После отдыха - без нагрузки образца ", i, "\n",
          " [Выборочное среднее, Стандартное отклонение,  Доверительный интервал] = ", "\n",
          stat_analys(sequence_distance1(sequence_max(sample_o[i]), sequence_max(sample[i]))), "\n",
          "С эмоциональной нагрузкой - без нагрузки образца ", i, "\n",
          " [Выборочное среднее, Стандартное отклонение,  Доверительный интервал] = ", "\n",
          stat_analys(sequence_distance1(sequence_max(sample_e[i]), sequence_max(sample[i]))))

"Тестирование нормальности распределения расстояний от факторов (с физ.нагрузкой, после отдыха, с эмоц.нагрузкой) до исходного стандарта для всех образцов"

for i in range(len(sample)):
    print("Результаты тестирования нормальности распределения с физической нагрузкой - без нагрузки образца", i)
    print(test_normal(sequence_distance1(sequence_max(sample_n[0]), sequence_max(sample[0]))))
    print("Результаты тестирования нормальности распределения после отдыха - без нагрузки образца", i)
    print(test_normal(sequence_distance1(sequence_max(sample_o[0]), sequence_max(sample[0]))))
    print("Результаты тестирования нормальности распределения с эмоциональной нагрузкой - без нагрузки образца", i)
    print(test_normal(sequence_distance1(sequence_max(sample_e[0]), sequence_max(sample[0]))))

# graph_kde(sequence_distance(sequence_max(sample[0]), sequence_max(standart[0])), sequence_distance(sequence_max(sample_n[0]), sequence_max(standart[0])), sequence_distance(sequence_max(sample_o[0]), sequence_max(standart[0])), sequence_distance(sequence_max(sample_e[0]), sequence_max(standart[0])))

# for i in range(len(standart)): graph_kde_all(sample, sample_n, sample_o, sample_e, standart[i])


# for i in range(n_sample): print("Список максимумов значений образца", i , sequence_max(sample[i]), "Всего максимумов:", sum(sequence_max(sample[i])))

# Групповой по дням образец

# print("Групповой образец по дням:", "\n", sum_list(sample))

# Результаты статистического анализа по дням образцов со всеми эталонами

# print("Список максимумов значений группового образца по дням:", "\n", sequence_max(sum_list(sample)), "Всего максимумов:", sum(sequence_max(sum_list(sample))))


# Групповой анализ данных

# print("Распределения максимумов и расстояний для всех образцов и всех эталонов")

# for i in range(n_standart):
#   for j in range(len(sample)):
#       print("Последовательность максимумов образца  ", j, "  и эталона  ", i, sequence_max(sample[j]), sum(sequence_max(sample[i])))
#        print("Последовательность расстояний для образца  ", j, "  и эталона  ", i, sequence_distance(sequence_max(sample[j]), sequence_max(standart[i])), len(sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))))


# Распределение средних значений пациентов без нагрузки для всех образцов и всех эталонов"

max_sample_list = []
for i in range(n_standart):
    m_list = []
    for j in range(len(sample)): m_list.append(
        np.mean(sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))))
    max_sample_list.append(m_list)
# print("Распределение средних значений пациентов без нагрузки для всех эталонов", "\n", max_sample_list)

# Распределение средних значений пациентов с физической нагрузкой для всех образцов и всех эталонов"
max_sample_list_n = []
for i in range(n_standart):
    m_list = []
    for j in range(len(sample_n)): m_list.append(
        np.mean(sequence_distance(sequence_max(sample_n[j]), sequence_max(standart[i]))))
    max_sample_list_n.append(m_list)
# print("Распределение средних значений пациентов с физической нагрузкой для всех эталонов", "\n", max_sample_list_n)

# Распределение средних значений пациентов с эмоциональной нагрузкой для всех образцов и всех эталонов"
max_sample_list_e = []
for i in range(n_standart):
    m_list = []
    for j in range(len(sample_e)): m_list.append(
        np.mean(sequence_distance(sequence_max(sample_e[j]), sequence_max(standart[i]))))
    max_sample_list_e.append(m_list)
# print("Распределение средних значений пациентов с эмоциональной нагрузкой для всех эталонов", "\n", max_sample_list_e)

# Распределение средних значений пациентов после отдыха для всех образцов и всех эталонов"
max_sample_list_o = []
for i in range(n_standart):
    m_list = []
    for j in range(len(sample_o)): m_list.append(
        np.mean(sequence_distance(sequence_max(sample_o[j]), sequence_max(standart[i]))))
    max_sample_list_o.append(m_list)
# print("Распределение средних значений пациентов после отдыха для всех эталонов", "\n", max_sample_list_o)


print(
    "Результаты  визуального  группового анализа по дням и по средним значениям для всех образцов без нагрузки и всех эталонов")

for i in range(n_standart):
    print("Результаты визуального анализа для сгруппированным по дням образцов без нагрузки  для эталона ", i, "\n",
          visual_analys2(sequence_distance(sequence_max(sum_list(sample)), sequence_max(standart[i])),
                         max_sample_list[i]))
    print(
        "Результаты тестирования нормальности распределения для сгруппированным по дням образцов без нагрузки для эталона ",
        i, "\n")
    test_normal(sequence_distance(sequence_max(sum_list(sample)), sequence_max(standart[i])))
    print(
        "Результаты тестирования нормальности распределения средних значений группы всех образцов без нагрузки для эталона ",
        i, "\n")
    test_normal(max_sample_list[i])

print(
    "Результаты статистического группового анализа по дням и по средним значениям для всех образцов без нагрузки для всех эталонов")

for i in range(n_standart):
    print("Результаты группового анализа по дням для эталонов без нагрузки  ", i, "\n",
          "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] =  ", "\n",
          stat_analysis(sum_list(sample), standart[i]))
    print("Результаты группового анализа распределения средних значений всех образцов без нагрузки для эталона  ", i,
          "\n", "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] =  ", "\n",
          stat_analys(max_sample_list[i]))
