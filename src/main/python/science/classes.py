from science import *
from science.funcs import sequence_max


class PatientDuplicateError(Exception):
    pass


class Patient:
    patients = {}

    def __init__(self, name):
        if name in Patient.patients:
            raise PatientDuplicateError('Пациент с именем {} уже загружен'.format(name))
        Patient.patients[name] = self

        self.name = name
        self.data = [None] * len(CATS)
        self.data_seq_max = [None] * len(CATS)

    def has_category(self, cat):
        return self.data[cat_index(cat)] is not None

    def _add_category(self, cat, data: list):
        cat = cat_index(cat)
        self.data[cat] = data
        self.data_seq_max[cat] = sequence_max(data)

    def add_category(self, cat, filename: str):
        data = read_sample(filename)
        self._add_category(cat, data)

    def delete(self):
        del Patient.patients[self.name]


class StandardDuplicateError(Exception):
    pass


class Standard:
    standards = {}

    def __init__(self, name, data):
        if name in Standard.standards:
            raise StandardDuplicateError('Эталон {} уже загружен'.format(name))
        Standard.standards[name] = self

        self.name = name
        self.data = data
        self.seq_max = sequence_max(self.data)

    def delete(self):
        del Standard.standards[self.name]

    @staticmethod
    def from_file(filename: str, name: str=""):
        if not name:
            name = file_base_name(filename)
        data = read_sample(filename)
        return Standard(name, data)

    @staticmethod
    def cleanup():
        Standard.standards.clear()
