import os
import matplotlib.pyplot as plt

from io import BytesIO

from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QImage, QPixmap

from docx import Document
from docx.shared import Cm
from openpyxl import load_workbook

FACTORS = [
    "без нагрузки",
    "с физической нагрузкой",
    "с эмоциональной нагрузкой",
    "после отдыха"
]


class XLSXParseError(ValueError):
    pass


def nnone(arr):
    for idx, el in enumerate(arr):
        if el is not None:
            yield idx, el


def is_float(s: str):
    try:
        return float(s)
    except ValueError:
        return False


def file_base_name(filename: str):
    return os.path.splitext(os.path.basename(filename))[0]


def read_sample(filename):
    """Чтение эталонов"""
    with open(filename) as file:
        data = [row.strip() for row in file]

    for idx, el in enumerate(data):
        # noinspection PyTypeChecker
        data[idx] = float(el)
    return data


def read_xlsx_sample(filename):
    wb = load_workbook(filename=filename)
    sheet = wb.get_active_sheet()

    datas = []
    for col in range(1, 4 + 1):
        data, row = [], 1
        val = sheet.cell(row, col).value
        if not val:
            datas.append(None)
            continue

        val = val.strip()
        # Пропустим первую строку, если там не число (заголовок, например)
        if is_float(val) is False:
            row += 1
        while sheet.cell(row, col).value is not None and sheet.cell(row, col).value.strip():
            try:
                data.append(float(sheet.cell(row, col).value))
            except ValueError:
                err = 'Ошибка при парсе файла {}, страницы {}, ячейки {}{}'.format(filename,
                                                                                   sheet.title,
                                                                                   'ABCD'[col],
                                                                                   row)
                print(err)
                raise XLSXParseError(err)
            row += 1
        datas.append(data)
    return datas


def patient_suffix(filename: str, suffix):
    return filename[:filename.rfind('.')] + suffix + filename[filename.rfind('.'):]


def plot_image(plot_func, *args):
    figure = plt.figure()
    plot_func(*args, figure)
    return plot_to_image(figure)


def plot_to_image(figure):
    """Вовзращет PIL.Image последнего вызова plt.figure()"""
    return Image.open(plot_to_stream(figure))


def plot_to_qimage(figure):
    return QImage(ImageQt(plot_to_image(figure)))


def plot_to_pixmap(figure):
    return QPixmap.fromImage(plot_to_qimage(figure))


def plot_to_stream(figure):
    buffer = BytesIO()
    figure.savefig(buffer)
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


if __name__ == '__main__':
    print('\n'.join(map(str, read_xlsx_sample("samples/1_1.xlsx"))))
