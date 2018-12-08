import os

from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.figure import Figure


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


def plot_to_image():
    """Вовзращет PIL.Image последнего вызова plt.figure()"""
    canvas = plt.get_current_fig_manager().canvas
    canvas.draw()
    return Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())
