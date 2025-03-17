import math
from .StairComponent import Component
from typing import List


class Position:
    @property
    def lower_elevation(self):
        return min(self.left_elevation, self.right_elevation)

    @property
    def higher_elevation(self):
        return max(self.left_elevation, self.right_elevation)

    @property
    def total_height(self):
        return self.higher_elevation - self.lower_elevation

    @property
    def left_plat_length(self):
        return self.left_x2 - self.left_x1

    @property
    def right_plat_length(self):
        return self.right_x2 - self.right_x1

    @property
    def main_plat_length(self):
        return self.right_x1 - self.left_x2

    def __init__(
        self, left_elevation, right_elevation, left_x1, left_x2, right_x1, right_x2
    ):
        self.left_elevation = left_elevation
        self.right_elevation = right_elevation
        self.left_x1 = left_x1
        self.left_x2 = left_x2
        self.right_x1 = right_x1
        self.right_x2 = right_x2


class StairBeam:

    def __init__(self, width, height, offset):
        self.width = width
        self.height = height
        self.offset = offset


class StairPart:

    @property
    def stair_type(self):
        left_extend = self.beam_list[1].offset + self.beam_list[1].width / 2
        right_extend = self.beam_list[2].offset + self.beam_list[2].width / 2
        if left_extend >= self.STAIR_EXTEND_LIMIT:
            if right_extend >= self.STAIR_EXTEND_LIMIT:
                return "DT"
            else:
                return "BT"
        else:
            if right_extend >= self.STAIR_EXTEND_LIMIT:
                return "CT"
            else:
                return "AT"

    @property
    def stair_elevation_range(self):
        return f"{self.position.lower_elevation/1000:.3f}~{self.position.higher_elevation/1000:.3f}"

    @property
    def total_height(self):
        return abs(self.position.left_elevation - self.position.right_elevation)

    @property
    def equivlent_main_slab_thick(self):
        slope = math.atan(self.position.total_height / self.position.main_plat_length)
        thick_1 = self.main_thick / math.cos(slope)
        thick_2 = self.position.total_height / self.step_num / 2
        return thick_1 + thick_2

    @property
    def total_horizental_length(self):
        length = self.position.right_x1 - self.position.left_x2
        length += self.beam_list[1].offset + self.beam_list[1].width / 2
        length += self.beam_list[2].offset + self.beam_list[2].width / 2
        return length

    @property
    def left_extend_length(self):
        if self.stair_type == "AT" or self.stair_type == "CT":
            return 0
        else:
            return self.beam_list[1].offset + self.beam_list[1].width / 2

    @property
    def right_extend_length(self):
        if self.stair_type == "AT" or self.stair_type == "BT":
            return 0
        else:
            return self.beam_list[2].offset + self.beam_list[2].width / 2

    @property
    def stair_length_list(self):
        return [
            self.left_extend_length,
            self.total_horizental_length
            - self.left_extend_length
            - self.right_extend_length,
            self.right_extend_length,
        ]

    @property
    def up_real_rebar_str(self):
        return f"E{self.up_d:d}@{self.up_dis:d}"

    @property
    def up_real_rebar_area(self):
        return f"{(self.up_d*self.up_d * math.pi/4/self.up_dis):.3f}"

    def get_calculate_moments(self) -> List[float]:
        if self.stair_type == "AT":
            return [0, 0, self.components[0].m_2, 0, 0]
        elif self.stair_type == "BT":
            return [0, self.components[0].m_2, self.components[1].m_2, 0, 0]
        elif self.stair_type == "CT":
            return [0, 0, self.components[0].m_2, self.components[1].m_2, 0]
        elif self.stair_type == "DT":
            return [
                0,
                self.components[0].m_2,
                self.components[1].m_2,
                self.components[2].m_2,
                0,
            ]
        return [0, 10, 20, 10, 0]

    def get_calculate_shears(self) -> List[float]:
        if self.stair_type == "AT":
            return [
                0,
                0,
                self.components[0].v1,
                self.components[0].v2,
                self.components[1].v1,
                self.components[1].v2,
                0,
                0,
            ]
        elif self.stair_type == "BT":
            return [
                self.components[0].v1,
                self.components[0].v2,
                self.components[1].v1,
                self.components[1].v2,
                self.components[2].v1,
                self.components[2].v2,
                0,
                0,
            ]
        elif self.stair_type == "CT":
            return [
                0,
                0,
                self.components[0].v1,
                self.components[0].v2,
                self.components[1].v1,
                self.components[1].v2,
                self.components[2].v1,
                self.components[2].v2,
            ]
        elif self.stair_type == "DT":
            return [
                self.components[0].v1,
                self.components[0].v2,
                self.components[1].v1,
                self.components[1].v2,
                self.components[2].v1,
                self.components[2].v2,
                self.components[3].v1,
                self.components[3].v2,
            ]
        return [0, 0, 0, 10, 20, 10, 0, 0]

    def get_left_slab_table_moments(self):
        moments = self.get_calculate_moments()
        return [0, moments[1] * 0.25, moments[1]]

    def get_main_table_moments(self):
        moments = self.get_calculate_moments()
        return [moments[1], moments[2], moments[3]]

    def get_right_slab_table_moments(self):
        moments = self.get_calculate_moments()
        return [moments[3], moments[3] * 0.25, 0]

    def get_left_slab_table_shears(self):
        shears = self.get_calculate_shears()
        return [shears[0], (shears[0] + shears[1]) / 2, shears[1]]

    def get_main_table_shears(self):
        shears = self.get_calculate_shears()
        return [shears[2], (shears[2] + shears[5]) / 2, shears[5]]

    def get_right_slab_table_shears(self):
        shears = self.get_calculate_shears()
        return [shears[6], (shears[6] + shears[7]) / 2, shears[7]]

    def get_shear_validate(self, which_side, ft, cover_thick):
        if which_side == "left":
            shears = self.get_left_slab_table_shears()
            shear_limit = 0.7 * 1 * ft * (self.left_thick - cover_thick) * 1000 / 1000
        elif which_side == "right":
            shears = self.get_right_slab_table_shears()
            shear_limit = 0.7 * 1 * ft * (self.right_thick - cover_thick) * 1000 / 1000
        else:
            shears = self.get_main_table_shears()
            shear_limit = 0.7 * 1 * ft * (self.main_thick - cover_thick) * 1000 / 1000
        max_shear = max([abs(i) for i in shears])
        if max_shear <= shear_limit:
            shear_context = f"Vmax={max_shear:.2f}kN < 0.7βhftbh0={shear_limit:.2f}kN，抗剪截面满足要求！"
        else:
            shear_context = f"Vmax={max_shear:.2f}kN > 0.7βhftbh0={shear_limit:.2f}kN，抗剪截面不满足要求！"

        return shear_context

    def init_default_data(self):
        self.stair_width = 1500
        self.stair_well_width = 100
        self.beam_list = [
            StairBeam(300, 500, 0),
            StairBeam(300, 500, 0),
            StairBeam(300, 500, 0),
            StairBeam(300, 500, 0),
        ]
        self.set_thickness(140, 140, 140)
        self.set_real_rebar(10, 150, 10, 150)

    def __init__(self, position: Position, step_num):
        self.position = position
        self.step_num = step_num
        self.init_default_data()

        self.STAIR_EXTEND_LIMIT = 200

    def set_thickness(self, left_thick, main_thick, right_thick):
        self.left_thick = left_thick
        self.main_thick = main_thick
        self.right_thick = right_thick

    def set_beam_offset(self, i, offset):
        self.beam_list[i].offset = offset

    def set_real_rebar(self, up_d, up_dis, down_d, down_dis):
        self.up_d = up_d
        self.up_dis = up_dis
        self.down_d = down_d
        self.down_dis = down_dis

    def set_calculate_result(self, components: List[Component]):
        self.components = components
