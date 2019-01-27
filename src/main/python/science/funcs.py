"""
len_ampl(x) - вычисление числа ненулевых элементов временного ряда
index(x) -  вычисление индексов ненулевых элементов временного ряда
sequence_max(x) - вычисление максимумов временного ряда x
sequence_max0(x) -  вычисление индикаторов 1 максимумов временного ряда
sequence_max1(x,v) - вычисление максимумов временного ряда с ограничением амплитуды
sequence_max_ampl(x,v) - вычисление индикаторов 1 максимумов временного ряда с ограничением амплитуды
sequence_distance(x, y, insert_zero) - вычисление расстояний от максимумов образца x до ближайшего максимума эталона y
(c добавлением 0 в начало списка x или без)
# sequence_distance(x, y) - вычисление расстояний от максимумов образца x до ближайшего максимума эталона y
norm_serie(x) - Нормализация временного ряда
delta_serie(x) - Приращения временного ряда
(-)func(x, y) - Суммирование почленное элементов двух разных списков
sum_list(x) - Почленное суммирование списков списка
sum_max_lists(x) -  Почленное суммирование индикаторов 1 максимумов списков списка
concat_list(x) - Конкатенация списков списка x
stat_analysis_distances(x,y) - Статистический анализ ряда распределений расстояний от x до y
stat_analysis(z) - Статистический анализ ряда распределений z
visual_analysis(x) - Визуальный анализ ряда распределений (гистограмма, ядерная оценка плотности и кривая Гаусса)
visual_analysis2(x,y) - Визуальный анализ двух рядов распределений
    (два рисунка с гистограммой, ядерной оценкой плотности и кривой Гаусса)
test_normal(x, qq, base) - Тестирование распределения на нормальность
                           (100 прогонов теста К-С, без QQ-теста) или
                           (1000 прогонов теста К-С, с QQ-тестом и графиком)
graph_kde(xr1, xr2, xr3, xr4) - Построение 4-х ядерных оценок плотности и кривой Гаусса
graph_kde3(xr1, xr2, xr3) - Построение 3-х ядерных оценок плотности и кривой Гаусса
graph_kde_all(x, y, u, v, w) - Построение 4-х ядерных оценок плотности и кривой Гаусса для всех пациентов и эталона w
"""
import random
from operator import add

import numpy as np
import scipy.stats as st

from matplotlib import pyplot
from matplotlib.figure import Figure

pyplot.style.use('seaborn-white')


class StatComputingError(ValueError):
    pass


def len_ampl(x):
    """вычисление числа ненулевых элементов временного ряда"""
    y = 0
    for i in range(len(x)):
        if x[i] != 0:
            y += 1
    return y


def index(x):
    """вычисление индексов ненулевых элементов временного ряда"""
    y = []
    for i in range(len(x)):
        if x[i] != 0:
            y.append(i)
    return y


def sequence_max(x):
    """Вычисление максимумов временного ряда"""
    y = []
    for i in range(1, len(x) - 1):
        if x[i - 1] <= x[i] and x[i + 1] <= x[i]:
            y.append(x[i])
        else:
            y.append(0)
    return y


def sequence_max0(x):
    """вычисление индикаторов 1 максимумов временного ряда"""
    y = []
    for i in range(1, len(x) - 1):
        if x[i - 1] <= x[i] and x[i + 1] <= x[i]:
            y.append(1)
        else:
            y.append(0)
    return y


def sequence_max1(x, v):
    """вычисление максимумов временного ряда с ограничением амплитуды"""
    y = []
    for i in range(1, len(x) - 1):
        if x[i - 1] <= x[i] and x[i + 1] <= x[i] and x[i] > v:
            y.append(x[i])
        else:
            y.append(0)
    return y


