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


#функция вычисления максимумов временного ряда
def sequence_max(x):
    """вычисление максимумов временного ряда"""
    y = []
    for i in range(1,len(x)-1):
        if x[i-1] <= x[i] and x[i+1] <= x[i]:
            y.append(1)
        else: y.append(0)    
    return y

#функция вычисления расстояний от максимумов ряда пациента до ближайшего максимума Kp:
#"-" максимум Kp находится слева, "+" максимум Kp находится справа 
def sequence_distance(x, y):
    """вычисление расстояний от максимумов образца до ближайшего максимума эталона"""
    x.insert(0,0)
    u = []   
    for i in range(len(x)): 
        if x[i] == 1:
            for j in range(len(y)):
                if ( i - j >= 0 and y[i - j ] == 1) and ( i + j < len(y) and y[i + j ] == 1):
                    if j == 0:
                        u.append(j)
                    else:
                        u.append(j)
                        u.append(-j)
                    break                     
                elif ( i - j >= 0 and y[i - j ] == 1) :
                    u.append(j)
                    break
                elif ( i + j < len(y)  and y[i + j ] == 1):
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
    #print(x, len(x))
    fig, ax = plt.subplots()
    _range = np.linspace(-5, 6, 100)
    plt.style.use('seaborn-white')
    ax.hist(x, bins=11,  range  = (-5,6), normed=True, alpha=0.5,
    histtype='stepfilled', color='steelblue', edgecolor='none')
    ax.plot(_range, norm.pdf(_range, np.mean(x), np.std(x)))
    ax.plot(_range, st.gaussian_kde(x)(_range))
    return plt.show() 
    
def visual_analys2(x,y):
    """Визуальный анализ двух рядов распределений"""    
    fig, ax = plt.subplots(2)
    _range = np.linspace(-5, 6, 100)
    plt.style.use('seaborn-white')
    ax[0].hist(x, bins=11,  range  = (-5,6), normed=True, alpha=0.5,
               histtype='stepfilled', color='steelblue',
               edgecolor='none')
    ax[0].plot(_range, norm.pdf(_range, np.mean(x), np.std(x)))
    ax[0].plot(_range, st.gaussian_kde(x)(_range))
    ax[1].hist(y, bins=11,  range  = (-5,6), normed=True, alpha=0.5,
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

print("Число эталонов:", n_standart,  "\n", "Список значений эталонов:", "\n",  standart)

for i in range(n_standart):
    print("Список максимумов значений эталона", i , "\n", sequence_max(standart[i]), "Всего максимумов:", sum(sequence_max(standart[i])))

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
    
print("Число образцов:",  n_sample)
#for i in range(n_sample):
#    print("Список максимумов значений образца", i , sequence_max(sample[i]), "Всего максимумов:", sum(sequence_max(sample[i])))

# Групповой по дням образец

#print("Групповой образец по дням:", "\n", sum_list(sample))

# Результаты статистического анализа по дням образцов со всеми эталонами

#print("Список максимумов значений группового образца по дням:", "\n", sequence_max(sum_list(sample)), "Всего максимумов:", sum(sequence_max(sum_list(sample))))


    # Групповой по пациентам образец для всех эталонов
    
print("Распределения максимумов и расстояний по пациентам для всех эталонов")

for i in range(n_standart):
    for j in range(len(sample)):
        print("Последовательность максимумов образца  ", j, "  и эталона  ", i, sequence_max(sample[j]), sum(sequence_max(sample[j])))
        print("Последовательность расстояний для образца  ", j, "  и эталона  ", i, sequence_distance(sequence_max(sample[j]), sequence_max(standart[i])), len(sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))))

concat_list = []    
for i in range(n_standart):
    concat = []
    k = 0
    for j in range(len(sample)):
        k += sum(sequence_max(sample[j]))
        concat  += sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))
    print("Распределение расстояний группы пациентов для эталона  ", i, concat, "Всего значений =  ", len(concat), k) 
    concat_list.append(concat)
    
#print("Распределение группы пациентов для всех эталонов:", "\n", concat_list, "Всего значений =  ", len(concat_list), len(concat_list[0])+len(concat_list[1])+len(concat_list[2]))
    
print("Результаты сравнительного визуального анализа по дням и по пациентам всех образцов со всеми эталонами")
    
for i in range(n_standart):
    print("Результаты визуального анализа для группового образца по дням и по пациентам для эталона ", i, "\n", visual_analys2(sequence_distance(sequence_max(sum_list(sample)), sequence_max(standart[i])),concat_list[i]))  
    print("Результаты тестирования нормальности распределения группового образца по дням для эталона ", i, "\n")
    test_normal(sequence_distance(sequence_max(sum_list(sample)), sequence_max(standart[i])))
    print("Результаты тестирования нормальности распределения группового образца по пациентам для эталона ", i, "\n")
    test_normal(concat_list[i])

