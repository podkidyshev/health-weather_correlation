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

fig, ax = plt.subplots(1, 1)

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


def func(x, y):
    """ Суммирование элементов двух разных списков """
    return x + y  

def sum_list(x):
    """Почленное суммирование списков списка"""
    y = [0]*len(x[0])
    for i in range(len(x)):
        y = list( map(func, y, x[i]) )
    return y

def concat_list1(x):
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
    num_tests = 10**2
    num_rejects = 0
    for i in range(num_tests):
	    normed_data = (x - mean(x)) / std(x)
	    D, pval = stats.kstest(normed_data, 'norm')
	    if pval < alpha:
		    num_rejects += 1
    ratio = float(num_rejects) / num_tests
    print("Результаты теста Колмогорова-Смирнова: ", "из 100 прогонов доля", '{}/{} = {:.2f} отклоняет гипотезу H0 на уровне отклонения {}'.format(num_rejects, num_tests, ratio, alpha)) 	
    #return 

def test_normal_q(x):
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

def graph_kde(xr1, xr2, xr3, xr4):
    """Построение 4-х ядерных оценок плотности и кривой Гаусса"""
    _range = np.linspace(0.9 * np.min(xr1), 1.1 * np.max(xr1), 100)
    plt.plot(_range, st.gaussian_kde(xr1)(_range), color = 'blue')
    plt.plot(_range, st.gaussian_kde(xr2)(_range), color = 'red')
    plt.plot(_range, st.gaussian_kde(xr3)(_range), color = 'green')
    plt.plot(_range, st.gaussian_kde(xr4)(_range), color = 'yellow')
    plt.plot(_range, norm.pdf(_range, 0, 1), '-.k')
    plt.style.use('seaborn-white')
    ax.set(xlim=(-4, 4), ylim=(0, 0.5),
           xlabel='x', ylabel='',
           title='синий график - без нагрузки, красный график - с физ.нагрузкой, \n зеленый график - после отдыха, желтый график - с эмоц.нагрузкой, \n черный штрихпунктирный график - стандартная кривая Гаусса')
    plt.show()

def graph_kde3(xr1, xr2, xr3):
    """Построение 3-х ядерных оценок плотности и кривой Гаусса"""
    _range = np.linspace(0.9 * np.min(xr1), 1.1 * np.max(xr1), 100)
    plt.plot(_range, st.gaussian_kde(xr1)(_range), color = 'blue')
    plt.plot(_range, st.gaussian_kde(xr2)(_range), color = 'red')
    plt.plot(_range, st.gaussian_kde(xr3)(_range), color = 'green')
    plt.plot(_range, norm.pdf(_range, 0, 1), '-.k')
    plt.style.use('seaborn-white')
    ax.set(xlim=(-4, 4), ylim=(0, 0.5),
           xlabel='x', ylabel='',
           title='синий график - с физ.нагрузкой, красный график - после отдыха , \n зеленый график - с эмоц.нагрузкой, \n черный штрихпунктирный график - стандартная кривая Гаусса')
    plt.show()

def graph_kde_all(x, y, u, v, w):
    """Построение 4-х ядерных оценок плотности и кривой Гаусса для всех пациентов и эталона w"""
    for j in range(len(x)): graph_kde(sequence_distance(sequence_max(x[j]), sequence_max(w)), sequence_distance(sequence_max(y[j]), sequence_max(w)), sequence_distance(sequence_max(u[j]), sequence_max(w)), sequence_distance(sequence_max(v[j]), sequence_max(w)))

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

#print("Число эталонов:", n_standart , "\n", "Список значений эталонов:", "\n",  standart)

#for i in range(n_standart):
#    print("Список максимумов значений эталона", i , "\n", sequence_max(standart[i]), "Всего максимумов:", sum(sequence_max(standart[i])))

#Загрузка списка образцов

#Данные пациентов без нагрузки

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
    

#Данные пациентов с физической нагрузкой

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
    

#Данные пациентов с эмоциональной нагрузкой

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
    
#Данные пациентов после отдыха

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
  

print("Построение кривой Гаусса и 4-х ядерных оценок плотности 4-х фактор-образцов для первого пациента и первого эталона")                                                                      
graph_kde(sequence_distance(sequence_max(sample[0]), sequence_max(standart[0])), sequence_distance(sequence_max(sample_n[0]), sequence_max(standart[0])), sequence_distance(sequence_max(sample_o[0]), sequence_max(standart[0])), sequence_distance(sequence_max(sample_e[0]), sequence_max(standart[0])))

print("Построение кривой Гаусса и 4-х ядерных оценок плотности 4-х фактор-образцов для всех пациентов и всех эталонов")
for i in range(len(standart)): graph_kde_all(sample, sample_n, sample_o, sample_e, standart[i])
    
print("Результаты  визуального анализа и тестирования нормальности для фактор-образца без нагрузки для всех пациентов и всех эталонов")
       
for i in range(n_standart):
    for j in range(n_sample): print("Результаты визуального анализа распределения фактор-образца без нагрузки пациента", j, "для эталона ", i, "\n",visual_analysis(sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))))  
    for j in range(n_sample): print("Результаты тестирования нормальности распределения фактор-образца без нагрузки пациента", j, "для эталона ", i, "\n", test_normal(sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))))
    
    
print("Результаты статистического  анализа распределения фактор-образца без нагрузки  для всех пациентов и всех эталонов")

for i in range(n_standart):
    for j in range(n_sample): print("Результаты статистического о анализа распределения фактор-образца без нагрузки пациента", j, "для эталона ", i, "\n", "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] =  ", "\n", stat_analys(sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))))
    

    
    


   
