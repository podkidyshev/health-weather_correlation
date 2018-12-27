from science import plot_image
from science.funcs import *
from science.classes import Sample, Standard
from science.test_normal import *


class FactorSampleStandard:
    def __init__(self, sample: Sample, factor: int, std: Standard):
        self.sample = sample
        self.factor = factor
        self.std = std

        self.distance = sequence_distance(sample.seq_max[factor], std.seq_max, insert_zero=True)
        self.distance1 = sequence_distance(sample.seq_max[factor], std.seq_max, insert_zero=False)

        self.stat_mean, self.stat_std, self.stat_interval = stat_analysis(self.distance)
        self.ntest = test_normal(self.distance, qq=False)

        self.va = plot_image(visual_analysis, self.distance)


class SampleStandard:
    def __init__(self, sample: Sample, std: Standard):
        self.sample = sample
        self.std = std

        self.distance = [sequence_distance(sample.seq_max[factor], std.seq_max, insert_zero=True)
                         for factor in range(4)]
        self.distance1 = [sequence_distance(sample.seq_max[factor], std.seq_max, insert_zero=False)
                          for factor in range(4)]

        self.graph_kde = plot_image(graph_kde, self.distance)
        self.va = [plot_image(visual_analysis, xr) for xr in self.distance]
        self.ntest = [test_normal(xr, qq=False) for xr in self.distance]

        stat = [stat_analysis(xr) for xr in self.distance]
        self.stat_mean = [stat[i][0] for i in range(4)]
        self.stat_std = [stat[i][1] for i in range(4)]
        self.stat_interval = [stat[i][2] for i in range(4)]

        # резерв


class MulSamplesStandard:
    def __init__(self, samples: list, std: Standard):
        self.samples = samples[:]
        self.std = std

        self.group_sample = [sum_list([sample.data[factor] for sample in samples]) for factor in range(4)]
        self.group_sample_seq_max = [sequence_max(self.group_sample[factor]) for factor in range(4)]
        self.group_sample_distance = [sequence_distance(self.group_sample_seq_max[factor],
                                                        std.seq_max,
                                                        insert_zero=True)
                                      for factor in range(4)]

        self.distance = [[sequence_distance(sample.seq_max[factor], std, insert_zero=True)
                          for factor in range(4)] for sample in samples]

        self.max_list = []
        for factor in range(4):
            max_list_factor = []
            for sample_num in range(len(samples)):
                max_list_factor.append(np.mean(self.distance[sample_num][factor]))
            self.max_list.append(max_list_factor)

        self.max_graph_kde = plot_image(graph_kde, self.max_list)
        self.max_va = [plot_image(visual_analysis, xr) for xr in self.max_list]
        self.max_va2 = [plot_image(visual_analysis2, self.group_sample_seq_max[factor], self.max_list[factor])
                        for factor in range(4)]

        self.group_sample_ntest = [test_normal(self.group_sample_distance[factor], qq=False) for factor in range(4)]
        self.max_list_ntest = [test_normal(self.max_list[factor], qq=False) for factor in range(4)]

        stat = [stat_analysis(self.max_list[factor]) for factor in range(4)]
        self.stat_mean = [stat[i][0] for i in range(4)]
        self.stat_std = [stat[i][1] for i in range(4)]
        self.stat_interval = [stat[i][2] for i in range(4)]


class FactorSampleMulStandards:
    def __init__(self, sample: Sample, factor: int, stds: list):
        self.sample = sample
        self.factor = factor
        self.stds = stds[:]

        self.distance = [sequence_distance(self.sample.seq_max[factor], std.seq_max, insert_zero=True)
                         for std in stds]
        self.distance1 = [sequence_distance(self.sample.seq_max[factor], std.seq_max, insert_zero=False)
                          for std in stds]

        stat = [stat_analysis(self.distance[std_num]) for std_num in range(len(stds))]
        self.stat_mean = [stat[std_num][0] for std_num in range(len(stds))]
        self.stat_std = [stat[std_num][1] for std_num in range(len(stds))]
        self.stat_interval = [stat[std_num][2] for std_num in range(len(stds))]


class SampleMulStandards:
    def __init__(self, sample: Sample, stds: list):
        self.sample = sample
        self.stds = stds[:]

        self.distance = [[sequence_distance(sample.seq_max[factor], std.seq_max, insert_zero=True)
                          for factor in range(4)]
                         for std in stds]
        self.distance1 = [[sequence_distance(sample.seq_max[factor], std.seq_max, insert_zero=False)
                           for factor in range(4)]
                          for std in stds]

        stat = [[stat_analysis(self.distance[std_num][factor]) for factor in range(4)]
                for std_num in range(len(stds))]
        self.stat_mean = [[stat[std_num][factor][0] for factor in range(4)] for std_num in range(len(stds))]
        self.stat_std = [[stat[std_num][factor][1] for factor in range(4)] for std_num in range(len(stds))]
        self.stat_interval = [[stat[std_num][factor][2] for factor in range(4)] for std_num in range(len(stds))]


class MulSamplesMulStandards:
    def __init__(self, samples: list, stds: list):
        self.samples = samples[:]
        self.stds = stds[:]

        self.distance = [[[sequence_distance(sample.seq_max[factor], std.seq_max, insert_zero=True)
                           for factor in range(4)] for sample in samples] for std in stds]
        self.distance1 = [[[sequence_distance(sample.seq_max[factor], std.seq_max, insert_zero=False)
                            for factor in range(4)] for sample in samples] for std in stds]

        stat = [[[stat_analysis(self.distance[std_num][sample_num][factor]) for factor in range(4)]
                 for sample_num in range(len(samples))] for std_num in range(len(stds))]
        self.stat_mean = [[[stat[std_num][sample_num][factor][0] for factor in range(4)]
                           for sample_num in range(len(samples))] for std_num in range(len(stds))]
        self.stat_std = [[[stat[std_num][sample_num][factor][1] for factor in range(4)]
                          for sample_num in range(len(samples))] for std_num in range(len(stds))]
        self.stat_interval = [[[stat[std_num][sample_num][factor][2] for factor in range(4)]
                               for sample_num in range(len(samples))] for std_num in range(len(stds))]
