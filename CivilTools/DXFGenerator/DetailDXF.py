from typing import List
from .BasicDXF import BasicDXF
from .DrawingAttribs import (
    DrawingAttribs,
    PolylineAttribs,
    TextAttribs,
    TextEntityAlignment,
)
from .LayerManager import DefaultLayers, CADColor
from CivilTools.Const import Concrete, ConcreteLevel, Steel, SteelLevel


class DetailDXF(BasicDXF):
    def __init__(self):
        super().__init__()


default_floor_height_table_attribs = {
    "column_con_level": None,
    "column_steel_level": None,
    "beam_con_level": None,
    "beam_steel_level": None,
}


class FloorInformation:
    def __init__(
        self,
        name: str,
        archi_elevation: float,
        plaster_thickness: float = 200,
        beam_slab_con_mat: ConcreteLevel = Concrete.C35,
        wall_con_mat: ConcreteLevel = Concrete.C60,
        column_con_mat: ConcreteLevel = Concrete.C50,
        brace_con_mat: ConcreteLevel = Concrete.C50,
        beam_steel_mat: SteelLevel = Steel.HRB300,
        column_steel_mat: SteelLevel = Steel.Q355,
        brace_steel_mat: SteelLevel = Steel.Q355,
    ):
        if plaster_thickness < 0:
            raise ValueError("Plaster value should be non-negitive.")
        self.floor_name = name
        self.__struct_elevation = archi_elevation - plaster_thickness
        self.__archi_elevation = archi_elevation

        self.beam_slab_con_mat = beam_slab_con_mat
        self.wall_con_mat = wall_con_mat
        self.column_con_mat = column_con_mat
        self.brace_con_mat = brace_con_mat

        self.beam_steel_mat = beam_steel_mat
        self.column_steel_mat = column_steel_mat
        self.brace_steel_mat = brace_steel_mat

    def get_attribute_by_name(self, attrib_name: str):
        if "楼层号" in attrib_name:
            return self.floor_name
        if "建筑" in attrib_name and "标高" in attrib_name:
            return self.archi_elevation
        if "结构" in attrib_name and "标高" in attrib_name:
            return self.struct_elevation
        if "柱" in attrib_name:
            return self.column_con_mat.name
        if "墙" in attrib_name:
            return self.wall_con_mat.name
        if "板" in attrib_name:
            return self.beam_slab_con_mat.name

    @property
    def struct_elevation(self):
        if self.__struct_elevation == 0:
            return "±0.000"
        return f"{self.__struct_elevation/1000:.3f}"

    @property
    def archi_elevation(self):
        if self.__archi_elevation == 0:
            return "±0.000"
        return f"{self.__archi_elevation/1000:.3f}"


