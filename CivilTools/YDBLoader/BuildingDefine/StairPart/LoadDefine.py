from enum import Enum


class LoadParams:
    def __init__(
        self,
        append_dead_load: float = 1,
        live_load: float = 3.5,
        dead_load_coef: float = 1.3,
        live_load_coef: float = 1.5,
        live_load_adjust_coef=1,
        live_load_permenent_coef=0.5,
    ):
        self.append_dead_load = append_dead_load
        self.live_load = live_load
        self.dead_load_coef = dead_load_coef
        self.live_load_coef = live_load_coef
        self.live_load_adjust_coef = live_load_adjust_coef
        self.live_load_permenent_coef = live_load_permenent_coef


class LoadType(Enum):
    Dead = 1
    Live = 2


class LoadCalulateType(Enum):
    qk = 1
    q = 2
    qe = 3


class StairLoad:
    def __init__(self, dead, live, load_params: LoadParams):
        self.dead = dead
        self.live = live
        self.load_params = load_params

    @property
    def qk(self):
        return self.dead + self.live

    @property
    def q(self):
        return (
            self.load_params.dead_load_coef * self.dead
            + self.load_params.live_load_coef * self.live
        )

    @property
    def qe(self):
        return self.dead + self.load_params.live_load_permenent_coef * self.live