print("Результаты статистического анализа распределений группы пациентов по дням и по пациентам для всех эталонов")

for i in range(n_standart):
    print("Результаты группового анализа по дням для эталона   ", i, "\n", "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] =  ", "\n" ,stat_analysis(sum_list(sample),standart[i]))
    print("Результаты группового анализа по пациентам для эталона   ", i, "\n", "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] =  ", "\n", stat_analys(concat_list[i]))
       
     

   
data = sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))
print(np.mean(data),  np.std(data), st.t.interval(0.95, len(data)-1, loc=np.mean(data), scale=st.sem(data)))    

print("Разультаты статистического анализа для группового образца по дням и эталона 0:  ",  "\n", "Выборочное среднее =  ", np.mean(sequence_distance(sequence_max(sum_list(sample)), sequence_max(standart[0]))),  "Стандартное отклонение =  ", np.std(sequence_distance(sequence_max(sum_list(sample)), sequence_max(standart[0]))), "Доверительный интервал =  ", st.t.interval(0.95, len(sequence_distance(sequence_max(sum_list(sample)), sequence_max(standart[0])))-1, loc=np.mean(sequence_distance(sequence_max(sum_list(sample)), sequence_max(standart[0]))), scale=st.sem(sequence_distance(sequence_max(sum_list(sample)), sequence_max(standart[0])))), "\n", test_normal())
print()


print("Результаты визуального анализа для группового образца по дням:", visual_analysis(sequence_distance(sequence_max(sum_list(sample)), sequence_max(standart[0]))))

print("Визуализация данных для группового образца по дням: гистограмма, ядерная оценка плотности распределения расстояний, плотность нормального распределения")
data = sequence_distance(sequence_max(sum_list(sample)), sequence_max(standart[0]))
fig, ax = plt.subplots()
_range = np.linspace(-4, 4, 100)
plt.style.use('seaborn-white')
ax.hist(data, bins=7,  range  = (-3,4), normed=True, alpha=0.5,
histtype='stepfilled', color='steelblue', edgecolor='none')
ax.plot(_range, norm.pdf(_range, np.mean(data), np.std(data)))
ax.plot(_range, st.gaussian_kde(data)(_range))
plt.show()    


for i in range(n_standart):
    print("Разультаты статистического анализа для эталона   ", i, "\n", "Выборочное среднее =     ",   "Стандартное отклонение =     ", "Доверительный интервал =")
    for j in range(n_sample):
        data = sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))
        print(np.mean(data),  np.std(data), st.t.interval(0.95, len(data)-1, loc=np.mean(data), scale=st.sem(data)))
        
        #ax.hist(data, bins=7,  range  = (-3,4), normed=True, alpha=0.5,
        #histtype='stepfilled', color='steelblue', edgecolor='none')        
        #_range = np.linspace(0.9 * np.min(data), 1.1 * np.max(data), 100)
        #plt.plot(_range, st.gaussian_kde(data)(_range), color = 'blue')           
        #plt.style.use('seaborn-white')
        #ax.set(xlim=(-4, 4), ylim=(0, 0.5),
        #xlabel='x', ylabel='', title='График ядерной оценки плотности распределения расстояний')
        #plt.show()
        
for i in range(n_standart):
    print("Визуализация данных: гистограмма, ядерная оценка плотности распределения расстояний, плотность нормального распределения")
    for j in range(n_sample):
        data = sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))
        fig, ax = plt.subplots()
        _range = np.linspace(-4, 4, 100)
        plt.style.use('seaborn-white')
        ax.hist(data, bins=7,  range  = (-3,4), normed=True, alpha=0.5,
        histtype='stepfilled', color='steelblue', edgecolor='none')
        ax.plot(_range, norm.pdf(_range, np.mean(data), np.std(data)))
        ax.plot(_range, st.gaussian_kde(data)(_range))
        #ax[1].plot(_range, norm.pdf(_range, np.mean(data), np.std(data)))
        #ax[1].plot(_range, st.gaussian_kde(data)(_range))
        plt.show()    

                
for i in range(n_standart):
    print("Визуализация данных: гистограмма, ядерной оценки плотности распределения расстояний, нормальное распределение")
    for j in range(n_sample):
        data = sequence_distance(sequence_max(sample[j]), sequence_max(standart[i]))
        fig, ax = plt.subplots(2)
        _range = np.linspace(-4, 4, 100)
        plt.style.use('seaborn-white')
        ax[0].hist(data, bins=7,  range  = (-3,4), normed=True, alpha=0.5,
        histtype='stepfilled', color='steelblue', edgecolor='none')
        ax[0].plot(_range, norm.pdf(_range, np.mean(data), np.std(data)))
                                
        ax[1].plot(_range, norm.pdf(_range, np.mean(data), np.std(data)))
        ax[1].plot(_range, st.gaussian_kde(data)(_range))
        plt.show()  
                                
print("Список значений пациента 1_1 без нагрузки:", data1, len(data1) )
                                
