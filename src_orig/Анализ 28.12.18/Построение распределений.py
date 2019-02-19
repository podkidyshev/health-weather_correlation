#-*- coding: utf-8 -*-
from numpy import *
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from scipy.stats import logistic,uniform,norm,pearsonr
from numpy import sqrt,pi,e
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.weightstats import zconfint
from numpy.random import seed
from numpy.random import randn
from scipy.stats import shapiro
from scipy.stats import normaltest
from scipy.stats import anderson
import scipy.stats as stats

#функция вычисления числа ненулевых элементов списка

def len_ampl(x):
    y = 0
    for i in range(len(x)):
        if  x[i] != 0:
            y +=1 
    return y

#функция вычисления максимумов временного ряда
def sequence_max(x):
    """вычисление максимумов временного ряда"""
    y = []
    for i in range(1,len(x)-1):
        if x[i-1] <= x[i] and x[i+1] <= x[i]:
            y.append(x[i])
        else: y.append(0)    
    return y

#функция вычисления расстояний от максимумов ряда пациента до ближайшего максимума Kp:
#"-" максимум Kp находится слева, "+" максимум Kp находится справа 
def sequence_distance(x, y):
    """вычисление расстояний от максимумов образца до ближайшего максимума эталона"""
    x.insert(0,0)
    u = []   
    for i in range(len(x)): 
        if x[i] != 0:
            for j in range(len(y)):
                if ( i - j >= 0 and y[i - j ] != 0) and ( i + j < len(y) and y[i + j ] != 0):
                    if j == 0:
                        u.append(j)
                    else:
                        u.append(j)
                        u.append(-j)
                    break                     
                elif ( i - j >= 0 and y[i - j ] != 0) :
                    u.append(j)
                    break
                elif ( i + j < len(y)  and y[i + j ] != 0):
                    u.append(-j)
                    break                    
    return u

def sequence_distance1(x, y):
    """вычисление расстояний от максимумов образца до ближайшего максимума эталона"""
    u = []   
    for i in range(len(x)): 
        if x[i] != 0:
            for j in range(len(y)):
                if ( i - j >= 0 and y[i - j ] != 0) and ( i + j < len(y) and y[i + j ] != 0):
                    if j == 0:
                        u.append(j)
                    else:
                        u.append(j)
                        u.append(-j)
                    break                     
                elif ( i - j >= 0 and y[i - j ] != 0) :
                    u.append(j)
                    break
                elif ( i + j < len(y)  and y[i + j ] != 0):
                    u.append(-j)
                    break                    
    return u

#функция вычисления распределения расстояний от максимумов ряда пациента до ближайшего максимума Kp 
def raspred(x):
    """распределение расстояний от максимумов образца до ближайшего максимума эталона"""
    y = []
    for i in range(7):
        y.append(x.count(i-3)) 
    return y

def func(x, y):
    """ Суммирование элементов двух разных списков """
    return x + y  

def sum_list(x):
    """Почленное суммирование списков списка"""
    y = [0]*len(x[0])
    for i in range(len(x)):
        y = list( map(func, y, x[i]) )
    return y

def concat_list(x):
    """Конкатенация списков списка"""
    y = []
    for i in range(len(x)):
        y += x[i]
    return y


def stat_analysis(x,y):
    """Статистический анализ ряда распределений расстояний от x до y"""
    z = sequence_distance(sequence_max(x), sequence_max(y))
    w = [np.mean(z), np.std(z), st.t.interval(0.95, len(z)-1, loc=np.mean(z), scale=st.sem(z))]
    return w

def stat_analys(z):
    """Статистический анализ ряда распределений"""
    return    [np.mean(z), np.std(z), st.t.interval(0.95, len(z)-1, loc=np.mean(z), scale=st.sem(z))]

def visual_analysis(x):
    """Визуальный анализ ряда распределений"""
    fig, ax = plt.subplots()
    _range = np.linspace(-3,4, 100)
    plt.style.use('seaborn-white')
    ax.hist(x, bins=7,  range  = (-3,4), normed=True, alpha=0.5,
    histtype='stepfilled', color='steelblue', edgecolor='none')
    ax.plot(_range, norm.pdf(_range, np.mean(x), np.std(x)), '-.k')
    ax.plot(_range, st.gaussian_kde(x)(_range), color = 'blue')
    ax.set(xlim=(-3, 4), ylim=(0, 0.5),
           xlabel='x', ylabel='',
           title='синий график - ядерная оценка плотности распределения, \n черный штрихпунктирный график - кривая Гаусса')
    return plt.show() 
    
