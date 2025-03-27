from .BasicPNGPlotter import BasicPNGPlotter
from CivilTools.YDBLoader.BuildingDefine.StairPart import StairPart
import math
from typing import List


class StairCalculationSheetPNGPlotter:
    def __init__(self, stair_part: StairPart):
        self.plotter = BasicPNGPlotter(5000, 3500)
        self.pen_width = 5
        self.bold_pen_width = 15
        self.current_stair = stair_part
        self.start_x = 800
        self.end_x = 4200
        self.start_y = 2200
        self.end_y = 750 if self.current_stair.stair_type == "CT" else 500
        self.extend = 500
        """绘图时左右平台的宽度"""
        self.__plot_basic_stair()

    @property
    def position_AT2(self):
        return (self.start_x, self.start_y, self.end_x, self.end_y)

    @property
    def position_BT1(self):
        return (self.start_x, self.start_y, self.start_x + self.extend, self.start_y)

    @property
    def position_BT2(self):
        return (self.start_x + self.extend, self.start_y, self.end_x, self.end_y)

    @property
    def position_CT2(self):
        return (self.start_x, self.start_y, self.end_x - self.extend, self.end_y)

    @property
    def position_CT3(self):
        return (self.end_x - self.extend, self.end_y, self.end_x, self.end_y)

    @property
    def position_DT1(self):
        return self.position_BT1

    @property
    def position_DT2(self):
        return (
            self.start_x + self.extend,
            self.start_y,
            self.end_x - self.extend,
            self.end_y,
        )

    @property
    def position_DT3(self):
        return self.position_CT3

    def plot_moment(self, moments: List[float]):
        moment_max = max([abs(i) for i in moments])
        # 用来确定弯矩最大值处的高度
        moment_height = [m / moment_max * 400 for m in moments]
        moment_height_1 = [0, moment_height[1] * 0.25, moment_height[1]]
        moment_height_2 = [moment_height[1], moment_height[2], moment_height[3]]
        moment_height_3 = [moment_height[3], moment_height[3] * 0.25, 0]
        moment_1 = [0, moments[1] * 0.25, moments[1]]
        moment_2 = [moments[1], moments[2], moments[3]]
        moment_3 = [moments[3], moments[3] * 0.25, 0]

        if self.current_stair.stair_type == "AT":
            self.__draw_moment_curve(
                *self.position_AT2, moment_height_2, moment_2, True
            )
        elif self.current_stair.stair_type == "BT":
            self.__draw_moment_curve(
                *self.position_BT1, moment_height_1, moment_1, False
            )
            self.__draw_moment_curve(
                *self.position_BT2, moment_height_2, moment_2, True
            )
        elif self.current_stair.stair_type == "CT":
            self.__draw_moment_curve(
                *self.position_CT2, moment_height_2, moment_2, True
            )
            self.__draw_moment_curve(
                *self.position_CT3, moment_height_3, moment_3, False
            )
        elif self.current_stair.stair_type == "DT":
            self.__draw_moment_curve(
                *self.position_DT1, moment_height_1, moment_1, False
            )
            self.__draw_moment_curve(
                *self.position_DT2, moment_height_2, moment_2, True
            )
            self.__draw_moment_curve(
                *self.position_DT3, moment_height_3, moment_3, False
            )
        self.__draw_label_and_title("弯矩线", "弯矩图(kN·m)")

    def plot_shear(self, shears: List[float]):
        shear_max = max([abs(i) for i in shears])
        # 用来确定弯矩最大值处的高度
        shear_height = [s / shear_max * 400 for s in shears]
        shear_height_1 = [shear_height[0], shear_height[1]]
        shear_height_2 = [shear_height[2], shear_height[3]]
        shear_height_3 = [shear_height[4], shear_height[5]]
        shear_1 = [shears[0], shears[1]]
        shear_2 = [shears[2], shears[3]]
        shear_3 = [shears[4], shears[5]]

        # todo: 具体绘图
        if self.current_stair.stair_type == "AT":
            self.__draw_shear_curve(*self.position_AT2, shear_height_2, shear_2, True)
        elif self.current_stair.stair_type == "BT":
            self.__draw_shear_curve(*self.position_BT1, shear_height_1, shear_1)
            self.__draw_shear_curve(*self.position_BT2, shear_height_2, shear_2, True)
        elif self.current_stair.stair_type == "CT":
            self.__draw_shear_curve(*self.position_CT2, shear_height_2, shear_2, True)
            self.__draw_shear_curve(*self.position_CT3, shear_height_3, shear_3)
        elif self.current_stair.stair_type == "DT":
            self.__draw_shear_curve(*self.position_DT1, shear_height_1, shear_1)
            self.__draw_shear_curve(*self.position_DT2, shear_height_2, shear_2, True)
            self.__draw_shear_curve(*self.position_DT3, shear_height_3, shear_3)
        self.__draw_label_and_title("剪力线", "剪力图(kN)")

    def plot_displacement(self, disp: float):
        start_x = self.start_x
        end_x = self.end_x
        start_y = self.start_y
        end_y = self.end_y
        # todo: 具体绘图
        if self.current_stair.stair_type == "AT":
            self.__draw_disp_curve(start_x, start_y, end_x, end_y, disp)
        elif self.current_stair.stair_type == "BT":
            self.plotter.draw_line(
                start_x, start_y, start_x + self.extend, start_y + 200
            )
            self.__draw_disp_curve(
                start_x + self.extend, start_y + 200, end_x, end_y, disp
            )
        elif self.current_stair.stair_type == "CT":
            self.__draw_disp_curve(
                start_x, start_y, end_x - self.extend, end_y + 200, disp
            )
            self.plotter.draw_line(end_x - self.extend, end_y + 200, end_x, end_y)
        elif self.current_stair.stair_type == "DT":
            self.plotter.draw_line(
                start_x, start_y, start_x + self.extend, start_y + 200
            )
            self.__draw_disp_curve(
                start_x + self.extend,
                start_y + 200,
                end_x - self.extend,
                end_y + 200,
                disp,
            )
            self.plotter.draw_line(end_x - self.extend, end_y + 200, end_x, end_y)
        self.__draw_label_and_title("塑性挠度线", "塑性挠度图(mm)")

    def to_stream(self):
        return self.plotter.to_stream()

    def save(self, path):
        self.plotter.save(path)

    def __plot_basic_stair(self):
        start_x = self.start_x
        end_x = self.end_x
        start_y = self.start_y
        end_y = self.end_y
        if self.current_stair.stair_type == "AT":
            self.plotter.draw_line(start_x, start_y, end_x, end_y)
            self.__draw_dimension(
                self.current_stair.total_horizental_length,
                start_x,
                start_y + 500,
                end_x,
                start_y + 500,
                300,
                500,
            )
        elif self.current_stair.stair_type == "BT":
            self.plotter.draw_line(start_x, start_y, start_x + 500, start_y)
            self.plotter.draw_line(start_x + 500, start_y, end_x, end_y)

            self.__draw_dimension(
                self.current_stair.left_extend_length,
                start_x,
                start_y + 500,
                start_x + 500,
                start_y + 500,
                300,
                300,
            )
            self.__draw_dimension(
                self.current_stair.stair_length_list[1],
                start_x + 500,
                start_y + 500,
                end_x,
                start_y + 500,
                300,
                500,
            )

        elif self.current_stair.stair_type == "CT":
            self.plotter.draw_line(start_x, start_y, end_x - 500, end_y)
            self.plotter.draw_line(end_x - 500, end_y, end_x, end_y)
            self.__draw_dimension(
                self.current_stair.stair_length_list[1],
                start_x,
                start_y + 500,
                end_x - 500,
                start_y + 500,
                300,
                450,
            )
            self.__draw_dimension(
                self.current_stair.right_extend_length,
                end_x - 500,
                start_y + 500,
                end_x,
                start_y + 500,
                450,
                500,
            )

        elif self.current_stair.stair_type == "DT":
            self.plotter.draw_line(start_x, start_y, start_x + 500, start_y)
            self.plotter.draw_line(start_x + 500, start_y, end_x - 500, end_y)
            self.plotter.draw_line(end_x - 500, end_y, end_x, end_y)
            self.__draw_dimension(
                self.current_stair.stair_length_list[0],
                start_x,
                start_y + 500,
                start_x + 500,
                start_y + 500,
                300,
                350,
            )
            self.__draw_dimension(
                self.current_stair.stair_length_list[1],
                start_x + 500,
                start_y + 500,
                end_x - 500,
                start_y + 500,
                350,
                450,
            )
            self.__draw_dimension(
                self.current_stair.stair_length_list[2],
                end_x - 500,
                start_y + 500,
                end_x,
                start_y + 500,
                450,
                500,
            )
        d = 50
        temp_x1 = start_x - d / 2 + 10
        temp_y1 = start_y
        self.__draw_boundary(temp_x1, temp_y1, 50)
        temp_x1 = end_x - d / 2 + 10
        temp_y1 = end_y
        self.__draw_boundary(temp_x1, temp_y1, 50)
        self.__draw_dimension(
            self.current_stair.total_height,
            end_x + 400,
            start_y,
            end_x + 400,
            end_y,
            300,
            300,
        )

    def __draw_dimension(self, distance, x1, y1, x2, y2, extend_len1, extend_len2):

        degree = math.atan2((y1 - y2), (x2 - x1))
        sin_deg = math.sin(degree)
        cos_deg = math.cos(degree)
        sin_deg_45 = math.sin(degree + math.pi / 4)
        cos_deg_45 = math.cos(degree + math.pi / 4)
        self.plotter.draw_line(
            x1 - (extend_len1 - 50) * sin_deg,
            y1 - (extend_len1 - 50) * cos_deg,
            x1 + 50 * sin_deg,
            y1 + 50 * cos_deg,
        )
        self.plotter.draw_line(
            x2 - (extend_len2 - 50) * sin_deg,
            y2 - (extend_len2 - 50) * cos_deg,
            x2 + 50 * sin_deg,
            y2 + 50 * cos_deg,
        )
        self.plotter.draw_line(
            x1 - 50 * cos_deg,
            y1 + 50 * sin_deg,
            x2 + 50 * cos_deg,
            y2 - 50 * sin_deg,
        )
        self.plotter.draw_line(
            x1 - 40 * sin_deg_45,
            y1 - 40 * cos_deg_45,
            x1 + 40 * sin_deg_45,
            y1 + 40 * cos_deg_45,
            width=self.bold_pen_width,
        )
        self.plotter.draw_line(
            x2 - 40 * sin_deg_45,
            y2 - 40 * cos_deg_45,
            x2 + 40 * sin_deg_45,
            y2 + 40 * cos_deg_45,
            width=self.bold_pen_width,
        )
        self.plotter.draw_text(
            int((x1 + x2) / 2),
            int((y1 + y2) / 2),
            f"{distance:.0f}",
            100,
            degree,
            y_offset=-150,
        )

    def __draw_boundary(self, x, y, dimeter):
        self.plotter.draw_circle(x, y, dimeter)
        self.plotter.draw_circle(x - 80, y + 138, dimeter)
        self.plotter.draw_circle(x + 80, y + 138, dimeter)
        self.plotter.draw_line(x + 37.5, y + 46.65, x + 92.5, y + 141.91)
        self.plotter.draw_line(x + 12.5, y + 46.65, x - 42.5, y + 141.91)
        self.plotter.draw_line(x - 154.56, y + 188.56, x + 205.44, y + 188.56)
        temp_y = y + 231.86
        for i in range(11):
            temp_x = x - 149.56 + 30 * i
            self.plotter.draw_line(temp_x, temp_y, temp_x + 25, temp_y - 43.3)

    def __draw_moment_curve(
        self,
        x1,
        y1,
        x2,
        y2,
        line_length_list: List[float],
        moment_list: List[float],
        draw_middle: bool,
    ):
        degree = math.atan2((y1 - y2), (x2 - x1))
        sin_deg = math.sin(degree)
        cos_deg = math.cos(degree)
        temp_x1 = x1 + line_length_list[0] * sin_deg
        temp_y1 = y1 + line_length_list[0] * cos_deg
        temp_x2 = (x1 + x2) / 2 + line_length_list[1] * sin_deg
        temp_y2 = (y1 + y2) / 2 + line_length_list[1] * cos_deg
        temp_x3 = x2 + line_length_list[2] * sin_deg
        temp_y3 = y2 + line_length_list[2] * cos_deg

        self.plotter.draw_line(x1, y1, temp_x1, temp_y1)
        self.plotter.draw_line(x2, y2, temp_x3, temp_y3)
        c_x1, c_y1, c_r = self.__calculate_circle_center_by_three_points(
            temp_x1, temp_y1, temp_x2, temp_y2, temp_x3, temp_y3
        )
        degree = math.atan2((temp_y3 - c_y1), (temp_x3 - c_x1))
        start_degree = 180 / math.pi * degree
        degree = math.atan2((temp_y1 - c_y1), (temp_x1 - c_x1))
        end_degree = 180 / math.pi * degree
        if start_degree > 0 and end_degree < 0:
            end_degree = end_degree + 180
        if start_degree > 0 and end_degree < start_degree:
            start_degree = start_degree - 180
            end_degree = end_degree - 180
        if start_degree < 0 and end_degree > start_degree:
            start_degree = start_degree + 180
            end_degree = end_degree + 180
        self.plotter.draw_arc(
            c_x1 - c_r,
            c_y1 - c_r,
            c_r * 2,
            c_r * 2,
            start_degree,
            end_degree,
        )
        degree = math.atan2((y1 - y2), (x2 - x1))
        if draw_middle:
            str_x = int(temp_x2)
            str_y = int(temp_y2)
            self.plotter.draw_text(
                str_x,
                str_y,
                f"{moment_list[1]:.1f}",
                100,
                degree,
                0,
                180 if moment_list[1] > 0 else -180,
            )

        str_x = int(temp_x1)
        str_y = int(temp_y1)
        self.plotter.draw_text(
            str_x,
            str_y,
            f"{moment_list[0]:.1f}",
            100,
            degree,
            800 if (self.current_stair.left_extend_length > 0 and draw_middle) else 0,
            180 if moment_list[0] > 0 else -180,
        )

        str_x = int(temp_x3)
        str_y = int(temp_y3)
        self.plotter.draw_text(
            str_x,
            str_y,
            f"{moment_list[2]:.1f}",
            100,
            degree,
            -800 if (self.current_stair.right_extend_length > 0 and draw_middle) else 0,
            180 if moment_list[2] > 0 else -180,
        )

    def __draw_shear_curve(
        self,
        x1,
        y1,
        x2,
        y2,
        line_length_list: List[float],
        shear_list: List[float],
        is_middle: bool = False,
    ):

        degree = math.atan2((y1 - y2), (x2 - x1))
        sin_deg = math.sin(degree)
        cos_deg = math.cos(degree)
        temp_x1 = x1 + line_length_list[0] * sin_deg
        temp_y1 = y1 + line_length_list[0] * cos_deg
        temp_x2 = x2 + line_length_list[1] * sin_deg
        temp_y2 = y2 + line_length_list[1] * cos_deg
        self.plotter.draw_line(x1, y1, temp_x1, temp_y1)
        self.plotter.draw_line(x2, y2, temp_x2, temp_y2)
        self.plotter.draw_line(temp_x1, temp_y1, temp_x2, temp_y2)
        str_x = int(temp_x1)
        str_y = int(temp_y1)
        self.plotter.draw_text(
            str_x,
            str_y,
            f"{shear_list[0]:.1f}",
            100,
            degree,
            800 if (self.current_stair.left_extend_length > 0 and is_middle) else 0,
            180 if shear_list[0] > 0 else -180,
        )

        str_x = int(temp_x2)
        str_y = int(temp_y2)
        self.plotter.draw_text(
            str_x,
            str_y,
            f"{shear_list[1]:.1f}",
            100,
            degree,
            -800 if (self.current_stair.right_extend_length > 0 and is_middle) else 0,
            180 if shear_list[1] > 0 else -180,
        )

    def __draw_disp_curve(self, x1, y1, x2, y2, disp):
        disp_offset = 400
        degree = math.atan2((y1 - y2), (x2 - x1))
        sin_deg = math.sin(degree)
        cos_deg = math.cos(degree)
        temp_x1 = x1
        temp_y1 = y1
        temp_x2 = (x1 + x2) / 2 + disp_offset * sin_deg
        temp_y2 = (y1 + y2) / 2 + disp_offset * cos_deg
        temp_x3 = x2
        temp_y3 = y2
        c_x1, c_y1, c_r = self.__calculate_circle_center_by_three_points(
            temp_x1, temp_y1, temp_x2, temp_y2, temp_x3, temp_y3
        )
        degree = math.atan2((temp_y3 - c_y1), (temp_x3 - c_x1))
        start_degree = 180 / math.pi * degree
        degree = math.atan2((temp_y1 - c_y1), (temp_x1 - c_x1))
        end_degree = 180 / math.pi * degree
        if start_degree > 0 and end_degree < 0:
            end_degree = end_degree + 180
        if start_degree > 0 and end_degree < start_degree:
            start_degree = start_degree - 180
            end_degree = end_degree - 180
        if start_degree < 0 and end_degree > start_degree:
            start_degree = start_degree + 180
            end_degree = end_degree + 180
        self.plotter.draw_arc(
            c_x1 - c_r,
            c_y1 - c_r,
            c_r * 2,
            c_r * 2,
            start_degree,
            end_degree,
        )
        degree = math.atan2((y1 - y2), (x2 - x1))
        str_x = int(temp_x2)
        str_y = int(temp_y2)
        self.plotter.draw_text(
            str_x,
            str_y,
            f"{disp:.2f}",
            100,
            degree,
            0,
            180,
        )

    def __draw_label_and_title(self, label: str, title: str):
        start_x = self.start_x
        end_y = self.end_y
        self.plotter.draw_line(start_x, end_y + 500, start_x + 500, end_y + 500)
        self.plotter.draw_text(start_x + 800, end_y + 500, label, 100, 0)
        self.plotter.draw_text(2700, 3050, title, 130, 0)
        self.plotter.draw_line(2100, 3150, 3300, 3150)
        self.plotter.draw_line(2100, 3190, 3300, 3190, width=15)

    def __calculate_circle_center_by_three_points(self, x1, y1, x2, y2, x3, y3):
        c_x1 = (
            (y1 - y3) * (x1 * x1 - x2 * x2 + y1 * y1 - y2 * y2)
            - (y1 - y2) * (x1 * x1 - x3 * x3 + y1 * y1 - y3 * y3)
        ) / (2 * ((x1 - x2) * (y1 - y3) - (x1 - x3) * (y1 - y2)))
        c_y1 = (
            (x1 - x2) * (x1 * x1 - x3 * x3 + y1 * y1 - y3 * y3)
            - (x1 - x3) * (x1 * x1 - x2 * x2 + y1 * y1 - y2 * y2)
        ) / (2 * ((x1 - x2) * (y1 - y3) - (x1 - x3) * (y1 - y2)))
        c_r = ((x1 - c_x1) ** 2 + (y1 - c_y1) ** 2) ** 0.5
        return (c_x1, c_y1, c_r)
