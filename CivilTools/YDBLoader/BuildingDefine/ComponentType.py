from enum import Enum

class ComponentType(Enum):
    Beam = 1
    Column = 2
    Wall = 3
    Slab = 4
    Brace = 5
    SlabHole = 6
    