def visual_analys2(x,y):
    """Визуальный анализ двух рядов распределений"""    
    fig, ax = plt.subplots(2)
    _range = np.linspace(-3, 4, 100)
    plt.style.use('seaborn-white')
    ax[0].hist(x, bins=11,  range  = (-3,4), normed=True, alpha=0.5,
               histtype='stepfilled', color='steelblue',
               edgecolor='none')
    ax[0].plot(_range, norm.pdf(_range, np.mean(x), np.std(x)))
    ax[0].plot(_range, st.gaussian_kde(x)(_range))
    ax[1].hist(y, bins=11,  range  = (-3,4), normed=True, alpha=0.5,
               histtype='stepfilled', color='steelblue',
               edgecolor='none')
    ax[1].plot(_range, norm.pdf(_range, np.mean(y), np.std(y)))
    ax[1].plot(_range, st.gaussian_kde(y)(_range))
    return plt.show() 


def test_normal(x):
    """Тестирование распределения на нормальность""" 
    print("Тест нормальности Шапиро-Вилка")
    stat, p = shapiro(x)
    print('Statistics=%.3f, p=%.3f' % (stat, p))
    alpha = 0.05
    if p > alpha:
	    print('Образец выглядит гауссовским (не может отклонить гипотезу H0)')
    else:
	    print('Образец не выглядит гауссовским (отклонить гипотезу H0)')
    
    print("Тест нормальности Д'Агостино-Пирсона")	
    if len(x) > 19:
	    x1 = x
    else:
	    x1 = []
	    for i in range(50):
		    x1.append(random.choice(x))
    stat, p = normaltest(x1)
    print('Statistics=%.3f, p=%.3f' % (stat, p))
    if p > alpha:
	    print('Образец выглядит гауссовским (не может отклонить гипотезу H0)')
    else:
	    print('Образец не выглядит гауссовским (отклонить H0)')
    
    print("Тест нормальности Андерсона-Дарлинга")
    result = anderson(x)
    print('Statistic: %.3f' % result.statistic)
    p = 0
    for i in range(len(result.critical_values)):
	    sl, cv = result.significance_level[i], result.critical_values[i]
	    if result.statistic < result.critical_values[i]:
		    print('%.3f: %.3f, Образец выглядит гауссовским (не может отклонить гипотезу H0)' % (sl, cv))
	    else:
		    print('%.3f: %.3f, Образец не выглядит гауссовским (отклонить H0)' % (sl, cv))
    print("Тест нормальности Колмогорова-Смирнова")
    num_tests = 10**3
    num_rejects = 0
    for i in range(num_tests):
	    normed_data = (x - mean(x)) / std(x)
	    D, pval = stats.kstest(normed_data, 'norm')
	    if pval < alpha:
		    num_rejects += 1
    ratio = float(num_rejects) / num_tests
    print("Результаты теста Колмогорова-Смирнова: ", "из 1000 прогонов доля", '{}/{} = {:.2f} отклоняет гипотезу H0 на уровне отклонения {}'.format(num_rejects, num_tests, ratio, alpha)) 	
    _range = np.linspace(0.9 * np.min(x), 1.1 * np.max(x), 100)
    stats.probplot(x, dist="norm", plot=plt)
    return plt.show()

#Загрузка списка эталонов

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

#Загрузка списка образцов

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
    
    
print("Распределения максимумов и расстояний фактор-образца без нагрузки для всех образцов и всех эталонов")

for i in range(n_standart):
    for j in range(len(sample)):
        print("Последовательность максимумов образца  ", j, "  и эталона  ", i, sequence_max(sample[j]), len_ampl(sequence_max(sample[j])))
        print("Последовательность расстояний для образца  ", j, "  и эталона  ", i, sequence_distance(sequence_max(sample[j]), sequence_max(standart[i])), len(sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))))

print("Результаты визуального анализа распределения расстояний фактор-образца без нагрузки для всех образцов и всех эталонов")

for i in range(n_standart):
    for j in range(len(sample)):
        print("Результаты визуального анализа распределения расстояний фактор-образца без нагрузки для образца  ", j, "  и эталона  ", i, visual_analysis(sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))))

print("Результаты тестирования нлрмальности распределения расстояний фактор-образца без нагрузки для всех образцов и всех эталонов")

for i in range(n_standart):
    for j in range(len(sample)): print("Результаты тестирования нормальности распределения расстояний фактор-образца без нагрузки для образца  ", j, "  и эталона  ", i, "\n", 
	test_normal(sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))))

print("Результаты статистического анализа распределения расстояний фактор-образца без нагрузки для всех образцов и всех эталонов")

for i in range(n_standart):
    for j in range(len(sample)): print("Результат статистическогоанализа распределения расстояний фактор-образца без нагрузки для образца  ", j, "  и эталона  ", i, "\n",  "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] =  ", "\n" , stat_analys(sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))))
	
