from .BasicDXF import BasicDXF
from .DrawingAttribs import DrawingAttribs,PolylineAttribs
from .LayerManager import DefaultLayers
from CivilTools.Const import Concrete,ConcreteLevel

class DetailDXF(BasicDXF):
    def __init__(self):
        super().__init__()
        

default_floor_height_table_attribs = {
    "column_con_level":None,
    "column_steel_level":None,
    "beam_con_level":None,
    "beam_steel_level":None
}

class FloorHeightTableDXF(BasicDXF):
    def __prepare(self):
        useful_layers = [
            DefaultLayers.TEXT,
            DefaultLayers.SYMBOL
        ]
        self.init_layers(useful_layers)

    def __init__(self,
                 floor_num:int,
                 default_concrete:ConcreteLevel=Concrete.C40,
                 font_size:float = 300,
                 ):
        super().__init__()
        self.__prepare()
        self.floor_num = floor_num
        self.defaul_concrete = default_concrete
        self.font_size = font_size
        
        for key, value in default_floor_height_table_attribs.items():
            setattr(self, key, value)
    
    def export_dxf(self,path):       
        self.__draw_table_grid()
        self.__draw_context()
        self._save(path)

    def __draw_table_grid(self):
        start_x = 0
        start_y = 0
        total_width = self.font_size * 20
        grid_draw_attrib = PolylineAttribs(DefaultLayers.SYMBOL.name)
        for _ in range(self.floor_num+1):
            self._add_horizental_line(start_x,start_y,total_width,grid_draw_attrib)
            start_y -= self.font_size*2\
    
    def __draw_context(self):
        self._add_text("什么？？？",[300,-500])