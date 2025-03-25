from ..BasicPltPlotter import SeismicPlotter, GetTicks
from typing import List
import numpy as np
import matplotlib.pyplot as plt


class ShearMomentPlotter(SeismicPlotter):
    def __init__(self, floor_num=8, type="Shear", fig_num=2):
        super().__init__(fig_num, floor_num)
        self.__limit = None
        if type.lower() == "shear":
            self.type = "楼层剪力 kN"
        elif type.lower() == "moment":
            self.type = "倾覆力矩 MN·m"
        else:
            raise ValueError("Only shear or moment is supported for type.")

    def set_data(
        self,
        wind_x: List[float],
        wind_y: List[float],
        seismic_x: List[float],
        seismic_y: List[float],
    ):
        # 验证数据长度
        data_dict = {
            "wind_x": wind_x,
            "wind_y": wind_y,
            "seismic_x": seismic_x,
            "seismic_y": seismic_y,
        }
        for name, data_list in data_dict.items():
            self._validate_list_length(data_list, name)

        self._ax1_x = np.array(wind_x)
        self._ax1_y = np.array(wind_y)
        self._ax2_x = np.array(seismic_x)
        self._ax2_y = np.array(seismic_y)

    def plot(self):
        if self.__limit:
            self.__plot_limit()
        kwargs_x = self.kwargs_x.copy()
        kwargs_x["label"] = "X风"
        kwargs_y = self.kwargs_y.copy()
        kwargs_y["label"] = "Y风"
        self.axes[0].plot(self._ax1_x, self._y_values, **kwargs_x)
        self.axes[0].plot(self._ax1_y, self._y_values, **kwargs_y)
        kwargs_x["label"] = "X小震"
        kwargs_y["label"] = "Y小震"
        self.axes[1].plot(self._ax2_x, self._y_values, **kwargs_x)
        self.axes[1].plot(self._ax2_y, self._y_values, **kwargs_y)
        self.__adjust_lim()
        self.__add_titles()

    def __adjust_lim(self):
        xmaxs = [self._ax1_x.max(), self._ax2_x.max()]
        for i in range(2):
            self.axes[i].set_xlim(left=0, right=xmaxs[i] * 1.2)
            self.axes[i].set_yticks(self._y_major_ticks)
            self.axes[i].set_yticks(self._y_minor_ticks, minor=True)
            x_ticks = GetTicks(xmaxs[i])
            self.axes[i].set_xticks(x_ticks)
            # self.axes[i].set_xticklabels([f"{i*100:.1f}%" for i in x_ticks])

    def __add_titles(self):
        self.axes[0].set_ylabel(self.y_label)
        self.axes[0].set_xlabel(f"风下{self.type}")
        self.axes[1].set_xlabel(f"小震下{self.type}")
        self.axes[0].legend(framealpha=0, fontsize=12, loc=1)
        self.axes[1].legend(framealpha=0, fontsize=12, loc=1)
