import ezdxf

class BasicDXF:
    file_extension = ".dxf"
    DXF2007 = "AC1021"
    def __init__(self):
        self.doc = ezdxf.new(BasicDXF.DXF2007)
        self.model_space = self.doc.modelspace()

    def creat_test(self):
        self.__add_polyline()

    def __add_polyline(self):
        self.model_space.add_lwpolyline([[0,0],[500,0],[500,500]],close=True)



    def save(self,path:str):
        if not path.endswith(BasicDXF.file_extension):
            path += BasicDXF.file_extension
        self.doc.saveas(path)