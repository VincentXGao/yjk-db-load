import math
import abc
from typing import List
import matplotlib.pyplot as plt

class SinglePeriod:
    """单个周期
    """
    def __init__(
        self,index:int,
        time:float, 
        angle:float = 0,
        coeff_x:float = 1,
        coeff_y:float = 0,
        coeff_z:float = 0,
        mass_particpate_x:float = 0,
        mass_particpate_y:float = 0,
        mass_particpate_z:float = 0,
    ):
        self.index = index
        self.time = time
        self.angle = angle
        assert abs(coeff_x 
                   + coeff_y 
                   + coeff_z-1)<0.01 ,"The sum of three participite coeff should == 1"
        self.coeff_x = coeff_x
        self.coeff_y = coeff_y
        self.coeff_z = coeff_z
        self.mass_participate_x = mass_particpate_x
        self.mass_participate_y = mass_particpate_y
        self.mass_participate_z = mass_particpate_z
        
    def __str__(self):
        return f"T{self.index}:\t{self.time:.4f}s\t[X:{self.coeff_x*100:.1f}%;\tY:{self.coeff_y*100:.1f}%;\tZ:{self.coeff_z*100:.1f}%]"  
    
    def __repr__(self):
        return str(self) 

class Period:
    def __init__(self,periods:List[SinglePeriod] , model_type = None):
        self.periods = periods
        
    def __str__(self):
        if len(self.periods)<=10:
            return "\n".join([str(period) for period in self.periods])
        else:
            result = "\n".join([str(period) for period in self.periods[:9]])
            result += "\n....\n"
            result += str(self.periods[-1])
            return result
        
    def __repr__(self):
        return self.__str__()
    
class ValuePeer:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y
    def __str__(self):
        if self.x >500:
            return f"X:{self.x:.1f}\tY:{self.y:.1f}"
        elif self.x >5:
            return f"X:{self.x:.2f}\tY:{self.y:.2f}"
        else:
            return f"X:{self.x:.3f}\tY:{self.y:.3f}"
    
class FloorSeismicResult:
    def __init__(self,
                 floor_num: int,
                 tower_num: int,
                 force:ValuePeer = None,
                 shear:ValuePeer = None,
                 moment:ValuePeer = None,
                 disp:ValuePeer = None,
                 stiffness:ValuePeer = None,
                 shear_capacity:ValuePeer = None,
                 ):
        self.floor_num = floor_num
        self.tower_num = tower_num
        self.force = force
        self.shear = shear
        self.moment = moment
        self.disp = disp
        self.stiffness = stiffness
        self.shear_capacity = shear_capacity
    
    def __str__(self):
        return f"Flr.{self.floor_num}:Fx={self.force.x};Fy={self.force.y}"

    def __repr__(self):
        return self.__str__()

class SeismicResult:
    def __init__(self,
                 floor_result : List[FloorSeismicResult]
        ):
        self.floor_result = floor_result
    
    @property
    def seismic_shear_x(self):
        return [i.shear.x for i in self.floor_result]
    
    @property
    def floor_index(self):
        return [i+1 for i in range(len(self.floor_result))]
    
    def plot_shear(self):
        fig,ax = plt.subplots(figsize=(2,5))
        ax.plot(self.seismic_shear_x,self.floor_index)
        return fig,ax
    
    def __str__(self):
        result = f"Total floor: {len(self.floor_result)}\n"
        for temp_result in self.floor_result:
            result += str(temp_result)
            result += "\n"
        return result
    
    def __repr__(self):
        return self.__str__()
    
    
if __name__ == "__main__":
    p_list = []
    for i in range(112):
        p_list.append(SinglePeriod(i+1,i*0.1+0.1,0,1-i*0.1,i*0.1,0))
    P = Period(p_list)
    print(str(P))