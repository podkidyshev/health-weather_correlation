# -*- coding: utf-8 -*-
# Гистограмма_ядерная плотность_гауссиана
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
from scipy.stats import norm
# noinspection PyUnresolvedReferences
from numpy import sqrt, pi, e

fig, ax = plt.subplots(1, 1)


def descriptive1d(x):
    _x = x  # Для возможности предобработки данных (например, исключения нечисловых значений) 
    result = []
    result.append(np.mean(_x))
    result.append((np.min(_x), np.max(_x)))
    result.append(np.std(_x))
    result.append(result[-1] / result[0])
    result.append((np.percentile(_x, 25), np.percentile(_x, 50), np.percentile(_x, 75)))
    result.append(st.mode(_x))
    result.append(st.skew(_x))  # асимметрия 
    result.append(st.kurtosis(_x))  # эксцесс
    _range = np.linspace(0.9 * np.min(_x), 1.1 * np.max(_x), 100)
    result.append(st.gaussian_kde(_x)(_range))  # оценка плотности распределения

    return tuple(result)


data = [1, -1, 1, 1, -3, 2, 0, 2, -2, -1, 0, 1, 1, 3, -3, 0, 1, -1, 3]

# print(descriptive1d(data))
_range = np.linspace(0.9 * np.min(data), 1.1 * np.max(data), 106)
plt.plot(_range, st.gaussian_kde(data)(_range))
plt.plot(_range, norm.pdf(_range, np.mean(data), np.std(data)))
# plt.plot(density(data, bw=0.5))
plt.style.use('seaborn-white')
plt.hist(data, bins=7, range=(-3, 4), normed=True, alpha=0.5,
         histtype='stepfilled', color='steelblue',
         edgecolor='none')
plt.show()
