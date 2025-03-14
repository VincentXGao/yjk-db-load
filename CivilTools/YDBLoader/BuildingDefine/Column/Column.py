from ..Section import Section, ShapeEnum
from ..Geometry import Joint


class Column:
    def __init__(self, id: int, joint: Joint, section: Section):
        self.id = id
        self.joint = joint
        self.std_flr_id = joint.std_flr_id
        self.section = section

    def __str__(self):
        return f"Column:{self.id}-{str(self.section)}"

    def __repr__(self):
        return self.__str__()
