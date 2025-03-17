from typing import List


class SingleMassResult:
    def __init__(
        self,
        floor_num: int,
        tower_num: int,
        dead_load: float,
        live_load: float,
        slab_area: float,
    ):
        self.floor_num = floor_num
        self.tower_num = tower_num
        self.dead_load = dead_load
        """单层恒载，单位kN，没有折减"""
        self.live_load = live_load
        """单层活载，单位kN，没有折减"""
        self.slab_area = slab_area
        """单层楼板面积，单位m2"""

    @property
    def total_load(self):
        """单层质量，恒+0.5活"""
        return self.dead_load + 0.5 * self.live_load


class MassResult:
    def __init__(self, mass_list: List[SingleMassResult]):
        self.mass_list = mass_list

    @property
    def total_slab_area(self):
        return sum([i.slab_area for i in self.mass_list])

    @property
    def total_dead_load(self):
        return sum([i.dead_load for i in self.mass_list])

    @property
    def total_live_load(self):
        return sum([i.live_load for i in self.mass_list])

    @property
    def total_load(self):
        return sum([i.total_load for i in self.mass_list])

    @classmethod
    def mock_data(cls):
        mass_list = []
        for i in range(5):
            mass_list.append(SingleMassResult(i + 1, 1, 5000, 2000, 350))

        return MassResult(mass_list)
