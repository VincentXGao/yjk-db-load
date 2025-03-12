import ezdxf
import warnings
from typing import List
from .LayerManager import CADLayer, CADColor,CADLineType

class BasicDXF:
    file_extension = ".dxf"
    DXF2007 = "AC1021"
    line_type_patterns = {
        CADLineType.Continuous:[1,1],
        CADLineType.CENTER:[1,0.4,-0.2,0.1,-0.3],
        CADLineType.DASHDOT:[1,0.6,-0.2,0,-0.2],
        CADLineType.DASHED:[1,0.7,-0.3]
    }
    """线型及其Pattern定义，Pattern定义可参考ezdxf内的定义
    The simple line type pattern is a list of
    floats :code:`[total_pattern_length, elem1, elem2, ...]`
    where an element > 0 is a line, an element < 0 is a gap and  an
    element == 0.0 is a dot.
    """
        
    def __init__(self):
        self.doc = ezdxf.new(BasicDXF.DXF2007)
        self.model_space = self.doc.modelspace()
        self.__loaded_line_types = []
        
    
    def init_layers(self, layer_list:List[CADLayer]):
        layers = self.doc.layers
        for my_layer in layer_list:
            # 如果图层名称已存在，则不进行新增
            if my_layer.name in [l.dxf.name for  l in layers]:
                warnings.warn(f"Layer {my_layer.name} already existed.")
                continue
            temp_layer = layers.new(name=my_layer.name)
            temp_layer.color = my_layer.color.value
            self.__load_line_type(
                my_layer.line_type.name,
                BasicDXF.line_type_patterns[my_layer.line_type]
            )
            temp_layer.dxf.linetype = my_layer.line_type.name
    
    def creat_test(self):
        self.__add_polyline()

    def __add_polyline(self):
        polyline = self.model_space.add_lwpolyline([[0,0],[5000,0],[5000,500]],close=True)
        polyline.dxf.layer = "AA"


    
    def save(self,path:str):
        if not path.endswith(BasicDXF.file_extension):
            path += BasicDXF.file_extension
        for _ in range(10):
            try:
                self.doc.saveas(path)
            except Exception:
                path = path.replace(BasicDXF.file_extension,"1"+BasicDXF.file_extension)

    def __load_line_type(self, name:str, pattern:List[float]):
        if name in self.__loaded_line_types:
            return
        self.doc.linetypes.add(name,pattern)
        self.__loaded_line_types.append(name)
        