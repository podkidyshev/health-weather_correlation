import science
from science.funcs import sequence_max


class GroupDuplicateError(Exception):
    pass


class GroupPatientNotFoundError(Exception):
    pass


class Group:
    groups = {}

    def __init__(self, name):
        if name in Group.groups:
            raise GroupDuplicateError('Группа с именем {} уже существует'.format(name))
        Group.groups[name] = self

        self.name = name
        self.pats = {}

    def add_pat(self, pat):
        self.pats[pat.name] = pat

    def delete(self):
        for pat in self.pats.values():
            pat._delete()
        del Group.groups[self.name]

    def delete_pat(self, pat):
        if pat.name not in self.pats:
            raise GroupPatientNotFoundError('Пациент {} не найден в группе {}'.format(pat.name, self.name))
        del self.pats[pat.name]
        pat._delete()


class PatientDuplicateError(Exception):
    pass


class Patient:
    patients = {}

    def __init__(self, name, group_name):
        if name in Patient.patients:
            raise PatientDuplicateError('Пациент с именем {} уже загружен'.format(name))
        Patient.patients[name] = self

        self.name = name
        self.data = [None] * len(science.CATS)
        self.data_seq_max = [None] * len(science.CATS)

        self.group = Group.groups[group_name]
        self.group.add_pat(self)

    def has_category(self, cat):
        return self.data[science.cat_index(cat)] is not None

    def _add_category(self, cat, data: list):
        cat = science.cat_index(cat)
        self.data[cat] = data
        self.data_seq_max[cat] = sequence_max(data)

    def add_category(self, cat, filename: str):
        data = science.read_sample(filename)
        self._add_category(cat, data)

    def _delete(self):
        del Patient.patients[self.name]

    def delete(self):
        self.group.delete_pat(self)


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
            name = science.file_base_name(filename)
        data = science.read_sample(filename)
        return Standard(name, data)

    @staticmethod
    def cleanup():
        Standard.standards.clear()


def test_structure():
    g1 = Group('1')
    p11, p12 = Patient('11', '1'), Patient('12', '1')
    p11.delete()
    assert '11' not in Patient.patients
    assert '11' not in g1.pats
    g1.delete()
    assert '12' not in Patient.patients
    assert '2' not in Group.groups


if __name__ == '__main__':
    test_structure()
