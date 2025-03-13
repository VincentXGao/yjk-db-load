
class ConcreteLevel:
    def __init__(
        self,
        level:int,
        fck:float,
        ftk:float,
        fc:float,
        ft:float,
        elastic_module:float        
        ):
        self.__level = level
        self.__fck = fck
        self.__ftk = ftk
        self.__fc = fc
        self.__ft = ft
        self.__elastic_module = elastic_module
        
    @property
    def name(self):
        return f"C{self.__level}"    
    
    @property
    def fck(self):
        """混凝土轴心抗压强度标准值，MPa"""
        return self.__fck

    @property
    def ftk(self):
        """混凝土轴心抗拉强度标准值，MPa"""
        return self.__ftk
    
    @property
    def fc(self):
        """混凝土轴心抗压强度设计值，MPa"""
        return self.__fc
    
    @property
    def ft(self):
        """混凝土轴心抗拉强度设计值，MPa"""
        return self.__ft
    
    @property
    def elastic_module(self):
        """混凝土弹性模量，MPa"""
        return self.__elastic_module
    
fck = {
    15:10.0,
    20:13.4,
    25:16.7,
    30:20.1,
    35:23.4,
    40:26.8,
    45:29.6,
    50:32.4,
    55:35.5,
    60:38.5,
    65:41.5,
    70:44.5,
    75:47.4,
    80:50.2,
}
ftk = {
    15:1.27,
    20:1.54,
    25:1.78,
    30:2.01,
    35:2.2,
    40:2.39,
    45:2.51,
    50:2.64,
    55:2.74,
    60:2.85,
    65:2.93,
    70:2.99,
    75:3.05,
    80:3.11 ,
}
fc = {
    15:7.2,
    20:9.6,
    25:11.9,
    30:14.3,
    35:16.7,
    40:19.1,
    45:21.1,
    50:23.1,
    55:25.3,
    60:27.5,
    65:29.7,
    70:31.8,
    75:33.8,
    80:35.9,
}
ft = {
    15:0.91,
    20:1.1,
    25:1.27,
    30:1.43,
    35:1.57,
    40:1.71,
    45:1.8,
    50:1.89,
    55:1.96,
    60:2.04,
    65:2.09,
    70:2.14,
    75:2.18,
    80:2.22,
}
e = {
    15:22000,
    20:25500,
    25:28000,
    30:30000,
    35:31500,
    40:32500,
    45:33500,
    50:34500,
    55:35500,
    60:36000,
    65:36500,
    70:37000,
    75:37500,
    80:38000,
}

class Concrete:
    C15 = ConcreteLevel(15,fck[15],ftk[15],fc[15],ft[15],e[15])
    C20 = ConcreteLevel(20,fck[20],ftk[20],fc[20],ft[20],e[20])
    C25 = ConcreteLevel(25,fck[25],ftk[25],fc[25],ft[25],e[25])
    C30 = ConcreteLevel(30,fck[30],ftk[30],fc[30],ft[30],e[30])
    C35 = ConcreteLevel(35,fck[35],ftk[35],fc[35],ft[35],e[35])
    C40 = ConcreteLevel(40,fck[40],ftk[40],fc[40],ft[40],e[40])
    C45 = ConcreteLevel(45,fck[45],ftk[45],fc[45],ft[45],e[45])
    C50 = ConcreteLevel(50,fck[50],ftk[50],fc[50],ft[50],e[50])
    C55 = ConcreteLevel(55,fck[55],ftk[55],fc[55],ft[55],e[55])
    C60 = ConcreteLevel(60,fck[60],ftk[60],fc[60],ft[60],e[60])
    C65 = ConcreteLevel(65,fck[65],ftk[65],fc[65],ft[65],e[65])
    C70 = ConcreteLevel(70,fck[70],ftk[70],fc[70],ft[70],e[70])
    C75 = ConcreteLevel(75,fck[75],ftk[75],fc[75],ft[75],e[75])
    C80 = ConcreteLevel(80,fck[80],ftk[80],fc[80],ft[80],e[80])
    