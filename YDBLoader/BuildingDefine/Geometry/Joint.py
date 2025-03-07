

class Joint:
    def __init__(self,id:int,x:float,y:float,std_flr_id:int):
        self.id = id
        self.x = x
        self.y = y
        self.std_flr_id = std_flr_id

    def __str__(self):
        return f"Joint(id:{self.id}):[x:{self.x:.4f},y:{self.y:.4f}]:stdFlrId:{self.std_flr_id}"
    

if __name__ == "__main__":
    j = Joint(1,3.1,36.6513246534313)
    print(j)