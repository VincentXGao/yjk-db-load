from enum import Enum

class CADColor(Enum):
    Red = 1
    Yellow = 2
    Green = 3
    Cyan = 4
    Blue = 5
    Magenta = 6
    White = 7
    Gray = 8
    LightGray = 9
    
class CADLineType(Enum):
    Continuous = 1
    DASHED = 2
    CENTER = 3
    DASHDOT = 4


class CADLayer:
    def __init__(self,name:str,color:CADColor,line_type:CADLineType=CADLineType.Continuous):
        self.name = name
        self.color = color
        self.line_type = line_type


class DefaultLayers:
    TEXT = CADLayer("0S-TEXT",CADColor.Cyan)
    SYMBOL = CADLayer("0S-SYMB",CADColor.Red)
    