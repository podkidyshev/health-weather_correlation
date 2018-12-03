import os
import sys


def sequence_max(x):
    """функция вычисления максимумов временного ряда"""
    y = []
    for i in range(1, len(x) - 1):
        if x[i - 1] <= x[i] and x[i + 1] <= x[i]:
            y.append(1)
        else:
            y.append(0)
    return y


def sequence_distance(x, y):
    """
    функция вычисления расстояний от максимумов ряда пациента до ближайшего максимума Kp:
    "-" максимум Kp находится слева, "+" максимум Kp находится справа
    """
    x.insert(0, 0)
    u = []
    for i in range(len(x)):
        if x[i] == 1:
            for j in range(len(y)):
                if (i - j >= 0 and y[i - j] == 1) and (i + j < len(y) and y[i + j] == 1):
                    if j == 0:
                        u.append(j)
                    else:
                        u.append(j)
                        u.append(-j)
                    break
                elif i - j >= 0 and y[i - j] == 1:
                    u.append(j)
                    break
                elif i + j < len(y) and y[i + j] == 1:
                    u.append(-j)
                    break
    return u


def distrib(x):
    """функция вычисления распределения расстояний от максимумов ряда пациента до ближайшего максимума Kp"""
    y = []
    for i in range(7):
        y.append(x.count(i - 3))
    return y


class FakePrint:
    def __init__(self):
        self.log = []
        self.orig_stdout = sys.stdout

    def write(self, *args):
        self.log.append(' '.join(map(str, args)))

    def activate(self):
        sys.stdout = self

    def deactivate(self):
        sys.stdout = self.orig_stdout

    def force_print(self, *args, **kwargs):
        self.orig_stdout.write(*args, **kwargs)


def read_sample(filename):
    """Чтение образцов и эталонов"""
    with open(filename) as file:
        data = [row.strip() for row in file]

    for idx, el in enumerate(data):
        data[idx] = float(el)
    return data


def read_test_sample(filename):
    return read_sample(os.path.join('samples', filename))


def patient_suffix(filename: str, suffix):
    return filename[:filename.rfind('.')] + suffix + filename[filename.rfind('.') + 1:]