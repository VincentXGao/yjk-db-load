from .ShapeEnum import ShapeEnum
from typing import List

class Section:
    def __init__(self,id:int,k:ShapeEnum,vals:List[float]):
        self.id = id
        self.k = k
        value_number = len(vals)
        self.b = vals[0] if value_number>=1 else None
        self.h = vals[1] if value_number>=2 else None
        self.u = vals[2] if value_number>=3 else None
        self.t = vals[3] if value_number>=4 else None
        self.d = vals[4] if value_number>=5 else None
        self.f = vals[5] if value_number>=6 else None
        

    def __str__(self):
        display_function = {
            ShapeEnum.Rect:lambda self:f"Rect-{self.b}mmx{self.h}mm",
            ShapeEnum.Circle:lambda self:f"Circle-Diameter:{self.b}mm"
        }
        return display_function[self.k](self)
    

if __name__ == "__main__":
    s = Section(1,ShapeEnum.Circle,[20,32])

    print(s)