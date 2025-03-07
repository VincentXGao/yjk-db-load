from enum import Enum

class ShapeEnum(Enum):
    # 矩形
    Rect = 1
    # 工字型
    HShape = 2
    # 圆形
    Circle = 3
    # 正多边形
    RegularPolygon = 4
    # 槽型
    Groove = 5
    # 十字形
    Cross = 6
    # 箱形
    Box = 7
    # 圆管
    CircleTube = 8
    # 钢管混凝土
    CircleCFT = 12
    # 工形劲
    HSRC = 13
    # 箱型劲
    BoxSRC = 14
    
    @classmethod
    def ConvertToShapeEnum(cls,index:int):
        try: 
            return (ShapeEnum)(index)
        except ValueError:
            raise ValueError(f"Shape kind ${index} is not supported yet.")
    
    
    