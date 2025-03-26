from docx.oxml.xmlchemy import BaseOxmlElement
from docx.oxml.ns import qn, nsdecls
from CivilTools.YDBLoader.BuildingDefine.StairPart import StairPart, Component
import numpy as np
from CivilTools.Const import ConcreteLevel, SteelLevel
from typing import List


# 网上找的代码，有点东西
# https://stackoverflow.com/questions/33069697/how-to-setup-cell-borders-with-python-docx
# 这个是github上的讨论帖，在讨论帖中找到的
# https://github.com/python-openxml/python-docx/issues/1306
def set_cell_border(cell, **kwargs):
    """
    Set cell`s border
    Usage:

    set_cell_border(
        cell,
        top={"sz": 12, "val": "single", "color": "#FF0000", "space": "0"},
        bottom={"sz": 12, "color": "#00FF00", "val": "single"},
        start={"sz": 24, "val": "dashed", "shadow": "true"},
        end={"sz": 12, "val": "dashed"},
    )
    """
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()

    # check for tag existnace, if none found, then create one
    tc_borders = tc_pr.first_child_found_in("w:tcBorders")
    if tc_borders is None:
        tc_borders = BaseOxmlElement("w:tcBorders")
        tc_pr.append(tc_borders)

    # list over all available tags
    for edge in ("start", "top", "end", "bottom", "insideH", "insideV"):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = "w:{}".format(edge)

            # check for tag existnace, if none found, then create one
            element = tc_borders.find(qn(tag))
            if element is None:
                element = BaseOxmlElement(tag)
                tc_borders.append(element)

            # looks like order of attributes is important
            for key in ["sz", "val", "color", "space", "shadow"]:
                if key in edge_data:
                    element.set(qn("w:{}".format(key)), str(edge_data[key]))


def analysis_sub_and_super_script(context: str):
    """根据字符串中的'_'与'^'标志的上下标（上下标需要被{}包围起来），将字符串分隔并返回上下标结果
    返回的sub_or_super列表中，0代表常规字符，1代表下标，2代表上标，3代表highlighted
    Args:
        context (str): 输入的文字
    """
    contexts = []
    sub_or_super = [0]
    i = 0
    j = 0
    length = len(context)
    flag = False
    index_for_flag = {"_": 1, "^": 2, "*": 3}

    for c in context:
        if (c in index_for_flag.keys()) and (j < length and context[j + 1] == "{"):
            flag = True
            contexts.append(context[i:j])
            sub_or_super.append(index_for_flag[c])
            i = j + 2
        if flag and c == "}":
            contexts.append(context[i:j])
            sub_or_super.append(0)
            i = j + 1
            flag = False
        j += 1
    contexts.append(context[i:j])
    return contexts, sub_or_super


def add_comma_in_num_str(num: int):
    if not isinstance(num, int):
        raise ValueError("Only int number can be added.")
    num_str = str(num)[::-1]
    result = ""
    for i in range(len(num_str)):
        if i > 0 and i % 3 == 0 and num_str[i] != "-":
            result = "," + result
        result = num_str[i] + result
    return result


