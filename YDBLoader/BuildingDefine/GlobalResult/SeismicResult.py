import math
from typing import List

class SinglePeriod:
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
    
    
if __name__ == "__main__":
    p_list = []
    for i in range(112):
        p_list.append(SinglePeriod(i+1,i*0.1+0.1,0,1-i*0.1,i*0.1,0))
    P = Period(p_list)
    print(str(P))