from ..Section import Section,ShapeEnum
from ..Geometry import Joint

class Column:
    def __init__(self,id:int,joint:Joint,sect:Section):
        self.id = id
        self.joint = joint
        self.section = sect
    