print("Список максимумов значений пациента 1_1 без нагрузки:", sequence_max(data1), len(sequence_max(data1)))

with open("1_1n.txt") as file:
    data2 = [row.strip() for row in file]
data2 = list(map(float, data2))
print("Список значений пациента 1_1 с физической нагрузкой:", data2)
print("Список максимумов значений пациента 1_1 с физической нагрузкой:", sequence_max(data2), len(sequence_max(data2)))

with open("1_1o.txt") as file:
    data3 = [row.strip() for row in file]
data3 = list(map(float, data3))
print("Список значений пациента 1_1 после отдыха:", data3)
print("Список максимумов значений пациента 1_1 после отдыха:", sequence_max(data3), len(sequence_max(data3)))

with open("1_1e.txt") as file:
    data4 = [row.strip() for row in file]
data4 = list(map(float, data4))
print("Список значений пациента 1_1 с эмоциональной нагрузкой:", data4)
print("Список максимумов значений пациента 1_1 с эмоциональной нагрузкой:", sequence_max(data4), len(sequence_max(data4)))


#вычисление распределения расстояний  от максимумов рядов пациентов до ближайшего максимума Kp 
print("Ряды расстояний и распределения расстояний от максимумов пациента 1_1 до ближайшего максимума Kp")
#вычисление последовательностей расстояний  от максимумов рядов пациентов до ближайшего максимума Kp 
xr1 = sequence_distance(sequence_max(data1), sequence_max(data))
xr2 = sequence_distance(sequence_max(data2), sequence_max(data))
xr3 = sequence_distance(sequence_max(data3), sequence_max(data))
xr4 = sequence_distance(sequence_max(data4), sequence_max(data))

#вычисление распределений расстояний  от максимумов рядов пациентов до ближайшего максимума Kp 
x1 = raspred(sequence_distance(sequence_max(data1), sequence_max(data)))
x2 = raspred(sequence_distance(sequence_max(data2), sequence_max(data)))
x3 = raspred(sequence_distance(sequence_max(data3), sequence_max(data)))
x4 = raspred(sequence_distance(sequence_max(data4), sequence_max(data)))

print("Ряд расстояний от максимумов пациента 1_1 без нагрузки до ближайшего максимума Kp:", xr1)
print("Распределение расстояний (значения от -3 до 3) пациента 1_1 без нагрузки:", x1)
print("Ряд расстояний от максимумов пациента 1_1 с физической нагрузкой до ближайшего максимума Kp:", xr2)
print("Распределение расстояний (значения от -3 до 3) пациента 1_1 с физической нагрузкой:", x2)
print("Ряд расстояний от максимумов пациента 1_1 после отдыха до ближайшего максимума Kp:", xr3)
print("Распределение расстояний (значения от -3 до 3) пациента 1_1 после отдыха:", x3)
print("Ряд расстояний от максимумов пациента 1_1 с эмоциональной нагрузкой до ближайшего максимума Kp:", xr4)
print("Распределение расстояний (значения от -3 до 3) пациента 1_1 с эмоциональной нагрузкой:", x4)

print("Анализ распределений расстояний от максимумов пациента 1_1 до ближайшего максимума Kp")
print("Анализ распределений расстояний пациента 1_1 без нагрузки:", "\n", "выборочное среднее =", np.mean(xr1), "стандартное отклонение =", np.std(xr1), "\n",  "Доверительный интервал:",  st.t.interval(0.95, len(xr1)-1, loc=np.mean(xr1), scale=st.sem(xr1)))

print("Анализ распределений расстояний пациента 1_1 с физической нагрузкой:", "\n", "выборочное среднее =", np.mean(xr2), "стандартное отклонение =", np.std(xr2), "\n",  "Доверительный интервал:", st.t.interval(0.95, len(xr2)-1, loc=np.mean(xr2), scale=st.sem(xr2)))

print("Анализ распределений расстояний пациента 1_1 после отдыха:", "\n", "выборочное среднее =", np.mean(xr3), "стандартное отклонение =", np.std(xr3), "\n", "Доверительный интервал:", st.t.interval(0.95, len(xr3)-1, loc=np.mean(xr3), scale=st.sem(xr3)))

print("Анализ распределений расстояний пациента 1_1 с эмоциональной нагрузкой:", "\n", "выборочное среднее =", np.mean(xr4), "стандартное отклонение =", np.std(xr4), "\n",  "Доверительный интервал:", st.t.interval(0.95, len(xr4)-1, loc=np.mean(xr4), scale=st.sem(xr4)))


#kwargs = dict(histtype='stepfilled', alpha=0.3, normed=True, bins=7)
#plt.hist(xr1, **kwargs)
#plt.hist(xr2, **kwargs)
#plt.hist(xr3, **kwargs)
#plt.hist(xr4, **kwargs)

_range = np.linspace(0.9 * np.min(xr1), 1.1 * np.max(xr1), 106)
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
