from .ShapeEnum import ShapeEnum
from typing import List

class Section:
    def __init__(self,
                 id:int,
                 k:ShapeEnum,
                 vals:List[float],
                 mat:int = 1
        ):
        self.id = id
        self.k = k
        self.mat = mat
        value_number = len(vals)
        self.b = vals[0] if value_number>=1 else None
        self.h = vals[1] if value_number>=2 else None
        self.u = vals[2] if value_number>=3 else None
        self.t = vals[3] if value_number>=4 else None
        self.d = vals[4] if value_number>=5 else None
        self.f = vals[5] if value_number>=6 else None
        

    def __str__(self):
        '''todo:这里需要完善str方法'''
        display_function = {
            ShapeEnum.Rect : lambda : f"Rect-{self.b}mmx{self.h}mm",
            ShapeEnum.HShape : lambda : f"{self.b}",
            ShapeEnum.Circle : lambda : f"Circle-Diameter:{self.b}mm",
            ShapeEnum.RegularPolygon : lambda : f"{self.b}",
            ShapeEnum.Groove : lambda  : f"{self.b}",
            ShapeEnum.Cross : lambda : f"{self.b}",
            ShapeEnum.Box : lambda : f"{self.b}",
            ShapeEnum.CircleTube : lambda : f"{self.b}",
            ShapeEnum.CircleCFT : lambda : f"{self.b}",
            ShapeEnum.HSRC : lambda : f"{self.b}",
            ShapeEnum.BoxSRC : lambda : f"{self.b}",
            ShapeEnum.CrossSRC : lambda : f"{self.b}",
            
            ShapeEnum.UnKnown : lambda : f"Unknown:{self.b}"
        }
        return display_function[self.k]()
    
    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    s = Section(1,ShapeEnum.Circle,[20,32])

    print(s)