from typing import List
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import io


class BasicPltPlotter:
    def __init__(self, fig_num: int = 1, fig_size=(10, 10)):
        self.fig, _axes = plt.subplots(1, fig_num, figsize=fig_size)
        if fig_num == 1:
            self.axes = [_axes]
        else:
            self.axes = _axes
        self.axes: List[Axes]
        self.__remove_border()

    def __remove_border(self):
        for ax in self.axes:
            ax.spines["right"].set_color("none")
            ax.spines["top"].set_color("none")

    def save_to_stream(self):
        # 将图片保存到内存中的 BytesIO 对象
        img_buffer = io.BytesIO()
        self.fig.savefig(img_buffer, format="png", dpi=300)  # 保存为 PNG 格式
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
        self.floor_num = floor_num
        self.__y_values = [i + 1 for i in range(self.floor_num)]
        self.__ax1_x = [i for i in range(self.floor_num)]
        self.__ax1_y = [i * 0.5 for i in range(self.floor_num)]
        self.__ax2_x = [i for i in range(self.floor_num)]
        self.__ax2_y = [i * 0.5 for i in range(self.floor_num)]

    def test_plot(self):
        self.__plot()

    def __plot(self):
        kwargs_x = {"label": "X", "ls": "-", "color": "k", "marker": "o", "ms": 3}
        kwargs_y = {"label": "X", "ls": "-", "color": "r", "marker": "o", "ms": 3}

        self.axes[0].plot(self.__ax1_x, self.__y_values, **kwargs_x)
        self.axes[0].plot(self.__ax1_y, self.__y_values, **kwargs_y)
        self.axes[1].plot(self.__ax2_x, self.__y_values, **kwargs_x)
        self.axes[1].plot(self.__ax2_y, self.__y_values, **kwargs_y)