class FloorHeightTableDXF(BasicDXF):
    def __prepare(self):
        useful_layers = [DefaultLayers.TEXT, DefaultLayers.SYMBOL]
        self.init_layers(useful_layers)

    def __init__(
        self,
        above_floor_num: int,
        under_floor_num: int,
        base_elevation: float,
        font_size: float = 300,
    ):
        super().__init__()
        self.__prepare()
        self.__above_floor_num = above_floor_num
        self.__under_floor_num = under_floor_num
        self.__base_elevation = base_elevation
        self.floor_num = above_floor_num + under_floor_num
        self.floors = self.__create_floors()
        self.__font_size = font_size
        self.__table_title = None
        self.insert_point = [0, 0]

        for key, value in default_floor_height_table_attribs.items():
            setattr(self, key, value)

    def __create_floors(self) -> List[FloorInformation]:
        result = []
        for i in range(self.__above_floor_num):
            temp_floor = FloorInformation(f"F{i+1}", self.__base_elevation + 3500 * i)
            result.append(temp_floor)
        for i in range(self.__under_floor_num):
            temp_floor = FloorInformation(
                f"B{i+1}", self.__base_elevation - 3500 * (i + 1)
            )
            result.insert(0, temp_floor)
        return result

    def export_dxf(self, path):
        self._remove_all_entities()
        self.__draw_table_title()
        self.__analysis_table_columns()
        self.__draw_table_grid()
        self.__draw_table_column_title()
        self.__draw_context()
        self._save(path)

    def set_table_title(self, title: str):
        self.__table_title = title

    def set_font_size(self, font_size: float):
        self.__font_size = font_size

    def set_embeding_floor(self):
        return NotImplemented

    def __analysis_table_columns(self):
        self.__columns = []
        self.__column_widths = []

        self.__columns.append("当前层")
        self.__column_widths.append(3)

        self.__columns.append("建筑楼层号")
        self.__column_widths.append(5)

        self.__columns.append("建筑标高(m)")
        self.__column_widths.append(6)

        self.__columns.append("结构标高(m)")
        self.__column_widths.append(6)

        self.__first_part_column_num = len(self.__columns)

        self.__columns.append("结构柱")
        self.__column_widths.append(3)

        self.__columns.append("剪力墙")
        self.__column_widths.append(3)

        self.__columns.append("梁/板")
        self.__column_widths.append(3)

    def __draw_table_title(self):
        if self.__table_title == None:
            return
        text_attrib = TextAttribs(
            DefaultLayers.TEXT.name,
            text_height=self.__font_size,
            text_align=TextEntityAlignment.MIDDLE_LEFT,
        )
        self._add_text(
            self.__table_title,
            [self.insert_point[0], self.insert_point[1] + self.__font_size * 1.5],
            text_attrib,
        )

    def __draw_table_grid(self):
        first_part_column_num = self.__first_part_column_num
        start_x = self.insert_point[0]
        start_y = self.insert_point[1]
        font_factor = self.__font_size

        total_width = font_factor * sum(self.__column_widths)
        first_part_width = font_factor * sum(
            self.__column_widths[:first_part_column_num]
        )

        total_height = font_factor * 2 * (self.floor_num + 2)
        grid_draw_attrib = PolylineAttribs(DefaultLayers.SYMBOL.name)
        for i in range(self.floor_num + 3):
            if i == 1:
                self._add_horizental_line(
                    start_x + first_part_width,
                    start_y,
                    total_width - first_part_width,
                    grid_draw_attrib,
                )
            else:
                self._add_horizental_line(
                    start_x, start_y, total_width, grid_draw_attrib
                )
            start_y -= font_factor * 2
        start_y = 0
        for i in range(len(self.__columns) + 1):
            if i <= first_part_column_num or i == len(self.__columns):
                self._add_vertical_line(
                    start_x, start_y, -total_height, grid_draw_attrib
                )
            else:
                self._add_vertical_line(
                    start_x,
                    start_y - font_factor * 2,
                    -total_height + font_factor * 2,
                    grid_draw_attrib,
                )
            if i == len(self.__columns):
                continue
            start_x += font_factor * self.__column_widths[i]

    def __draw_table_column_title(self):
        font_factor = self.__font_size
        start_x = self.insert_point[0]
        start_y = self.insert_point[1]
        for i in range(len(self.__columns)):
            temp_string = self.__columns[i]
            temp_x = (
                sum(self.__column_widths[: i + 1]) - self.__column_widths[i] / 2
            ) * font_factor
            temp_y = (
                -font_factor * 2
                if i < self.__first_part_column_num
                else -font_factor * 3
            )
            self._add_text(
                temp_string,
                [start_x + temp_x, start_y + temp_y],
                TextAttribs(
                    DefaultLayers.TEXT.name,
                    text_height=font_factor,
                    text_align=TextEntityAlignment.MIDDLE_CENTER,
                ),
            )

    def __draw_context(self):
        font_factor = self.__font_size

        start_x = self.insert_point[0]
        start_y = self.insert_point[1] - font_factor * 4
        for i in range(len(self.floors)):
            temp_floor = self.floors[::-1][i]
            for j in range(1, len(self.__columns)):
                temp_insert_point = [
                    start_x + font_factor * (sum(self.__column_widths[: j + 1]) - 0.5),
                    start_y - font_factor * (2 * i + 1),
                ]
                temp_string = temp_floor.get_attribute_by_name(self.__columns[j])
                self._add_text(
                    temp_string,
                    temp_insert_point,
                    TextAttribs(
                        DefaultLayers.TEXT.name,
                        color_index=CADColor.Yellow.value,
                        text_height=font_factor,
                        text_align=TextEntityAlignment.MIDDLE_RIGHT,
                    ),
                )

    def __draw_embeding_dimension(self):
        return NotImplemented
