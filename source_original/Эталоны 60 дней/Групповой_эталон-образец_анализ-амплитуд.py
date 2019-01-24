# -*- coding: utf-8 -*-
from pylab import *
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import logistic,uniform,norm,pearsonr
import scipy.stats as st
from scipy.stats import gaussian_kde
from scipy.stats import shapiro
from scipy.stats import normaltest
from scipy.stats import anderson
import scipy.stats as stats

def len_ampl(x):
    """вычисление числа ненулевых элементов временного ряда"""
    y = 0
    for i in range(len(x)):
        if  x[i] != 0:
            y +=1 
    return y

def sequence_max(x):
    """вычисление максимумов временного ряда"""
    y = []
    for i in range(1,len(x)-1):
        if x[i-1] <= x[i] and x[i+1] <= x[i]:
            y.append(x[i])
        else: y.append(0)    
    return y

def sequence_max0(x):
    """вычисление индикаторов 1 максимумов временного ряда"""
    y = []
    for i in range(1,len(x)-1):
        if x[i-1] <= x[i] and x[i+1] <= x[i]:
            y.append(1)
        else: y.append(0)    
    return y

def index(x):
    """вычисление индексов ненулевых элементов временного ряда"""
    y = []
    for i in range(len(x)):
        if  x[i] != 0:
            y.append(i) 
    return y

#функция вычисления расстояний от максимумов образца до ближайшего максимумаэталона:
#"-" максимум эталона находится слева, "+" максимум эталона находится справа 
def sequence_distance(x, y):
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


def norm_serie(x):
    """Нормализация временного ряда"""
    y = []
    for i in range (len(x)):
        y.append((x[i] - min(x))/(max(x) - min(x)))
    return y

def delta_serie(x):
    """Приращения временного ряда"""
    y = []
    for i in range (1, len(x)):
        y.append((x[i] - x[i - 1]))
    return y

def sequence_max(x):
    """вычисление максимумов временного ряда"""
    y = []
    for i in range(1,len(x)-1):
        if x[i-1] <= x[i] and x[i+1] <= x[i]:
            y.append(x[i])
        else: y.append(0)    
    return y

def sequence_max1(x,v):
    """вычисление максимумов временного ряда с ограничением амплитуды"""
    y = []
    for i in range(1,len(x)-1):
        if x[i-1] <= x[i] and x[i+1] <= x[i] and x[i] > v:
            y.append(x[i])
        else: y.append(0)    
    return y
 
def sequence_max_ampl(x,v):
    """вычисление индикаторов 1 максимумов временного ряда с ограничением амплитуды"""
    y = []
    for i in range(1, len(x)-1):
        if x[i-1] <= x[i] and x[i+1] <= x[i] and x[i] > v:
            y.append(1)
        else: y.append(0)    
    return y

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

def stat_analys(z):
    """Статистический анализ ряда распределений"""
    return    [np.mean(z), np.std(z), st.t.interval(0.95, len(z)-1, loc=np.mean(z), scale=st.sem(z))]

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

def func(x, y):
    """ Суммирование почленное элементов двух разных списков """
    return x + y  

def sum_list(x):
    """Почленное суммирование списков списка"""
    y = [0]*len(x[0])
    for i in range(len(x)):
        y = list( map(func, y, x[i]) )
    return y

def sum_max_lists(x):
    """Почленное суммирование максимумов списков списка"""
    y = sequence_max0(x[0])
    for i in range(1,len(x)):
        y = list( map(func, y, sequence_max0(x[i])))
    return y

standart = []
n_standart = 0
with open("Kp_60.txt") as file:
    standart.append(list(map(float, [row.strip() for row in file])))
    n_standart += 1
with open("Скор.ветра_60.txt") as file:
    standart.append(list(map(float, [row.strip() for row in file])))
    n_standart += 1
with open("T_60.txt") as file:
    standart.append(list(map(float, [row.strip() for row in file])))
    n_standart += 1
with open("f_60.txt") as file:
    standart.append(list(map(float, [row.strip() for row in file])))
    n_standart += 1
