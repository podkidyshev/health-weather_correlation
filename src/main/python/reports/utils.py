from science import plot_image, FACTORS
from science.funcs import test_normal_plot
from science.classes import Standard, Sample

from reports import Printer, str_arr


def report_ntest(report, doc: Printer):
    res_ok = "Образец выглядит гауссовским (не может отклонить гипотезу H0)"
    res_nok = "Образец не выглядит гауссовским (отклонить гипотезу H0)"

    shapiro = report["shapiro"]
    doc.add_heading("Тест нормальности Шапиро-Вилка", 2)
    doc.add_paragraph("Statistics = {:.3f}, p = {:.3f}".format(shapiro["stat"], shapiro["p"]))
    doc.add_paragraph((res_ok if shapiro["res"] else res_nok) + '\n')

    agostino = report["agostino"]
    doc.add_heading("D'Agostino and Pearson's Test", 2)
    doc.add_paragraph("Statistics = {:.3f}, p = {:.3f}".format(agostino["stat"], agostino["p"]))
    doc.add_paragraph((res_ok if agostino["res"] else res_nok) + '\n')

    anderson = report["anderson"]
    doc.add_heading("Тест нормальности Андерсона-Дарлинга", 2)
    doc.add_paragraph("Statistic = {:.3f}".format(anderson["statistic"]))
    for res, cv, sl in zip(anderson["res"], anderson["critical"], anderson["sig_level"]):
        doc.add_paragraph("{:.3f}: {:.3f}, {}\n".format(sl, cv, res_ok if res else res_nok))

    ks = report["ks"]
    doc.add_heading("Тест нормальности Колмогорова-Смирнова", 2)
    num_tests = ks["num_tests"]
    num_rejects = ks["num_rejects"]
    ratio = ks["ratio"]
    alpha = ks["alpha"]
    doc.add_paragraph(
        "Результаты теста Колмогорова-Смирнова: "
        "из {} прогонов доля {}/{} = {:.2f} отклоняет гипотезу H0 на уровне отклонения {}\n".format(
            num_tests, num_rejects, num_tests, ratio, alpha))

    if report['qq']:
        img = plot_image(test_normal_plot, report, io=True)
        doc.add_picture(img)


def report_sample_factor(sample: Sample, factor: int, doc: Printer):
    doc.add_heading("Фактор-образец {}".format(FACTORS[factor].lower()), 2)
    doc.add_paragraph("Количество значений равно = {}".format(len(sample.data[factor])))
    doc.add_paragraph(str_arr(sample.data[factor]))
    doc.add_paragraph("Количество максимумов равно = {}".format(len(sample.seq_max[factor])))
    doc.add_paragraph(str_arr(sample.seq_max[factor]))


def report_sample(sample: Sample, doc: Printer):
    doc.add_heading("Образец {}".format(sample.name), 1)
    for factor in range(4):
        report_sample_factor(sample, factor, doc)


def report_std(std: Standard, doc: Printer):
    doc.add_heading("Эталон {}".format(std.name), 1)
    doc.add_paragraph("Количество значений равно = {}".format(len(std.data)))
    doc.add_paragraph(str_arr(std.data))
    doc.add_paragraph("Количество максимумов равно = {}".format(len(std.seq_max)))
    doc.add_paragraph(str_arr(std.seq_max))
