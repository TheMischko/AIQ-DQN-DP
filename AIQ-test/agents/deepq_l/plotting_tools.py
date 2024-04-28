import textwrap
from enum import Enum
from typing import Type

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter


def normalized(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2 == 0] = 1
    divider = np.expand_dims(l2, axis)
    return a / divider


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class PlottingTools(object):
    NUM_AVERAGE_OVER_INPUTS = 5

    COLORS = ['red', 'blue', 'green', 'orange', 'purple', 'yellow', 'brown', 'pink', 'gray', 'black']

    def __init__(self):
        self.average_arrs = list()

    def on_exit(self):
        if len(self.average_arrs) > 0:
            np_average_arrs = np.array(self.average_arrs)
            avg_of_arrays = np.average(np_average_arrs, 0)
            self.plot_array(avg_of_arrays, "Average loss figure")
            self.average_arrs.clear()

    def add_values_to_average_arr(self, values_arr):
        if len(values_arr) > 0:
            self.average_arrs.append(values_arr)

    def plot_array(self, y, x=None, title="Figure", type="-"):
        x_points = np.array([i for i in range(len(y))]) if x is None else np.array(x)
        y_points = np.array(y)

        plt.title(title)
        plt.plot(x_points, y_points, type)

        plt.show()

    def plot_multiple_array(self, arrays, title="Figure", type="-"):
        x_points = np.array([i for i in range(len(arrays[0]))])
        if len(x_points) < 10:
            return
        fig, axes = plt.subplots(nrows=len(arrays), ncols=1, figsize=(12, 8))

        for i, arr in enumerate(arrays):
            smoothen_vals = savgol_filter(np.array(arr), window_length=7, polyorder=2)
            axes[i].plot(x_points, smoothen_vals, color=self.COLORS[i], linestyle=type)

        # plt.tight_layout()
        plt.show()


class PlotType(Enum):
    Line = 0
    Dots = 1
class Subplot:
    def __init__(self):
        self.title = ""
        self.data = []
        self.type = PlotType.Line


class SubplotBuilder:
    def __init__(self):
        self.subplot = Subplot()

    def called(self, title):
        self.subplot.title = title
        return self

    def has_data(self, data):
        self.subplot.data = data
        return self

    def typeof(self, plot_type: PlotType):
        self.subplot.type = plot_type
        return self

    def build(self):
        return self.subplot


class PlotBuilder:
    def __init__(self, title, filename = None):
        self.title = title
        self.subplots = []
        self.filename = filename

    def add_sub_plot(self, subplot: Type[Subplot]):
        self.subplots.append(subplot)

    def build(self):
        num_subplots = len(self.subplots)
        num_cols = 2
        num_rows = (num_subplots + num_cols + 1) // num_cols

        fig, axes = plt.subplots(num_rows, num_cols, figsize=(10, num_rows * 5))
        wrapped_title = textwrap.fill(self.title, width=40)
        fig.suptitle(wrapped_title, fontsize=16)

        for i, subplot in enumerate(self.subplots):
            row = i // num_cols
            col = i % num_cols
            ax = axes[row, col]
            self.set_subplot(ax, subplot)

        for i in range(len(self.subplots), len(axes.flat)):
            axes.flatten()[i].axis('off')

        plt.tight_layout(rect=[0, 0.003, 1, 0.95])

        if self.filename:
            plt.savefig(self.filename)
            plt.close()
        else:
            plt.show()

    def set_subplot(self, axis, subplot):
        axis.set_title(subplot.title)
        if subplot.type == PlotType.Dots:
            axis.plot(subplot.data, marker='o', linestyle='', markersize=1)
            return
        axis.plot(subplot.data)