with open("Po_60.txt") as file:
    standart.append(list(map(float, [row.strip() for row in file])))
    n_standart += 1
with open("BX_60.txt") as file:
    standart.append(list(map(float, [row.strip() for row in file])))
    n_standart += 1
with open("BY_60.txt") as file:
    standart.append(list(map(float, [row.strip() for row in file])))
    n_standart += 1
with open("BZ_60.txt") as file:
    standart.append(list(map(float, [row.strip() for row in file])))
    n_standart += 1
with open("SW_60.txt") as file:
    standart.append(list(map(float, [row.strip() for row in file])))
    n_standart += 1
with open("SWP_60.txt") as file:
    standart.append(list(map(float, [row.strip() for row in file])))
    n_standart += 1
with open("Flow_60.txt") as file:
    standart.append(list(map(float, [row.strip() for row in file])))
    n_standart += 1


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


#Анализ синхронизации максимумов амплитуд значений эталонов с максимумами группы фактор-образцов без нагрузки

for j in range(n_standart): 
    print("Список максимумов значений эталона", j, "среднее значение", np.mean(standart[j]) , "\n" , sequence_max1(standart[j], np.mean(standart[j])), "\n" , index(sequence_max1(standart[j], np.mean(standart[j]))), "Всего максимумов:", len_ampl(sequence_max1(standart[j], np.mean(standart[j]))))
    print("Список максимумов значений эталона", j, "среднее значение", np.mean(standart[j]) , "\n" , sequence_max_ampl(standart[j], np.mean(standart[j])), "\n" , index(sequence_max_ampl(standart[j], np.mean(standart[j]))), "Всего максимумов:", sum(sequence_max_ampl(standart[j], np.mean(standart[j]))))

print("Распределение расстояний максимумов амплитуд значений эталонов до максимумов группы фактор-образцов без нагрузки")
for j in range(n_standart): print("Для эталона", j,  sequence_distance(sequence_max_ampl(standart[j], np.mean(standart[j])), sequence_max0(sum_list(sample))), sum(sequence_max0(standart[j])))

print("Результат статистического анализа распределения расстояний максимумов амплитуд значений эталонов до максимумов группы  фактор-образцов без нагрузки")
for j in range(n_standart): print("Для эталона", j, "\n",  "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] =  ", "\n" , stat_analys(sequence_distance(sequence_max_ampl(standart[j], np.mean(standart[j])), sequence_max0(sum_list(sample)))))

print("Результаты тестирования нормальности распределения расстояний  максимумов амплитуд значений эталонов до максимумов группы  фактор-образцов без нагрузки")
for j in range(n_standart): print("Для эталона", j, 
	test_normal(sequence_distance(sequence_max_ampl(standart[j], np.mean(standart[j])), sequence_max0(sum_list(sample)))))
        
print("Результаты визуального анализа распределения расстояний максимумов амплитуд значений эталонов до максимумов группы  фактор-образцов без нагрузки")
for j in range(n_standart): print("Для эталона", j,  visual_analysis(sequence_distance(sequence_max_ampl(standart[j], np.mean(standart[j])), sequence_max0(sum_list(sample)))))

print("Распределение расстояний максимумов амплитуд значений эталонов до максимумов фактор-образцов без нагрузки")
for j in range(n_standart):
    for i in range(n_sample): print("Для эталона", j, "и образца", i, sequence_distance(sequence_max_ampl(standart[j], np.mean(standart[j])), sequence_max0(sample[i])), sum(sequence_max_ampl(standart[j], np.mean(standart[j]))))

print("Результат статистического анализа распределения расстояний максимумов амплитуд значений эталонов до максимумов фактор-образцов без нагрузки")
for j in range(n_standart):
    for i in range(n_sample): print("Для эталона", j, "и образца", i,  "\n",  "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] =  ", "\n" , stat_analys(sequence_distance(sequence_max_ampl(standart[j], np.mean(standart[j])), sequence_max0(sample[i]))))

