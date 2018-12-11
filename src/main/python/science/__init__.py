import os
from io import BytesIO

from PIL import Image
from matplotlib import pyplot as plt

from docx import Document
from docx.shared import Cm


CATS_SHORT = {
    "": "без нагрузки",
    "n": "с физической нагрузкой",
    "o": "после отдыха",
    "e": "с эмоциональной нагрузкой"
}
CATS_FULL = {value: key for key, value in CATS_SHORT.items()}
CATS = [(cat, CATS_SHORT[cat]) for cat in ["", "n", "o", "e"]]


class CategoryError(Exception):
    pass


def cat_index(cat):
    if isinstance(cat, int):
        return cat
    if not isinstance(cat, str):
        raise CategoryError('Неизвестный тип нахождения категории: {}'.format(type(cat)))
    for idx, (short, long) in enumerate(CATS):
        if short == cat or long == cat:
            return idx
    raise CategoryError('Неизвестная категоря: ""'.format(cat))


def nnone(arr):
    for idx, el in enumerate(arr):
        if el is not None:
            yield idx, el


def file_base_name(filename: str):
    return os.path.splitext(os.path.basename(filename))[0]


def read_sample(filename):
    """Чтение образцов и эталонов"""
    with open(filename) as file:
        data = [row.strip() for row in file]

    for idx, el in enumerate(data):
        # noinspection PyTypeChecker
        data[idx] = float(el)
    return data


def patient_suffix(filename: str, suffix):
    return filename[:filename.rfind('.')] + suffix + filename[filename.rfind('.'):]


def plot_to_image(figure):
    """Вовзращет PIL.Image последнего вызова plt.figure()"""
    # wh = plt.get_current_fig_manager().canvas.get_width_height()
    buf = plot_to_stream(figure)
    return Image.open(buf)


def plot_to_stream(figure):
    # img = plot_to_image()
    buffer = BytesIO()
    figure.savefig(buffer)
    # img.save(buffer, 'png')
    buffer.seek(0)
    return buffer


def create_docx():
    doc = Document()
    doc.core_properties.author = "Молчанов В.А."
    return doc


def save_docx(doc, obj):
    for section in doc.sections:
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(1.5)
    doc.save(obj)
