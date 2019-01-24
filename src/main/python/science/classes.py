import science
import science.funcs as funcs

import numpy as np

DATA_LENGTH_DEFAULT = -1
DATA_LENGTH = DATA_LENGTH_DEFAULT
GROUP_SAMPLE_NAME = 'group'


class Sample:
    samples = {}
    group = None

    def __init__(self, name, datas):
        # проверка параметров
        Sample.handle_init(name, datas)
        # инициализация атрибутов
        self.name = name
        self.data, self.seq_max, self.seq_max0 = [], [], []
        for data in datas:
            self.data.append(data)
            self.seq_max.append(data if data is None else funcs.sequence_max(data))
            self.seq_max0.append(data if data is None else funcs.sequence_max0(data))
        # добавление образца в глобальный список
        if name != GROUP_SAMPLE_NAME:
            Sample.samples[name] = self
        # обновление группового образца
        self.handle_group()

    def delete(self):
        if self.name == GROUP_SAMPLE_NAME:
            raise science.ClassesError('Невозможно удалить групповой образец')
        # обновляем групповой образец
        for factor in range(4):
            for idx in range(DATA_LENGTH):
                Sample.group.data[factor][idx] -= self.data[factor][idx]
        Sample.group.seq_max = [funcs.sequence_max(data) for data in Sample.group.data]
        Sample.group.seq_max0 = [funcs.sequence_max0(data) for data in Sample.group.data]
        # удаляем образец из глобального списка
        del Sample.samples[self.name]

    @staticmethod
    def from_file(filename):
        name = science.file_base_name(filename)
        try:
            datas = science.read_xlsx_sample(filename)
        except science.ParseError as e:
            raise science.ClassesError(e.args[0])
        return Sample(name, datas)

    @staticmethod
    def handle_init(name, datas):
        # проверка дубликатов
        if name in Sample.samples:
            raise science.ClassesError('Образец с именем {} уже загружен'.format(name))
        # все данные должны быть одной длины
        global DATA_LENGTH
        if DATA_LENGTH == DATA_LENGTH_DEFAULT:
            DATA_LENGTH = len(datas[0])
            print('DATA_LENGTH =', DATA_LENGTH)
        if any([len(datas[factor]) != DATA_LENGTH for factor in range(4)]):
            raise science.ClassesError('Для образца {} переданы некорректные данные: '
                                       'проверьте количество данных для каждого фактора'.format(name))

    def handle_group(self):
        if self.name == GROUP_SAMPLE_NAME:
            return
        if Sample.group is None:
            datas = [[0] * DATA_LENGTH for _factor in range(4)]
            Sample.group = Sample(GROUP_SAMPLE_NAME, datas)
            print('Групповой образец инициализирован')
        # обновляем групповой образец
        for factor in range(4):
            for idx in range(DATA_LENGTH):
                Sample.group.data[factor][idx] += self.data[factor][idx]
        Sample.group.seq_max = [funcs.sequence_max(data) for data in Sample.group.data]
        Sample.group.seq_max0 = [funcs.sequence_max0(data) for data in Sample.group.data]

    def display(self):
        if self.name == GROUP_SAMPLE_NAME:
            return "Групповой образец"
        else:
            return "Образец: " + self.name

    def display_file(self, factor=science.FACTORS_ALL):
        fname = self.display().replace(":", "")
        if factor != science.FACTORS_ALL:
            fname += " " + science.FACTORS_L[factor]
        return fname

    @staticmethod
    def display_file_group(factor=science.FACTORS_ALL):
        fname = "Группа образцов"
        if factor != science.FACTORS_ALL:
            fname += " " + science.FACTORS_L[factor]
        return fname

    def display_g(self):
        if self.name == GROUP_SAMPLE_NAME:
            return "группового образца"
        else:
            return "образца " + self.name


class Standard:
    standards = {}

    def __init__(self, name, data):
        # проверка параметров
        Standard.handle_init(name, data)
        # инициализация атрибутов
        self.name = name
        self.data = data
        self.seq_max = funcs.sequence_max(self.data)
        self.seq_max0 = funcs.sequence_max0(self.data)
        self.seq_max_apl = funcs.sequence_max_ampl(self.data, np.mean(self.data))
        # добавление эталона в глобальный список
        Standard.standards[name] = self

    def delete(self):
        del Standard.standards[self.name]

    @staticmethod
    def from_file(filename: str):
        name = science.file_base_name(filename)
        try:
            data = science.read_sample(filename)
        except science.ParseError as e:
            raise science.ClassesError(e.args[0])
        return Standard(name, data)

    @staticmethod
    def handle_init(name, data):
        # проверка дубликатов
        if name in Standard.standards:
            raise science.ClassesError('Эталон с именем {} уже загружен'.format(name))
        # все данные должны быть одной длины
        global DATA_LENGTH
        if DATA_LENGTH == DATA_LENGTH_DEFAULT:
            DATA_LENGTH = len(data)
            print('DATA_LENGTH =', DATA_LENGTH)
        if len(data) != DATA_LENGTH:
            raise science.ClassesError('Для эталона {} переданы некорректные данные: '
                                       'проверьте количество данных'.format(name))

    def display(self):
        return "Погода: " + self.name

    def display_file(self):
        return self.display().replace(":", "")


if __name__ == '__main__':
    s1 = Sample('s1', [[1, 1], [2, 2], [1, 1], [2, 2]])
    s2 = Sample('s2', [[3, 3], [100, 100], [1, 1], [0, 0]])
    s1.delete()
    assert Sample.group.data[0][0] == 3
    assert Sample.group.data[3][-1] == 0
