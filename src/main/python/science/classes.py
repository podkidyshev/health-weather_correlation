import science
import science.funcs as funcs


class PatientDuplicateError(Exception):
    pass


class Patient:
    patients = {}

    def __init__(self, name, datas):
        if name in Patient.patients:
            raise PatientDuplicateError('Пациент с именем {} уже загружен'.format(name))
        Patient.patients[name] = self

        self.name = name
        self.data, self.seq_max = [], []
        for data in datas:
            self.data.append(data)
            self.seq_max.append(data if data is None else funcs.sequence_max(data))

    def has_factor(self, factor: int):
        return self.data[factor] is not None

    def delete(self):
        del Patient.patients[self.name]

    @staticmethod
    def from_file(filename, name: str=""):
        if not name:
            name = science.file_base_name(filename)
        datas = science.read_xlsx_sample(filename)
        return Patient(name, datas)


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
        self.seq_max = funcs.sequence_max(self.data)

    def delete(self):
        del Standard.standards[self.name]

    @staticmethod
    def from_file(filename: str, name: str=""):
        if not name:
            name = science.file_base_name(filename)
        data = science.read_sample(filename)
        return Standard(name, data)

    @staticmethod
    def cleanup():
        Standard.standards.clear()


def test_structure():
    pass


if __name__ == '__main__':
    test_structure()
