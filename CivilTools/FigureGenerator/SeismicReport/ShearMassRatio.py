from ..BasicPltPlotter import SeismicPlotter, GetTicks
from typing import List
import numpy as np
import matplotlib.pyplot as plt


class ShearMassRatioPlotter(SeismicPlotter):
    def __init__(self, fig_num=2, floor_num=8):
        super().__init__(fig_num, floor_num)
        self.__limit = None
        self.type = "剪重比"

    def set_data(self, shear_x: List[float], shear_y: List[float], mass: List[float]):
        if len(shear_x) != self.floor_num:
            raise ValueError(
                f"Lenght of shear_x is not equal to floor number: {self.floor_num}!"
            )
        if len(shear_y) != self.floor_num:
            raise ValueError(
                f"Lenght of shear_y is not equal to floor number: {self.floor_num}!"
            )
        if len(mass) != self.floor_num:
            raise ValueError(
                f"Lenght of mass is not equal to floor number: {self.floor_num}!"
            )

        self._ax1_x = np.array(shear_x) / np.array(mass)
        self._ax2_x = np.array(shear_y) / np.array(mass)

    def set_limit(self, limit: float):
        self.__limit = limit

    def plot(self):
        if self.__limit:
            self.__plot_limit()
        kwargs_x = self.kwargs_x.copy()
        kwargs_x["label"] = "X"
        kwargs_y = self.kwargs_x.copy()
        kwargs_y["label"] = "Y"
        self.axes[0].plot(self._ax1_x, self._y_values, **kwargs_x)
        self.axes[1].plot(self._ax2_x, self._y_values, **kwargs_y)
        self.__adjust_lim()
        self.__add_titles()

    def __plot_limit(self):
        limitation = self.__limit
        for ax in self.axes:
            ax.vlines(
                x=limitation,
                ymin=0,
                ymax=self.floor_num,
                color="r",
                linewidth=3,
                ls="--",
                label=f"限值{limitation*100:.1f}%",
            )

    def __adjust_lim(self):
        xmaxs = [self._ax1_x.max(), self._ax2_x.max()]
        for i in range(2):
            self.axes[i].set_xlim(left=0, right=xmaxs[i] * 1.2)
            self.axes[i].set_yticks(self._y_major_ticks)
            self.axes[i].set_yticks(self._y_minor_ticks, minor=True)
            x_ticks = GetTicks(xmaxs[i])
            self.axes[i].set_xticks(x_ticks)
            self.axes[i].set_xticklabels([f"{i*100:.1f}%" for i in x_ticks])

    def __add_titles(self):
        self.axes[0].set_ylabel(self.y_label)
        self.axes[0].set_xlabel(f"X小震下{self.type}")
        self.axes[1].set_xlabel(f"Y小震下{self.type}")
        self.axes[0].legend(framealpha=0, fontsize=12, loc=4)
        self.axes[1].legend(framealpha=0, fontsize=12, loc=4)
