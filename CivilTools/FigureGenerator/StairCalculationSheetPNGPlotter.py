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

        self.__plot_basic_stair()

    def plot_moment(self, path, moments: List[float]):
        start_x = self.start_x
        end_x = self.end_x
        start_y = self.start_y
        end_y = self.end_y

        moment_max = max([abs(i) for i in moments])
        # 用来确定弯矩最大值处的高度
        moment_height = [m / moment_max * 400 for m in moments]
        self.__draw_moment_curve(start_x, start_y, end_x, end_y, moment_height)
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

    def __draw_moment_curve(self, x1, y1, x2, y2, line_length_list: List[float]):
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
