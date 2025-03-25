import math
import abc
from typing import List
import matplotlib.pyplot as plt


class SinglePeriod:
    """单个周期"""

    def __init__(
        self,
        index: int,
        time: float,
        angle: float = 0,
        coeff_x: float = 1,
        coeff_y: float = 0,
        coeff_z: float = 0,
        mass_particpate_x: float = 0,
        mass_particpate_y: float = 0,
        mass_particpate_z: float = 0,
    ):
        self.index = index
        self.time = time
        self.angle = angle
        assert (
            abs(coeff_x + coeff_y + coeff_z - 1) < 0.01
        ), "The sum of three participite coeff should == 1"
        self.coeff_x = coeff_x
        self.coeff_y = coeff_y
        self.coeff_z = coeff_z
        if coeff_x >= coeff_y and coeff_x >= coeff_z:
            self.direction = "X"
        elif coeff_y >= coeff_x and coeff_y >= coeff_z:
            self.direction = "Y"
        else:
            self.direction = "Z"
        self.mass_participate_x = mass_particpate_x
        self.mass_participate_y = mass_particpate_y
        self.mass_participate_z = mass_particpate_z

    @property
    def time_str(self):
        return f"{self.time:.4f}"

    @property
    def movement_coeff(self):
        return (
            f"{self.coeff_x + self.coeff_y:.2f} ({self.coeff_x:.2f}+{self.coeff_y:.2f})"
        )

    @property
    def rotation_coeff(self):
        return f"{self.coeff_z:.2f}"

    def get_mass_participate_x(self, last):
        return f"{self.mass_participate_x*100:.1f} ({(self.mass_participate_x + last)*100:.1f})"

    def get_mass_participate_y(self, last):
        return f"{self.mass_participate_y*100:.1f} ({(self.mass_participate_y + last)*100:.1f})"

    def __str__(self):
        return f"T{self.index}:\t{self.time:.4f}s\t[X:{self.coeff_x*100:.1f}%;\tY:{self.coeff_y*100:.1f}%;\tZ:{self.coeff_z*100:.1f}%]"

    def __repr__(self):
        return str(self)

    def to_json(self):
        return {"index": self.index, "time": self.time}


class Period:
    def __init__(self, periods: List[SinglePeriod], model_type=None):
        if len(periods) < 3:
            raise ValueError("At least three periods is needed.")
        self.periods = periods

    def __str__(self):
        if len(self.periods) <= 10:
            return "\n".join([str(period) for period in self.periods])
        else:
            result = "\n".join([str(period) for period in self.periods[:9]])
            result += "\n....\n"
            result += str(self.periods[-1])
            return result

    def __repr__(self):
        return self.__str__()

    @classmethod
    def mock_data(
        cls, order: str = "xyz", num: int = 40, mass_participate: float = 0.95
    ):
        single_period_list = []
        single_period_list.append(
            SinglePeriod(
                1,
                2.5,
                0,
                order[0] == "x",
                order[0] == "y",
                order[0] == "z",
                0.1,
                0.1,
                0.1,
            )
        )
        single_period_list.append(
            SinglePeriod(
                2,
                2.0,
                0,
                order[1] == "x",
                order[1] == "y",
                order[1] == "z",
                0.2,
                0.2,
                0.2,
            )
        )
        single_period_list.append(
            SinglePeriod(
                3,
                1.5,
                0,
                order[2] == "x",
                order[2] == "y",
                order[2] == "z",
                0.3,
                0.3,
                0.3,
            )
        )

        for i in range(num - 3):
            single_period_list.append(
                SinglePeriod(
                    i + 4,
                    0.5 - 0.01 * i,
                    0,
                    1,
                    0,
                    0,
                    mass_participate,
                    mass_participate,
                    mass_participate,
                )
            )
        return Period(single_period_list)

    def to_json(self):
        return {"periods": [i.to_json() for i in self.periods]}


class ValuePeer:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        if self.x > 500:
            return f"X:{self.x:.1f}\tY:{self.y:.1f}"
        elif self.x > 5:
            return f"X:{self.x:.2f}\tY:{self.y:.2f}"
        else:
            return f"X:{self.x:.3f}\tY:{self.y:.3f}"

    def to_json(self):
        return {"X": self.x, "Y": self.y}


class FloorDrift:
    def __init__(
        self,
        floor_height: float,
        drift_disp_x: float,
        drift_disp_y: float,
        drift_min_disp_x: float,
        drift_min_disp_y: float,
        max_disp_x: float,
        ave_disp_x: float,
        max_disp_y: float,
        ave_disp_y: float,
    ):
        self.floor_height = floor_height
        self.max_disp_x = drift_disp_x
        self.max_disp_y = drift_disp_y
        self.min_disp_x = drift_min_disp_x
        self.min_disp_y = drift_min_disp_y
        self.max_disp_x = max_disp_x
        self.ave_disp_x = ave_disp_x
        self.max_disp_y = max_disp_y
        self.ave_disp_y = ave_disp_y


class FloorSeismicResult:
    def __init__(
        self,
        floor_num: int,
        tower_num: int,
        force: ValuePeer = None,
        shear: ValuePeer = None,
        moment: ValuePeer = None,
        disp: ValuePeer = None,
        stiffness: List[ValuePeer] = [],
        shear_capacity: ValuePeer = None,
        drifts: List[FloorDrift] = [],
    ):
        self.floor_num = floor_num
        self.tower_num = tower_num
        self.force = force
        self.shear = shear
        self.moment = moment
        self.disp = disp
        self.stiffness = stiffness
        self.shear_capacity = shear_capacity
        self.drifts = drifts

    def __str__(self):
        return f"Flr.{self.floor_num}:Fx={self.force.x};Fy={self.force.y}"

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return {
            "floor_num": self.floor_num,
            "tower_num": self.tower_num,
            "shear": self.shear.to_json(),
        }


class SeismicResult:
    def __init__(self, floor_result: List[FloorSeismicResult]):
        self.floor_result = floor_result

    @property
    def seismic_shear_x(self):
        return [i.shear.x for i in self.floor_result]

    @property
    def floor_index(self):
        return [i + 1 for i in range(len(self.floor_result))]

    def plot_shear(self):
        fig, ax = plt.subplots(figsize=(2, 5))
        ax.plot(self.seismic_shear_x, self.floor_index)
        return fig, ax

    def __str__(self):
        result = f"Total floor: {len(self.floor_result)}\n"
        for temp_result in self.floor_result:
            result += str(temp_result)
            result += "\n"
        return result

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return {"floor_result": [i.to_json() for i in self.floor_result]}


if __name__ == "__main__":
    p_list = []
    for i in range(112):
        p_list.append(SinglePeriod(i + 1, i * 0.1 + 0.1, 0, 1 - i * 0.1, i * 0.1, 0))
    P = Period(p_list)
    print(str(P))
