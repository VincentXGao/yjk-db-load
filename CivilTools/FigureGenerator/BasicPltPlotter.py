from typing import List
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import io
import numpy as np

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.size"] = 14


def GetTicks(n_max=1):
    if n_max == 0:
        n_max = 100
    m = int(np.log10(n_max))
    if m <= 0 and n_max <= 1:
        m -= 1
    p = n_max / (10**m)
    if p <= 2.2:
        result = [i * 1 * 10**m for i in range(3)]
    elif p <= 3.5:
        result = [i * 2 * 10**m for i in range(3)]
    elif p <= 5:
        result = [i * 2.5 * 10**m for i in range(3)]
    elif p <= 6.9:
        result = [i * 3 * 10**m for i in range(4)]
    elif p <= 8:
        result = [i * 2 * 10**m for i in range(5)]
    else:
        result = [i * 2 * 10**m for i in range(6)]
    return result


class BasicPltPlotter:
    def __init__(self, fig_num: int = 1, fig_size=(10, 10)):
        self.fig, _axes = plt.subplots(1, fig_num, figsize=fig_size)
        if fig_num == 1:
            self.axes = [_axes]
        else:
            self.axes = _axes
        self.fig.patch.set_facecolor("none")
        for ax in self.axes:
            ax.patch.set_facecolor("none")
        self.axes: List[Axes]
        self.__remove_border()

    def __remove_border(self):
        for ax in self.axes:
            ax.spines["right"].set_color("none")
            ax.spines["top"].set_color("none")

    def save_to_stream(self):
        # 将图片保存到内存中的 BytesIO 对象
        img_buffer = io.BytesIO()
        self.fig.savefig(img_buffer, format="png", dpi=150)  # 保存为 PNG 格式
        plt.close()  # 关闭图形，释放内存
        # 将指针重置到流的开头，以便后续读取
        img_buffer.seek(0)
        return img_buffer


class SeismicPlotter(BasicPltPlotter):
    def __init__(self, fig_num=2, floor_num: int = 8):
        if fig_num != 1 and fig_num != 2:
            raise ValueError("Only 1 or 2 is accepted for fig_num.")
        if fig_num == 1:
            fig_size = (3, 5)
        else:
            fig_size = (6, 5)
        super().__init__(fig_num, fig_size)
        self.kwargs_x = {
            "label": "X",
            "ls": "-",
            "color": "k",
            "marker": "o",
            "ms": 3,
        }
        self.kwargs_y = {
            "label": "X",
            "ls": "-",
            "color": "r",
            "marker": "o",
            "ms": 3,
        }
        self.floor_num = floor_num
        self.y_label = "层号"
        self._y_values = [i + 1 for i in range(self.floor_num)]
        self._y_major_ticks = self.__create_y_ticks()
        self._y_minor_ticks = [i + 1 for i in range(self.floor_num)]
        self._ax1_x = [i for i in range(self.floor_num)]
        self._ax1_y = [i * 0.5 for i in range(self.floor_num)]
        self._ax2_x = [i for i in range(self.floor_num)]
        self._ax2_y = [i * 0.5 for i in range(self.floor_num)]

    def test_plot(self):
        self.__plot()

    def __plot(self):
        self.axes[0].plot(self._ax1_x, self._y_values, **self.kwargs_x)
        self.axes[0].plot(self._ax1_y, self._y_values, **self.kwargs_y)
        self.axes[1].plot(self._ax2_x, self._y_values, **self.kwargs_x)
        self.axes[1].plot(self._ax2_y, self._y_values, **self.kwargs_y)

    def __create_y_ticks(self):
        floor_num = self.floor_num
        return range(0, int(floor_num) + 1, int(floor_num // 5) + 1)

    def _validate_list_length(self, data_list, name):
        """
        验证列表长度是否与楼层数相等
        :param data_list: 待验证的列表
        :param name: 列表的名称，用于异常信息
        """
        if len(data_list) != self.floor_num:
            raise ValueError(
                f"Length of {name} is not equal to floor number: {self.floor_num}!"
            )
