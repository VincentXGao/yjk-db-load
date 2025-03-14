from .BasicDXF import BasicDXF
from .DrawingAttribs import (
    DrawingAttribs,
    PolylineAttribs,
    TextAttribs,
    TextEntityAlignment,
)
from .LayerManager import DefaultLayers
from CivilTools.Const import Concrete, ConcreteLevel


class DetailDXF(BasicDXF):
    def __init__(self):
        super().__init__()


default_floor_height_table_attribs = {
    "column_con_level": None,
    "column_steel_level": None,
    "beam_con_level": None,
    "beam_steel_level": None,
}


class FloorHeightTableDXF(BasicDXF):
    def __prepare(self):
        useful_layers = [DefaultLayers.TEXT, DefaultLayers.SYMBOL]
        self.init_layers(useful_layers)

    def __init__(
        self,
        floor_num: int,
        default_concrete: ConcreteLevel = Concrete.C40,
        font_size: float = 300,
    ):
        super().__init__()
        self.__prepare()
        self.floor_num = floor_num
        self.defaul_concrete = default_concrete
        self.font_size = font_size
        self.table_title = None
        self.insert_point = [0, 0]

        for key, value in default_floor_height_table_attribs.items():
            setattr(self, key, value)

    def export_dxf(self, path):
        self._remove_all_entities()
        self.__draw_table_title()
        self.__draw_table_grid()
        self.__draw_context()
        self._save(path)

    def set_table_title(self, title: str):
        self.table_title = title

    def set_embeding_floor(self):
        return NotImplemented

    def __draw_table_title(self):
        if self.table_title == None:
            return
        text_attrib = TextAttribs(
            DefaultLayers.TEXT.name,
            text_height=self.font_size,
            text_align=TextEntityAlignment.MIDDLE_LEFT,
        )
        self._add_text(
            self.table_title,
            [self.insert_point[0], self.insert_point[1] + self.font_size * 1.5],
            text_attrib,
        )

    def __draw_table_grid(self):
        start_x = 0
        start_y = 0
        total_width = self.font_size * 20
        total_height = self.font_size * 2 * self.floor_num
        grid_draw_attrib = PolylineAttribs(DefaultLayers.SYMBOL.name)
        for _ in range(self.floor_num + 1):
            self._add_horizental_line(start_x, start_y, total_width, grid_draw_attrib)
            start_y -= self.font_size * 2
        start_y = 0
        for _ in range(6):
            self._add_vertical_line(start_x, start_y, -total_height, grid_draw_attrib)
            start_x += self.font_size * 4

    def __draw_context(self):
        for i in range(self.floor_num):
            for j in range(5):
                self._add_text(
                    "什么?",
                    [self.font_size * (4 * j + 2), -self.font_size * (2 * i + 1)],
                    TextAttribs(DefaultLayers.TEXT.name, text_height=self.font_size),
                )

    def __draw_embeding_dimension(self):
        return NotImplemented
