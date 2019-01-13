import science
import science.funcs as funcs

import numpy as np

DATA_LENGTH_DEFAULT = -1
DATA_LENGTH = DATA_LENGTH_DEFAULT
GROUP_SAMPLE_NAME = 'group'


class Sample:
    class SampleError(Exception):
        pass

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
            raise Sample.SampleError('Невозможно удалить групповой образец')
        # обновляем групповой образец
        for factor in range(4):
            for idx in range(DATA_LENGTH):
                Sample.group.data[factor][idx] -= self.data[factor][idx]
        # удаляем образец из глобального списка
        del Sample.samples[self.name]

    @staticmethod
    def from_file(filename, name: str = ""):
        if not name:
            name = science.file_base_name(filename)
            if name == "":
                return None
        datas = science.read_xlsx_sample(filename)
        return Sample(name, datas)

    @staticmethod
    def handle_init(name, datas):
        # проверка дубликатов
        if name in Sample.samples:
            raise Sample.SampleError('Образец с именем {} уже загружен'.format(name))
        # все данные должны быть одной длины
        global DATA_LENGTH
        if DATA_LENGTH == DATA_LENGTH_DEFAULT:
            DATA_LENGTH = len(datas[0])
            print('DATA_LENGTH =', DATA_LENGTH)
        if any([len(datas[factor]) != DATA_LENGTH for factor in range(4)]):
            raise Sample.SampleError('Для образца {} переданы некорректные данные: '
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
        Sample.samples[GROUP_SAMPLE_NAME] = Sample.group


class Standard:
    class StandardError(Exception):
        pass

    standards = {}

    def __init__(self, name, data):
        # проверка параметров
        Standard.handle_init(name, data)
        # инициализация атрибутов
        self.name = name
        self.data = data
        self.seq_max = funcs.sequence_max(self.data)
        self.seq_max_apl = funcs.sequence_max_ampl(self.data, np.mean(self.data))
        # добавление эталона в глобальный список
        Standard.standards[name] = self

    def delete(self):
        del Standard.standards[self.name]

    @staticmethod
    def from_file(filename: str, name: str = ""):
        if not name:
            name = science.file_base_name(filename)
        data = science.read_sample(filename)
        return Standard(name, data)

    @staticmethod
    def handle_init(name, data):
        # проверка дубликатов
        if name in Standard.standards:
            raise Standard.StandardError('Эталон с именем {} уже загружен'.format(name))
        # # все данные должны быть одной длины
        # global DATA_LENGTH
        # if DATA_LENGTH == DATA_LENGTH_DEFAULT:
        #     DATA_LENGTH = len(data)
        #     print('DATA_LENGTH =', DATA_LENGTH)
        # if len(data) != DATA_LENGTH:
        #     raise Sample.SampleError('Для эталона {} переданы некорректные данные: '
        #                              'проверьте количество данных'.format(name))


if __name__ == '__main__':
    s1 = Sample('s1', [[1, 1], [2, 2], [1, 1], [2, 2]])
    s2 = Sample('s2', [[3, 3], [100, 100], [1, 1], [0, 0]])
    s1.delete()
    assert Sample.group.data[0][0] == 3
    assert Sample.group.data[3][-1] == 0


# TODO: в эталоне BX_62.txt - 62 элемента, а в образцах по 60 элементов: как контролировать?
