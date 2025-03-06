from .ShapeEnum import ShapeEnum
from typing import List

class Section:
    def __init__(self,id:int,k:ShapeEnum,vals:List[float]):
        self.id = id
        self.k = k
        self.b = vals[0]
        self.h = vals[1]

    def __str__(self):
        display_function = {
            ShapeEnum.Rect:lambda self:f"Rect-{self.b}mmx{self.h}mm",
            ShapeEnum.Circle:lambda self:f"Circle-Radius:{self.b}mm"
        }
        return display_function[self.k](self)
    

if __name__ == "__main__":
    s = Section(1,ShapeEnum.Circle,[20,32])

    print(s)