print("Результаты тестирования нормальности распределения расстояний  максимумов  амплитуд значений эталонов до максимумов фактор-образцов без нагрузки")
for j in range(n_standart):
    for i in range(n_sample): print("Для эталона", j, "и образца", i, 
	test_normal(sequence_distance(sequence_max_ampl(standart[j], np.mean(standart[j])), sequence_max0(sample[i]))))
        
print("Результаты визуального анализа распределения расстояний максимумов значений эталонов до максимумов фактор-образцов без нагрузки")
for j in range(n_standart):
    for i in range(n_sample): print("Для эталона", j, "и образца", i,  visual_analysis(sequence_distance(sequence_max_ampl(standart[j], np.mean(standart[j])), sequence_max0(sample[i]))))

#print("Список всех максимумов значений образца","\n" , sequence_max1(sample[0], 0), "\n" , index(sequence_max1(sample[0], 0)), "Всего максимумов:", len_ampl(sequence_max1(sample[0], 0)))

#print("Распределение расстояний максимумов фактор-образца без нагрузки для образца  ", 0)
#for i in range(n_standart): print("Для эталона  ", i, sequence_distance(sequence_max1(sample[0], np.mean(sample[0])), sequence_max1(standart[i], np.mean(standart[i]))), "\n" , sequence_distance(sequence_max1(sample[0], 0), sequence_max1(standart[i], min(standart[i]))), len_ampl(sequence_max1(sample[0], 0)))    





#Анализ синхронизации максимумов значений эталонов с максимумами группы фактор-образцов без нагрузки


#print("Список максимумов значений эталонов") 
#for i in range(n_standart): print("Для эталона", i , sequence_max0(standart[i]),  index(sequence_max0(standart[i])), "Всего максимумов:", len_ampl(sequence_max0(standart[i])))


print("Распределение расстояний максимумов значений эталонов до максимумов фактор-образцов без нагрузки")
for j in range(n_standart):
    for i in range(n_sample): print("Для эталона", j, "и образца", i, sequence_distance(sequence_max0(standart[j]), sequence_max0(sample[i])), sum(sequence_max0(standart[j])))

print("Результат статистического анализа распределения расстояний максимумов значений эталонов до максимумов фактор-образцов без нагрузки")
for j in range(n_standart):
    for i in range(n_sample): print("Для эталона", j, "и образца", i,  "\n",  "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] =  ", "\n" , stat_analys(sequence_distance(sequence_max0(standart[j]), sequence_max0(sample[i]))))

print("Результаты тестирования нормальности распределения расстояний  максимумов значений эталонов до максимумов фактор-образцов без нагрузки")
for j in range(n_standart):
    for i in range(n_sample): print("Для эталона", j, "и образца", i, 
	test_normal(sequence_distance(sequence_max0(standart[j]), sequence_max0(sample[i]))))
        
print("Результаты визуального анализа распределения расстояний максимумов значений эталонов до максимумов фактор-образцов без нагрузки")
for j in range(n_standart):
    for i in range(n_sample): print("Для эталона", j, "и образца", i,  visual_analysis(sequence_distance(sequence_max0(standart[j]), sequence_max0(sample[i]))))



print("Распределение расстояний максимумов значений эталона 0 до максимумов фактор-образцов без нагрузки")
for i in range(n_sample): print("Для образца", i, sequence_distance(sequence_max0(standart[0]), sequence_max0(sample[i])), sum(sequence_max0(standart[0])))

print("Результаты тестирования нормальности распределения расстояний  максимумов значений эталона 0 до максимумов фактор-образцов без нагрузки")
for i in range(n_sample): print("Для образца  ", i, "\n", 
	test_normal(sequence_distance(sequence_max0(standart[0]), sequence_max0(sample[i]))))
        
print("Результаты визуального анализа распределения расстояний максимумов значений эталона 0 до максимумов фактор-образцов без нагрузки")
for i in range(n_sample): print("Для образца  ", i, "\n", visual_analysis(sequence_distance(sequence_max0(standart[0]), sequence_max0(sample[i]))))