def sequence_max_ampl(x, v):
    """вычисление индикаторов 1 максимумов временного ряда с ограничением амплитуды"""
    y = []
    for i in range(1, len(x) - 1):
        if x[i - 1] <= x[i] and x[i + 1] <= x[i] and x[i] > v:
            y.append(1)
        else:
            y.append(0)
    return y


def sequence_distance(x, y):
    """Вычисление расстояний от максимумов образца до максимума эталона"""
    x = [0] + x
    return sequence_distance_1(x, y)


def sequence_distance_1(x, y):
    """вычисление расстояний от максимумов образца до ближайшего максимума эталона"""
    u = []
    for i in range(len(x)):
        if x[i] != 0:
            for j in range(len(y)):
                if (i - j >= 0 and y[i - j] != 0) and (i + j < len(y) and y[i + j] != 0):
                    if j == 0:
                        u.append(j)
                    else:
                        u.append(j), u.append(-j)
                    break
                elif i - j >= 0 and y[i - j] != 0:
                    u.append(j)
                    break
                elif i + j < len(y) and y[i + j] != 0:
                    u.append(-j)
                    break
    return u


def norm_serie(x):
    """Нормализация временного ряда"""
    x_min = min(x)
    x_diff = max(x) - x_min
    return [(xi - x_min) / x_diff for xi in x]


def delta_serie(x):
    """Приращения временного ряда"""
    y = []
    for i in range(1, len(x)):
        y.append((x[i] - x[i - 1]))
    return y


def sum_list(x):
    """Почленное суммирование списков списка"""
    y = [0] * len(x[0])
    for i in range(len(x)):
        y = list(map(add, y, x[i]))
    return y


def sum_max_lists(x):
    """Почленное суммирование индикаторов 1 максимумов списков списка"""
    y = sequence_max0(x[0])
    for i in range(1, len(x)):
        y = list(map(add, y, sequence_max0(x[i])))
    return y


def concat_list(x):
    """Конкатенация списков списка"""
    y = []
    for i in range(len(x)):
        y += x[i]
    return y


def stat_analysis(z):
    """Статистический анализ ряда распределений"""
    return [np.mean(z), np.std(z), st.t.interval(0.95, len(z) - 1, loc=np.mean(z), scale=st.sem(z))]


def visual_analysis(x, base: Figure):
    """Визуальный анализ ряда распределений"""
    fig = base.subplots()
    rng = np.linspace(-3, 4, 100)
    norm_pdf = st.norm.pdf(rng, np.mean(x), np.std(x))
    fig.hist(x, bins=7, range=(-3, 4), density=True, alpha=0.5, histtype='stepfilled', color='steelblue',
             edgecolor='none')
    fig.plot(rng, norm_pdf, '-k')
    fig.plot(rng, st.gaussian_kde(x)(rng), color='blue')

    fig.set(xlim=(-3, 4), ylim=(0, max(max(norm_pdf), 0.5)), xlabel='x', ylabel='',
            title='синий график – ядерная оценка плотности распределения,\n'
                  'черный штрихпунктирный график – кривая Гаусса')


def visual_analysis2(x, y, base: Figure):
    """Визуальный анализ двух рядов распределений"""
    fig = base.subplots(2)
    rng = np.linspace(-3, 4, 100)
    fig[0].hist(x, bins=11, range=(-3, 4), density=True, alpha=0.5, histtype='stepfilled', color='steelblue',
                edgecolor='none')
    fig[0].plot(rng, st.norm.pdf(rng, np.mean(x), np.std(x)))
    fig[0].plot(rng, st.gaussian_kde(x)(rng))
    fig[1].hist(y, bins=11, range=(-3, 4), density=True, alpha=0.5, histtype='stepfilled', color='steelblue',
                edgecolor='none')
    fig[1].plot(rng, st.norm.pdf(rng, np.mean(y), np.std(y)))
    fig[1].plot(rng, st.gaussian_kde(y)(rng))


