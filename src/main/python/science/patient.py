from science import read_sample, file_base_name, sequence_max


DEFAULT_CATEGORIES_SHORT = {
    "": "без нагрузки",
    "n": "с физической нагрузкой",
    "o": "после отдыха",
    "e": "с эмоциональной нагрузкой"
}
DEFAULT_CATEGORIES = {value: key for key, value in DEFAULT_CATEGORIES_SHORT.items()}

DEFAULT_MAIN_CATEGORY = "без нагрузки"
DEFAULT_MAIN_CATEGORY_SHORT = ""


class CategoryError(Exception):
    pass


class PatientDuplicateError(Exception):
    pass


class Patient:
    all_pats = {}

    def __init__(self, name):
        if name in Patient.all_pats:
            raise PatientDuplicateError('Пациент с именем {} уже загружен'.format(name))
        Patient.all_pats[name] = self

        self.name = name
        # Удобные ссылки для основной категории (DEFAULT_MAIN_CATEGORY)
        self.data = None
        self.seq_max = None

        self.categories = {cat: None for cat in DEFAULT_CATEGORIES_SHORT}
        self.categories_seq_max = {cat: None for cat in DEFAULT_CATEGORIES_SHORT}

    def has_category(self, category: str):
        return self.categories[category] is not None

    def _add_category(self, cat: str, data: list):
        self.categories[cat] = data
        self.categories_seq_max[cat] = sequence_max(data)
        if cat == DEFAULT_CATEGORIES_SHORT:
            self.data = self.categories[cat]
            self.seq_max = self.categories_seq_max[cat]

    def add_category(self, cat: str, filename: str):
        if cat not in DEFAULT_CATEGORIES_SHORT:
            raise CategoryError('Неизвестная категория {}'.format(cat))
        data = read_sample(filename)
        self._add_category(cat, data)


class ReferenceDuplicateError(Exception):
    pass


class Reference:
    all_refs = {}

    def __init__(self, name, data):
        if name in Reference.all_refs:
            raise ReferenceDuplicateError('Эталон {} уже загружен'.format(name))
        Reference.all_refs[name] = self

        self.name = name
        self.data = data
        self.seq_max = sequence_max(self.data)

    @staticmethod
    def from_file(filename: str, name: str=""):
        if not name:
            name = file_base_name(filename)
        data = read_sample(filename)
        return Reference(name, data)

    @staticmethod
    def cleanup():
        Reference.all_refs.clear()
