from ..Section import Section, ShapeEnum
from ..Geometry import Joint


class Beam:
    def __init__(self, id: int, start_joint: Joint, end_joint: Joint, section: Section):
        self.id = id
        self.start_joint = start_joint
        self.end_joint = end_joint
        self.section = section
        self.std_flr_id = self.start_joint.std_flr_id

    def get_data_for_plot(self):
        return [
            [self.start_joint.x, self.end_joint.x],
            [self.start_joint.y, self.end_joint.y],
        ]

    def __str__(self):
        return f"Beam:{self.id}-{str(self.section)}"

    def __repr__(self):
        return self.__str__()