def graph_kde(xr: list, base: Figure):
    """Построение 4-х ядерных оценок плотности и кривой Гаусса"""
    fig = base.subplots(1)
    rng = np.linspace(0.9 * np.min(xr[0]), 1.1 * np.max(xr[0]), 100)
    norm_pdf = st.norm.pdf(rng, 0, 1)
    maximum = 0
    for xi, c in zip(xr, ["blue", "red", "green", "yellow"]):
        maximum = max(maximum, max(st.gaussian_kde(xi)(rng)))
        fig.plot(rng, st.gaussian_kde(xi)(rng), color=c)
    fig.plot(rng, norm_pdf, '-.k')

    maximum = max(maximum, max(norm_pdf))
    fig.set(xlim=(-4, 4), ylim=(0, max(0.5, maximum)), xlabel='x', ylabel='',
            title='синий график – без нагрузки, красный график – с физ.нагрузкой,\n'
                  'зеленый график – после отдыха, желтый график – с эмоц.нагрузкой,\n'
                  'черный штрихпунктирный график – стандартная кривая Гаусса')


def graph_kde3(xr, base: Figure):
    """Построение 3-х ядерных оценок плотности и кривой Гаусса"""
    fig = base.subplots()
    rng = np.linspace(0.9 * np.min(xr[0]), 1.1 * np.max(xr[0]), 100)
    maximum = 0
    for xi, c in zip(xr, ['blue', 'red', 'green']):
        maximum = max(maximum, max(st.gaussian_kde(xi)(rng)))
        fig.plot(rng, st.gaussian_kde(xi)(rng), color=c)
    fig.plot(rng, st.norm.pdf(rng, 0, 1), '-.k')

    maximum = max(maximum, max(st.norm.pdf(rng, 0, 1)))
    fig.set(xlim=(-4, 4), ylim=(0, max(0.5, maximum)), xlabel='x', ylabel='',
            title='синий график – с физ.нагрузкой, красный график – после отдыха,\n'
                  'зеленый график – с эмоц.нагрузкой,\n'
                  'черный штрихпунктирный график – стандартная кривая Гаусса')


def test_normal(x: list, *, qq: bool):
    """Тестирование распределения на нормальность"""
    report = {"x": x[:], "qq": qq}
    alpha = 0.05

    stat, p = st.shapiro(x)
    report["shapiro"] = {
        "name": "Shapiro-Wilk Test",
        "alpha": alpha,
        "stat": stat,
        "p": p,
        "res": p > alpha
    }

    if len(x) > 7:
        x1 = x
    else:
        x1 = []
        for i in range(8):
            x1.append(random.choice(x))

    num_tests = 10 ** 2
    num_rejects = 0
    for i in range(num_tests):
        stat, p = st.normaltest(x1)
        if p < alpha:
            num_rejects += 1
    ratio = float(num_rejects) / num_tests
    report["agostino"] = {
        "name": "D'Agostino and Pearson's Test",
        "num_tests": num_tests,
        "num_rejects": num_rejects,
        "ratio": ratio,
        "alpha": alpha,
    }

    num_tests = 10 ** 2
    num_rejects = 0
    for i in range(num_tests):
        normed_data = (x - np.mean(x)) / np.std(x)
        d, pval = st.kstest(normed_data, 'norm')
        if pval < alpha:
            num_rejects += 1
    ratio = float(num_rejects) / num_tests
    report["ks"] = {
        "name": "Kolmogorov-Smirnov Test",
        "num_tests": num_tests,
        "num_rejects": num_rejects,
        "ratio": ratio,
        "alpha": alpha
    }
    return report


def test_normal_plot(report, base):
    fig = base.subplots(1, 1)
    st.probplot(report["x"], dist="norm", plot=fig)


if __name__ == '__main__':
    from matplotlib.pyplot import figure, show

    _fig = figure()
    graph_kde([[1, 2, 3, 0], [4, 0, 2, 1], [0, 3, 1, 4], [0, 1, 3, 2]], _fig)
    show()
