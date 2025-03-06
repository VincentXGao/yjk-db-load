from .BuildingDefine import Beam
from .SQLiteConnector.Connector import Connector

class YDBLoader:

    def __init__(self, file_name = None):
        self.connector = Connector(file_name)
        

        
    def sum(self,x,y):
        return x+y
    
    def get_beams(self):
        a = Beam()
        return a