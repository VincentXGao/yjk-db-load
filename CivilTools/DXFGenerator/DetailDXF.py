from .BasicDXF import BasicDXF
from .LayerManager import DefaultLayers

class DetailDXF(BasicDXF):
    def __init__(self):
        super().__init__()
        



class FloorHeightTableDXF(BasicDXF):
    
    def __prepare(self):
        useful_layers = [
            DefaultLayers.TEXT,
            DefaultLayers.SYMBOL
        ]
        self.init_layers(useful_layers)

    def __init__(self):
        super().__init__()
        self.__prepare()
    
    def export_dxf(self,path):
        self.save(path)
