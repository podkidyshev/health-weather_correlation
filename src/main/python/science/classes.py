from science import read_sample, file_base_name
from science.funcs import sequence_max


CATEGORIES_SHORT = {
    "": "без нагрузки",
    "n": "с физической нагрузкой",
    "o": "после отдыха",
    "e": "с эмоциональной нагрузкой"
}
CATEGORIES = {value: key for key, value in CATEGORIES_SHORT.items()}
CATEGORIES_LIST = [(cat, CATEGORIES_SHORT[cat]) for cat in ["", "n", "o", "e"]]

MAIN_CATEGORY = "без нагрузки"
MAIN_CATEGORY_SHORT = ""


class CategoryError(Exception):
    pass


class PatientDuplicateError(Exception):
    pass


class Patient:
    patients = {}

    def __init__(self, name):
        if name in Patient.patients:
            raise PatientDuplicateError('Пациент с именем {} уже загружен'.format(name))
        Patient.patients[name] = self

        self.name = name
        # Удобные ссылки для основной категории (DEFAULT_MAIN_CATEGORY)
        self.data = None
        self.seq_max = None

        self.categories = {cat: None for cat in CATEGORIES_SHORT}
        self.categories_seq_max = {cat: None for cat in CATEGORIES_SHORT}

    def has_category(self, category: str):
        return self.categories[category] is not None

    def _add_category(self, cat: str, data: list):
        self.categories[cat] = data
        self.categories_seq_max[cat] = sequence_max(data)
        if cat == CATEGORIES_SHORT:
            self.data = self.categories[cat]
            self.seq_max = self.categories_seq_max[cat]

    def add_category(self, cat: str, filename: str):
        if cat not in CATEGORIES_SHORT:
            raise CategoryError('Неизвестная категория {}'.format(cat))
        data = read_sample(filename)
        self._add_category(cat, data)


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

    @staticmethod
    def from_file(filename: str, name: str=""):
        if not name:
            name = file_base_name(filename)
        data = read_sample(filename)
        return Standard(name, data)

    @staticmethod
    def cleanup():
        Standard.standards.clear()