print("Результат статистического анализа распределения расстояний максимумов значений эталона 0 до всех максимумов фактор-образцов без нагрузки")
for i in range(n_sample): print("Для образца  ", i, "\n",  "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] =  ", "\n" , stat_analys(sequence_distance(sequence_max0(standart[0]), sequence_max0(sample[i]))))






print("Распределение расстояний максимумов фактор-образцов без нагрузки до всех максимумов значений группы эталонов")
for i in range(n_sample): print("Для образца", i, sequence_distance(sequence_max0(sample[i]), sum_max_lists(standart)), sum(sequence_max0(sample[i])))
 
print("Распределение расстояний максимумов фактор-образцов с физической нагрузкой до  всех максимумов значений группы эталонов")
for i in range(n_sample_n): print("Для образца", i, sequence_distance(sequence_max0(sample_n[i]),sum_max_lists(standart)), sum(sequence_max0(sample_n[i])))

print("Распределение расстояний максимумов фактор-образцов с эмоциональной нагрузкой до  всех максимумов значений группы эталонов")
for i in range(n_sample_e): print("Для образца", i, sequence_distance(sequence_max0(sample_e[i]), sum_max_lists(standart)), sum(sequence_max0(sample_e[i])))

print("Распределение расстояний максимумов фактор-образцов после отдыха до  всех максимумов значений группы эталонов")
for i in range(n_sample_o): print("Для образца", i, sequence_distance(sequence_max0(sample_o[i]), sum_max_lists(standart)), sum(sequence_max0(sample_o[i])))
			
#print("Список максимумов значений образца, среднее значение", np.mean(sample[0]) , "\n" , sequence_max1(sample[0], np.mean(sample[0])), "\n" , index(sequence_max1(sample[0], np.mean(sample[0]))), "Всего максимумов:", len_ampl(sequence_max1(sample[0], np.mean(sample[0]))))
#print("Список всех максимумов значений образца","\n" , sequence_max1(sample[0], 0), "\n" , index(sequence_max1(sample[0], 0)), "Всего максимумов:", len_ampl(sequence_max1(sample[0], 0)))

#print("Распределение расстояний максимумов фактор-образца без нагрузки для образца  ", 0)
#for i in range(n_standart): print("Для эталона  ", i, sequence_distance(sequence_max1(sample[0], np.mean(sample[0])), sequence_max1(standart[i], np.mean(standart[i]))), "\n" , sequence_distance(sequence_max1(sample[0], 0), sequence_max1(standart[i], min(standart[i]))), len_ampl(sequence_max1(sample[0], 0)))

#print("Результат статистического анализа распределения расстояний максимумов фактор-образца без нагрузки для образца  ", 0)
#for i in range(n_standart): print("для эталона", i,  "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] =  ", "\n" , stat_analys(sequence_distance(sequence_max1(sample[0], np.mean(sample[0])), sequence_max1(standart[i], np.mean(standart[i])))), "\n" , "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] =  ", "\n" , stat_analys(sequence_distance(sequence_max1(sample[0], 0), sequence_max1(standart[i], min(standart[i])))))


#print("Результаты визуального анализа распределения расстояний максимумов фактор-образца без нагрузки для образца  ", 0)
#for i in range(n_standart): print("Для эталона  ", i, visual_analysis(sequence_distance(sequence_max1(sample[0], np.mean(sample[0])), sequence_max1(standart[i], np.mean(standart[i])))), "\n" , visual_analysis(sequence_distance(sequence_max1(sample[0], 0), sequence_max1(standart[i], min(standart[i])))))


print("Результаты тестирования нормальности распределения расстояний максимумов фактор-образца без нагрузки для образца  ", 0)
for i in range(n_standart): print("Для эталона  ", i, "\n", 
	test_normal(sequence_distance(sequence_max1(sample[0], np.mean(sample[0])), sequence_max1(standart[i], np.mean(standart[i])))), "\n", 
	test_normal(sequence_distance(sequence_max1(sample[0], 0), sequence_max1(standart[i], min(standart[i])))))
