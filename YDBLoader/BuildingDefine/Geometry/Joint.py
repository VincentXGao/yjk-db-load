

class Joint:
    def __init__(self,id:int,x:float,y:float,stdFlrID:int):
        self.id = id
        self.x = x
        self.y = y
        self.stdFlrID = stdFlrID

    def __str__(self):
        return f"Joint(id:{self.id}):[x:{self.x:.4f},y:{self.y:.4f}]:stdFlrId:{self.stdFlrID}"
    

if __name__ == "__main__":
    j = Joint(1,3.1,36.6513246534313)
    print(j)