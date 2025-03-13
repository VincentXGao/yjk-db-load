class DrawingAttribs:
    def __init__(self,
                 layer:str,
                 color_index:int=256,
        ):
        self.layer = layer
        self.color_index = color_index
        
class PolylineAttribs(DrawingAttribs):
    def  __init__(self, layer, color_index = 256, close:bool = False):
        super().__init__(layer, color_index)
        self.close = close
        
        
class TextAttribs(DrawingAttribs):
    def __init__(self, layer, color_index = 256):
        super().__init__(layer, color_index)