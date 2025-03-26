class SteelLevel:
    def __init__(
        self,
        name: str,
        fy: float,
        elastic_module: float,
    ):
        self.name = name
        self.fy = fy
        self.elastic_module = elastic_module


class Steel:
    HRB300 = SteelLevel("HRB300", 270, 2100000)
    HRB355 = SteelLevel("HRB355", 300, 2000000)
    HRB400 = SteelLevel("HRB400", 360, 2000000)
    HRB500 = SteelLevel("HRB500", 435, 2000000)
    Q235 = SteelLevel("Q235", 111, 2000000)
    Q345 = SteelLevel("Q345", 111, 2000000)
    Q355 = SteelLevel("Q355", 111, 2000000)
    Q420 = SteelLevel("Q420", 111, 2000000)
