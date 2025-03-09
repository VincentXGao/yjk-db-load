from ..Section import Section,ShapeEnum
from ..Geometry import Joint

class Beam:
    def __init__(
        self,
        id:int,
        start_joint:Joint,
        end_joint:Joint,
        section:Section
        ):
        self.id = id 
        self.start_joint = start_joint
        self.end_joint = end_joint
        self.section = section
        
    def __str__(self):
        return f"Beam:{self.id}-{str(self.section)}"
    
    def __repr__(self):
        return self.__str__()