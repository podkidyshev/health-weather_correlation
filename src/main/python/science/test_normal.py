# Тест нормальности
import time
# noinspection PyUnresolvedReferences
from numpy.random import seed
from scipy.stats import shapiro, normaltest, anderson
import scipy.stats as stats
from numpy import *
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from src.main.python.science import read_sample, sequence_distance, sequence_max


def tests(data_reference: list):
    report = {}
    # seed the random number generator
    if __name__ == '__main__':
        seed(1)
    else:
        seed(int(time.time() * 1000))

    # generate univariate observations
    # normality test
    # print("Shapiro-Wilk Test")
    stat, p = shapiro(data_reference)
    # print('Statistics=%.3f, p=%.3f' % (stat, p))
    # interpret
    alpha = 0.05
    # if p > alpha:
    #     print('Sample looks Gaussian (fail to reject H0)')
    # else:
    #     print('Sample does not look Gaussian (reject H0)')
    report["shapiro-wilk"] = {
        "name": "Shapiro-Wilk Test",
        "alpha": alpha,
        "stat": stat,
        "p": p,
        "res": p > alpha
    }

    # print("D'Agostino and Pearson's Test")
    # normality test
    stat, p = normaltest(data_reference)
    # print('Statistics=%.3f, p=%.3f' % (stat, p))
    # interpret
    alpha = 0.05
    # if p > alpha:
    #     print('Sample looks Gaussian (fail to reject H0)')
    # else:
    #     print('Sample does not look Gaussian (reject H0)')
    report["agostino_pearson"] = {
        "name": "D'Agostino and Pearson's Test",
        "alpha": alpha,
        "stat": stat,
        "p": p,
        "res": p > alpha
    }

    # print("Anderson-Darling Test")
    result = anderson(data_reference)

    report["anderson"] = {
        "name": "Anderson-Darling Test",
        "statistic": result[0],
        "critical": result[1],
        "res": []
    }
    # print('Statistic: %.3f' % result.statistic)
    # for i in range(len(result[1])):
    for sl, cv in zip(result[2], result[1]):
        report["anderson"]["res"].append((sl, cv, result[0] < cv))
        # if result.statistic < result.critical_values[i]:
        #     print('%.3f: %.3f, data looks normal (fail to reject H0)' % (sl, cv))
        #     report["anderson"]["res"].append((sl, cv, True))
        # else:
        #     print('%.3f: %.3f, data does not look normal (reject H0)' % (sl, cv))

    # print("Kolmogorov-Smirnov Test")
    num_tests = 10 ** 3
    num_rejects = 0
    for i in range(num_tests):
        normed_data = (data_reference - mean(data_reference)) / std(data_reference)
        D, pval = stats.kstest(normed_data, 'norm')
        if pval < alpha:
            num_rejects += 1
    ratio = float(num_rejects) / num_tests
    # print("Kolmogorov test for normality:", '{}/{} = {:.2f} rejects at rejection level {}'.format(
    #     num_rejects, num_tests, ratio, alpha))
    report["ks"] = {
        "name": "Kolmogorov-Smirnov Test",
        "num_tests": num_tests,
        "num_rejects": num_rejects,
        "ratio": ratio,
        "alpha": alpha
    }

    return report


def prob_plot(data_reference, base_figure):
    # fig = base_figure.subplots(1, 1)

    _range = np.linspace(0.9 * np.min(data_reference), 1.1 * np.max(data_reference), 100)
    stats.probplot(data_reference, dist="norm", plot=plt)
    # stats.probplot(stats.gaussian_kde(data)(_range), dist="norm", plot=plt)


def test():
    data_reference = read_sample("samples/Flow_62.txt")
    data_patient = read_sample("samples/1_1.txt")
    x_distance = sequence_distance(sequence_max(data_patient), sequence_max(data_reference))

    # data_reference = [1, -1, 1, 1, -3, 2, 0, 2, -2, -1, 0, 1, 1, 3, -3, 0, 1, -1, 3]
    report = tests(x_distance)

    base_figure = Figure(figsize=(200, 200), dpi=100)
    # base_figure = plt.figure(figsize=(200, 200), dpi=100)

    prob_plot(data_reference, base_figure)

    plt.show()
    # base_figure.show()


if __name__ == '__main__':
    test()
