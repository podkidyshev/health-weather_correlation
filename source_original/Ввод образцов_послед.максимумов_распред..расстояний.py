#-*- coding: utf-8 -*-
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from scipy.stats import logistic,uniform,norm,pearsonr
from numpy import sqrt,pi,e
import numpy as np

fig, ax = plt.subplots(1, 1)
n=1000# объём выборки
x = np.arange(-3, 4, 0.01)

#функция вычисления максимумов временного ряда
def sequence_max(x): 
    y = []
    for i in range(1,len(x)-1):
        if x[i-1] <= x[i] and x[i+1] <= x[i]:
            y.append(1)
        else: y.append(0)    
    return y

#функция вычисления расстояний от максимумов ряда пациента до ближайшего максимума Kp:
#"-" максимум Kp находится слева, "+" максимум Kp находится справа 
def sequence_distance(x, y):
    u = []   
    for i in range(len(x)): 
        if x[i] == 1:
            for j in range(len(y)):
                if ( i - j >= 0 and y[i - j + 1] == 1) and ( i + j < len(y) and y[i + j + 1] == 1):
                    if j == 0:
                        u.append(j)
                    else:
                        u.append(j)
                        u.append(-j)
                    break                     
                elif ( i - j >= 0 and y[i - j + 1] == 1) :
                    u.append(j)
                    break
                elif ( i + j < len(y) and y[i + j + 1] == 1):
                    u.append(-j)
                    break                    
    return u

#функция вычисления распределения расстояний от максимумов ряда пациента до ближайшего максимума Kp 
def raspred(x):
    y = []
    for i in range(7):
        y.append(x.count(i-3)) 
    return y

#загрузка списка Kp и списков пациентов группы
with open("Kp_62.txt") as file:
    data = [row.strip() for row in file]
data = list(map(float, data))
print("Список Кр-значений:", data, len(data))
print("Список максимумов Кр-значений:", sequence_max(data), len(sequence_max(data)))

with open("1_1.txt") as file:
    data1 = [row.strip() for row in file]
data1 = list(map(float, data1))
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
print("Распределение расстояний (значения от -3 до 3) пациента 1_1 с эмоциональной нагрузкой:", xr4)

print("Анализ распределений расстояний от максимумов пациента 1_1 до ближайшего максимума Kp")
print("Анализ распределений расстояний пациента 1_1 без нагрузки",  "выборочное среднее =", np.mean(xr1), "стандартное отклонение =", np.std(xr1), "\n", "радиус интервала =", 2.10*np.std(xr1)/sqrt(len(xr1)-1), "Доверительный интервал:", [np.mean(xr1) - 2.10*np.std(xr1)/sqrt(len(xr1)-1), np.mean(xr1) + 2.10*np.std(xr1)/sqrt(len(xr1)-1)])

print("Анализ распределений расстояний пациента 1_1 с физической нагрузкой:", "выборочное среднее =", np.mean(xr2), "стандартное отклонение =", np.std(xr2), "\n", "радиус интервала =", 2.13*np.std(xr2)/sqrt(len(xr2)-1), "Доверительный интервал:", [np.mean(xr2)- 2.13*np.std(xr2)/sqrt(len(xr2)-1), np.mean(xr2) + 2.13*np.std(xr2)/sqrt(len(xr2)-1)])

print("Анализ распределений расстояний пациента 1_1 после отдыха:", "выборочное среднее =", np.mean(xr3), "стандартное отклонение =", np.std(xr3), "\n", "радиус интервала =", 2.09*np.std(xr3)/sqrt(len(xr3)-1), "Доверительный интервал:", [np.mean(xr3)- 2.09*np.std(xr3)/sqrt(len(xr3)-1), np.mean(xr3) + 2.09*np.std(xr3)/sqrt(len(xr3)-1)])

print("Анализ распределений расстояний пациента 1_1 с эмоциональной нагрузкой:", "выборочное среднее =", np.mean(xr4), "стандартное отклонение =", np.std(xr4), "\n", "радиус интервала =", 2.18*np.std(xr4)/sqrt(len(xr4)-1), "Доверительный интервал:", [np.mean(xr4)- 2.18*np.std(xr4)/sqrt(len(xr4)-1), np.mean(xr4) + 2.18*np.std(xr4)/sqrt(len(xr4)-1)])


