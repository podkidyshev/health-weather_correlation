# Тест нормальности
import scipy.stats as stats
from numpy import *
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import science.funcs as funcs


def test_normal(x: list, *, qq: bool, base: Figure = None):
    """Тестирование распределения на нормальность"""
    report = {"x": x[:]}
    alpha = 0.05

    stat, p = stats.shapiro(x)
    report["shapiro"] = {
        "name": "Shapiro-Wilk Test",
        "alpha": alpha,
        "stat": stat,
        "p": p,
        "res": p > alpha
    }

    stat, p = stats.normaltest(x)
    report["agostino"] = {
        "name": "D'Agostino and Pearson's Test",
        "alpha": alpha,
        "stat": stat,
        "p": p,
        "res": p > alpha
    }

    statistic, critical_values, significance_level = stats.anderson(x)
    report["anderson"] = {
        "name": "Anderson-Darling Test",
        "statistic": statistic,
        "critical": critical_values,
        "sig_level": significance_level,
        "res": [statistic < cv for cv in critical_values]
    }

    num_tests = 10 ** (3 if qq else 2)
    num_rejects = 0
    for i in range(num_tests):
        normed_data = (x - np.mean(x)) / np.std(x)
        D, pval = stats.kstest(normed_data, 'norm')
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

    if qq and base is None:
        raise funcs.StatComputingError('Не передана фигура для рисования графика')
    if qq:
        stats.probplot(x, dist="norm", plot=base.subplots(1))
    return report


def get_report(report):
    shapiro = report["shapiro"]
    print("Тест нормальности Шапиро-Вилка")
    print('Statistics=%.3f, p=%.3f' % (shapiro["stat"], shapiro["p"]))
    if shapiro["res"]:
        print('Образец выглядит гауссовским (не может отклонить гипотезу H0)')
    else:
        print('Образец не выглядит гауссовским (отклонить гипотезу H0)')

    agostino = report["agostino"]
    print("D'Agostino and Pearson's Test")
    print('Statistics=%.3f, p=%.3f' % (agostino["stat"], agostino["p"]))
    if agostino["res"]:
        print('Образец выглядит гауссовским (не может отклонить гипотезу H0)')
    else:
        print('Образец не выглядит гауссовским (отклонить H0)')

    anderson = report["anderson"]
    print("Тест нормальности Андерсона-Дарлинга")
    print('Statistic: %.3f' % anderson["statistic"])
    for res, cv, sl in zip(anderson["res"], anderson["critical"], anderson["sig_level"]):
        if res:
            print('{:.3f}: {:.3f}, Образец выглядит гауссовским (не может отклонить гипотезу H0)'.format(sl, cv))
        else:
            print('{:.3f}: {:.3f}, Образец не выглядит гауссовским (отклонить H0)'.format(sl, cv))

    ks = report["ks"]
    print("Тест нормальности Колмогорова-Смирнова")
    num_tests = ks["num_tests"]
    num_rejects = ks["num_rejects"]
    ratio = ks["ratio"]
    alpha = ks["alpha"]
    print("Результаты теста Колмогорова-Смирнова: ", "из {} прогонов доля".format(num_tests),
          '{}/{} = {:.2f} отклоняет гипотезу H0 на уровне отклонения {}'.format(num_rejects, num_tests, ratio, alpha))
    # TODO: здесь график если надо
    # base = plt.figure()
    # st.probplot(report["x"], dist="norm", plot=base)


def test():
    x_distance = [1, -1, 1, 1, -3, 2, 0, 2, -2, -1, 0, 1, 1, 3, -3, 0, 1, -1, 3]

    base = plt.figure()
    report = test_normal(x_distance, qq=True, base=base)
    get_report(report)
    base.show()


if __name__ == '__main__':
    test()