class MatrixSolver:
    def __init__(self, stair: StairPart):
        self.stair = stair
        self.cut_point = 0.5

    def set_load(self, q1, q2, q3):
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3

    def pre_analysis(self):
        concrete_e = 30000
        uniform_b = 1000
        top_y = (
            self.stair.position.higher_elevation - self.stair.position.lower_elevation
        )
        if self.stair.stair_type == "AT":
            self.point_num = 3
            self.boundary = np.array([0, 0, 1, 1, 1, 1, 0, 0, 1])

            point1 = [0, 0]
            point2 = [self.stair.total_horizental_length, top_y]
            point_middle = self.calculate_middle_point(point1, point2, self.cut_point)
            comp1 = Component(point1, point_middle)
            comp2 = Component(point_middle, point2)
            comp1.set_vertical_q(self.q2)
            comp1.set_comp_attr(concrete_e, uniform_b, self.stair.main_thick)
            comp2.set_vertical_q(self.q2)
            comp2.set_comp_attr(concrete_e, uniform_b, self.stair.main_thick)
            self.comp_list = [comp1, comp2]

        elif self.stair.stair_type == "BT":
            self.point_num = 4
            self.q_list = [self.q1, self.q2, self.q2]
            self.boundary = np.array([0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1])
            point0 = [0, 0]
            point1 = [self.stair.left_extend_length, 0]
            point2 = [self.stair.total_horizental_length, top_y]
            point_middle = self.calculate_middle_point(point1, point2, self.cut_point)
            comp1 = Component(point0, point1)
            comp2 = Component(point1, point_middle)
            comp3 = Component(point_middle, point2)
            comp1.set_vertical_q(self.q1)
            comp1.set_comp_attr(concrete_e, uniform_b, self.stair.left_thick)
            comp2.set_vertical_q(self.q2)
            comp2.set_comp_attr(concrete_e, uniform_b, self.stair.main_thick)
            comp3.set_vertical_q(self.q2)
            comp3.set_comp_attr(concrete_e, uniform_b, self.stair.main_thick)
            self.comp_list = [comp1, comp2, comp3]

        elif self.stair.stair_type == "CT":
            self.point_num = 4
            self.q_list = [self.q2, self.q2, self.q3]
            self.boundary = np.array([0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1])

            point1 = [0, 0]
            point2 = [
                self.stair.total_horizental_length - self.stair.right_extend_length,
                top_y,
            ]
            point3 = [self.stair.total_horizental_length, top_y]
            point_middle = self.calculate_middle_point(point1, point2, self.cut_point)
            comp1 = Component(point1, point_middle)
            comp2 = Component(point_middle, point2)
            comp3 = Component(point2, point3)
            comp1.set_vertical_q(self.q2)
            comp1.set_comp_attr(concrete_e, uniform_b, self.stair.main_thick)

            comp2.set_vertical_q(self.q2)
            comp2.set_comp_attr(concrete_e, uniform_b, self.stair.main_thick)

            comp3.set_vertical_q(self.q3)
            comp3.set_comp_attr(concrete_e, uniform_b, self.stair.right_thick)
            self.comp_list = [comp1, comp2, comp3]

        else:
            self.point_num = 5
            self.q_list = [self.q1, self.q2, self.q2, self.q3]
            self.boundary = np.array([0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1])

            point0 = [0, 0]
            point1 = [self.stair.left_extend_length, 0]
            point2 = [
                self.stair.total_horizental_length - self.stair.right_extend_length,
                top_y,
            ]
            point3 = [self.stair.total_horizental_length, top_y]
            point_middle = self.calculate_middle_point(point1, point2, self.cut_point)
            comp1 = Component(point0, point1)
            comp2 = Component(point1, point_middle)
            comp3 = Component(point_middle, point2)
            comp4 = Component(point2, point3)

            comp1.set_vertical_q(self.q1)
            comp1.set_comp_attr(concrete_e, uniform_b, self.stair.left_thick)
            comp2.set_vertical_q(self.q2)
            comp2.set_comp_attr(concrete_e, uniform_b, self.stair.main_thick)
            comp3.set_vertical_q(self.q2)
            comp3.set_comp_attr(concrete_e, uniform_b, self.stair.main_thick)
            comp4.set_vertical_q(self.q3)
            comp4.set_comp_attr(concrete_e, uniform_b, self.stair.right_thick)
            self.comp_list = [comp1, comp2, comp3, comp4]

    def calculate_middle_point(self, p1, p2, cut_point):
        x = p1[0] + (p2[0] - p1[0]) * cut_point
        y = p1[1] + (p2[1] - p1[1]) * cut_point
        return [x, y]

    def submit_problem(self):
        self.pre_analysis()
        comp_num = len(self.comp_list)
        total_k = np.zeros((comp_num * 3 + 3, comp_num * 3 + 3))
        total_f = np.zeros((comp_num * 3 + 3, 1))
        for i in range(len(self.comp_list)):
            comp = self.comp_list[i]
            temp_k = comp.create_k()
            temp_f = comp.create_f()
            total_k[i * 3 : i * 3 + 6, i * 3 : i * 3 + 6] += temp_k
            total_f[i * 3 : i * 3 + 6, :] += temp_f
        # 生成缩减矩阵并计算
        new_k = np.delete(total_k, np.nonzero(self.boundary == 0), axis=0)
        new_k = np.delete(new_k, np.nonzero(self.boundary == 0), axis=1)
        new_f = np.delete(total_f, np.nonzero(self.boundary == 0), axis=0)
        new_u = np.dot(np.linalg.inv(new_k), new_f)

        total_u = self.boundary.copy().reshape(-1, 1).astype(float)
        total_u[np.nonzero(total_u == 1)[0]] = new_u

        # 计算每个构件端点的数据
        for i in range(len(self.comp_list)):
            comp = self.comp_list[i]
            comp_u = total_u[i * 3 : i * 3 + 6]
            comp_f = np.dot(comp.create_k(), comp_u)
            comp_f -= comp.create_f()
            comp.set_f(comp_f[0][0], comp_f[1][0], comp_f[3][0], comp_f[4][0])
            comp.set_m(comp_f[2][0], comp_f[5][0])
        return self.comp_list


class ConcreteSolver:
    @classmethod
    def CalculateRebar(
        cls,
        moment: float,
        thickness: float,
        rebar_d: float,
        cover_thickness: float,
        concrete: ConcreteLevel,
        rebar: SteelLevel,
        min_rebar_ratio: float = 0.002,
    ) -> List[float]:
        h0 = thickness - rebar_d / 2 - cover_thickness
        alpha_s = abs(moment) * 1000000 / concrete.fc / 1000 / h0 / h0
        temp_yita = 1 - (1 - 2 * alpha_s) ** 0.5
        rebar_cal = temp_yita * concrete.fc * 1000 * h0 / rebar.fy
        rebar_min = thickness * min_rebar_ratio * 1000
        result = [max(rebar_cal, rebar_min), rebar_min]
        if moment < 0:
            return result
        else:
            return result[::-1]
