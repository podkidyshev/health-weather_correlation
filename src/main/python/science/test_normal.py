# Тест нормальности
# noinspection PyUnresolvedReferences
from numpy.random import seed
from scipy.stats import shapiro
from scipy.stats import normaltest
from scipy.stats import anderson
import scipy.stats as stats
from numpy import *
import numpy as np
import matplotlib.pyplot as plt

# seed the random number generator
seed(1)
# generate univariate observations

data = [1, -1, 1, 1, -3, 2, 0, 2, -2, -1, 0, 1, 1, 3, -3, 0, 1, -1, 3]

# normality test
print("Shapiro-Wilk Test")
stat, p = shapiro(data)
print('Statistics=%.3f, p=%.3f' % (stat, p))
# interpret
alpha = 0.05
if p > alpha:
    print('Sample looks Gaussian (fail to reject H0)')
else:
    print('Sample does not look Gaussian (reject H0)')

print("D'Agostino and Pearson's Test")
# normality test
stat, p = normaltest(data)
print('Statistics=%.3f, p=%.3f' % (stat, p))
# interpret
alpha = 0.05
if p > alpha:
    print('Sample looks Gaussian (fail to reject H0)')
else:
    print('Sample does not look Gaussian (reject H0)')

print("Anderson-Darling Test")
result = anderson(data)
print('Statistic: %.3f' % result.statistic)
p = 0
for i in range(len(result.critical_values)):
    sl, cv = result.significance_level[i], result.critical_values[i]
    if result.statistic < result.critical_values[i]:
        print('%.3f: %.3f, data looks normal (fail to reject H0)' % (sl, cv))
    else:
        print('%.3f: %.3f, data does not look normal (reject H0)' % (sl, cv))

print("Kolmogorov-Smirnov Test")
num_tests = 10 ** 3
num_rejects = 0
for i in range(num_tests):
    normed_data = (data - mean(data)) / std(data)
    D, pval = stats.kstest(normed_data, 'norm')
    if pval < alpha:
        num_rejects += 1
ratio = float(num_rejects) / num_tests
print("Kolmogorov test for normality:", '{}/{} = {:.2f} rejects at rejection level {}'.format(
    num_rejects, num_tests, ratio, alpha))

_range = np.linspace(0.9 * np.min(data), 1.1 * np.max(data), 100)
stats.probplot(data, dist="norm", plot=plt)
# stats.probplot(stats.gaussian_kde(data)(_range), dist="norm", plot=plt)

plt.show()