print("Результаты визуального анализа распределения расстояний максимумов фактор-образца без нагрузки для образца  ", 0, "  после эталона  ", 0, visual_analysis(sequence_distance_l(sequence_max(sample[0]), sequence_max(standart[0]))))
print("Результат статистического анализа распределения расстояний максимумов фактор-образца без нагрузки для образца  ", 0, "  и до эталона  ", 0, "\n",  "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] =  ", "\n" , stat_analys(sequence_distance_r(sequence_max(sample[0]), sequence_max(standart[0]))))
print("Результат статистического анализа распределения расстояний максимумов фактор-образца без нагрузки для образца  ", 0, "  и после эталона  ", 0, "\n",  "[Выборочное среднее, Стандартное отклонение,  Доверительный интервал] =  ", "\n" , stat_analys(sequence_distance_l(sequence_max(sample[0]), sequence_max(standart[0]))))
print("Результаты тестирования нормальности распределения расстояний мин-максимумов фактор-образца без нагрузки для образца  ", 0, "  и эталона  ", 0, "\n", 
	test_normal(sequence_distance_r(sequence_min(sample[0]), sequence_max(standart[0]))))
print("Результаты тестирования нормальности распределения расстояний мин-максимумов фактор-образца без нагрузки для образца  ", 0, "  и эталона  ", 0, "\n", 
	test_normal(sequence_distance_l(sequence_min(sample[0]), sequence_max(standart[0]))))
plt.style.use('seaborn-white')
ax[0].plot(data)
ax[1].plot(sequence_max(data))
ax[2].plot(data1, color = 'red')
ax[3].plot(sequence_max(data1), color = 'red')
plt.show()

print("Значения Kp")
print(data)
print(delta_serie(norm_serie(data)))
print(sequence_max(norm_serie(data)))
print("Значения 1_1")
print(data1)
print(delta_serie(norm_serie(data1)))
print(sequence_max(norm_serie(data1)))



#Чтобы русские символы отображались корректно на графике
rcParams['font.family'] = ['Liberation serif']
plot(delta_serie(data),  color = 'blue')
#plot(norm_serie(delta_serie(data1)), color = 'red')
#plot(data2, color = 'green')
#plot(data3, color = 'yellow')
title(u'синий график - без нагрузки, красный график  - с физ.нагрузкой, \n  зеленый график - после отдыха, желтый график - с эмоц.нагрузкой')
xlabel(u'Дни')
ylabel(u'Значение Т-зубца')
show()


plot(data1)
plot(data2)
title(u'Коэффициент корреляции в зависимости от сдвига')
xlabel(u'Сдвиг')
ylabel(u'Коэффициент корреляции')
show()
print("Распределение значений фактор-образцов для пациента")



print('Коэффициент корреляции Пирсона для двух совокупностей данных:', np.corrcoef(data1, data2)[0,1])

def custom_corr(data1, data2):
    '''
    Вспомогательная функция, вычисляющая корреляции с учетом сдвига
    '''
    return [np.corrcoef(data2[j:],data1[: len(data1) - j])[0,1] for j in range(8)]
print(custom_corr(data1, data2))

print('Максимальная корреляция с учетом возможных сдвигов ', max(custom_corr(data1,data2)))
#print('Максимальная по абсолютной величине корреляция с учетом возможных сдвигов ', max(np.abs(custom_corr(data1,data2))))


def norm_serie(x):
    """Нормализация временного ряда"""
    y = []
    for i in range (len(x)):
        y.append((x[i] - min(x))/(max(x) - min(x)))
    return y


      
def lineplot(x_data, y_data, x_label="", y_label="", title=""):
    # Create the plot object
    _, ax = plt.subplots()

    # Plot the best fit line, set the linewidth (lw), color and
    # transparency (alpha) of the line
    ax.plot(x_data, y_data, lw = 2, color = '#539caf', alpha = 1)

    # Label the axes and provide a title
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    
