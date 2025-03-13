from ezdxf.enums import TextEntityAlignment
from CivilTools.Const import CADConst


class DrawingAttribs:
    """这是一个基础的属性，包含图层、颜色等所有人都有的信息"""
    def __init__(self,
                 layer:str,
                 color_index:int=CADConst.BY_LAYER,
        ):
        self.layer = layer
        self.color_index = color_index
        
class PolylineAttribs(DrawingAttribs):
    """Polyline对象的属性，包括是否封闭等"""
    def  __init__(self, layer,
                  color_index:int = CADConst.BY_LAYER,
                  close:bool = False,
                  constant_width:float = 0
                  ):
        super().__init__(layer, color_index)
        self.close = close
        self.constant_width = constant_width
        """全局宽度"""
        
        
class TextAttribs(DrawingAttribs):
    def __init__(self, layer,
                 color_index:int = CADConst.BY_LAYER,
                 text_height:float = 300,
                 text_width_factor:float = 0.7,
                 text_align:TextEntityAlignment = TextEntityAlignment.MIDDLE_CENTER,
                 ):
        super().__init__(layer, color_index)
        self.text_height = text_height
        self.text_width_factor = text_width_factor
        self.text_align = text_align
        
        
        