# -*- coding: utf-8 -*-
# Гистограмма_ядерная плотность_гауссиана
import numpy as np
import scipy.stats as st

from matplotlib import pyplot as plt
from matplotlib.pyplot import Figure
from scipy.stats import norm

if __name__ == '__main__':
    import matplotlib
    matplotlib.use("Qt5Agg")


def descriptive1d(x):
    x = x[:]  # Для возможности предобработки данных (например, исключения нечисловых значений)

    mean = np.mean(x)
    std = np.std(x)
    xmin, xmax = np.min(x), np.max(x)
    rng = np.linspace(0.9 * xmin, 1.1 * xmax, 100)
    result = [
        mean,
        (xmin, xmax),
        std,
        std / mean,
        (np.percentile(x, 25), np.percentile(x, 50), np.percentile(x, 75)),
        st.mode(x),
        st.skew(x),  # асимметрия
        st.kurtosis(x),  # эксцесс
        st.gaussian_kde(x)(rng)  # оценка плотности распределения
    ]
    return tuple(result)


def plot(x_distance, base_figure: Figure):
    # data = [1, -1, 1, 1, -3, 2, 0, 2, -2, -1, 0, 1, 1, 3, -3, 0, 1, -1, 3]
    # print(descriptive1d(data))
    fig = base_figure.subplots(1, 1)

    rng = np.linspace(0.9 * np.min(x_distance), 1.1 * np.max(x_distance), 106)
    fig.plot(rng, st.gaussian_kde(x_distance)(rng))
    fig.plot(rng, norm.pdf(rng, np.mean(x_distance), np.std(x_distance)))
    # plt.plot(density(data, bw=0.5))
    # plt.style.use('seaborn-white')
    fig.hist(x_distance, bins=7, range=(-3, 4), normed=True, alpha=0.5,
             histtype='stepfilled', color='steelblue',
             edgecolor='none')


def test():
    from science.samples_hist import init_data

    report = init_data("samples/Flow_62.txt", ["samples/1_1.txt",
                                               "samples/1_1n.txt",
                                               "samples/1_1o.txt",
                                               "samples/1_1e.txt"])

    base_figure = plt.figure(figsize=(5, 4), dpi=100)
    plot(report["distances"][0], base_figure)
    plt.show()


if __name__ == '__main__':
    test()
