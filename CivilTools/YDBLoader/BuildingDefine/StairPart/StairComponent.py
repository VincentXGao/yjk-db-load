import math
import numpy as np


class Component:

    def init_attr(self):
        self.E = 30000
        self.B = 1000
        self.H = 150
        self.vertical_q = 10
        self.length = math.sqrt(
            (self.end_point[1] - self.start_point[1]) ** 2
            + (self.end_point[0] - self.start_point[0]) ** 2
        )
        if self.start_point[0] == self.end_point[0]:
            self.alpha = 0
        else:
            self.alpha = math.atan(
                (self.end_point[1] - self.start_point[1])
                / (self.end_point[0] - self.start_point[0])
            )

    def __init__(self, p1, p2) -> None:
        self.start_point = p1
        self.end_point = p2
        self.section_kind = "Rectangle"
        self.init_attr()

    def set_comp_attr(self, e, b, h):
        self.E = e
        self.B = b
        self.H = h

    def set_vertical_q(self, q):
        self.vertical_q = q

    def create_k(self):
        self.calculate_section_attr()
        K = np.zeros((6, 6))

        l = self.length
        i = self.E * self.I / l
        B = self.E * self.area / l
        c_x = math.cos(self.alpha)
        c_y = math.sin(self.alpha)
        a1 = B * c_x * c_x + 12 * i / l / l * c_y * c_y
        a2 = (B - 12 * i / l / l) * c_x * c_y
        a3 = B * c_y * c_y + 12 * i / l / l * c_x * c_x
        a4 = -6 * i / l * c_y
        a5 = 6 * i / l * c_x
        a6 = 4 * i
        K[0, 0] = K[3, 3] = a1
        K[0, 3] = K[3, 0] = -a1
        K[1, 0] = K[4, 3] = K[0, 1] = K[3, 4] = a2
        K[1, 3] = K[0, 4] = K[3, 1] = K[4, 0] = -a2
        K[1, 1] = K[4, 4] = a3
        K[1, 4] = K[4, 1] = -a3
        K[0, 2] = K[0, 5] = K[2, 0] = K[5, 0] = a4
        K[2, 3] = K[3, 5] = K[3, 2] = K[5, 3] = -a4
        K[1, 2] = K[1, 5] = K[2, 1] = K[5, 1] = a5
        K[2, 4] = K[4, 5] = K[4, 2] = K[5, 4] = -a5
        K[2, 2] = K[5, 5] = a6
        K[2, 5] = K[5, 2] = a6 / 2
        return K

    def create_f(self):
        F = np.zeros((6, 1))
        # 这里只针对竖向荷载
        length = abs(self.end_point[0] - self.start_point[0])

        F[1, 0] = -self.vertical_q * length / 2
        F[2, 0] = -self.vertical_q * length**2 / 12
        F[4, 0] = -self.vertical_q * length / 2
        F[5, 0] = self.vertical_q * length**2 / 12
        return F

    def calculate_section_attr(self):
        if self.section_kind == "Rectangle":
            self.I = self.B * self.H**3 / 12
            self.area = self.B * self.H

    def set_f(self, f_1_x, f_1_y, f_2_x, f_2_y):
        self.f_1_x = f_1_x / 1e3
        self.f_1_y = f_1_y / 1e3
        self.f_2_x = f_2_x / 1e3
        self.f_2_y = f_2_y / 1e3

    def set_m(self, m_1, m_2):
        self.m_1 = m_1 / 1e6
        self.m_2 = m_2 / 1e6

    def set_u(self, u1x, u1y, u1r, u2x, u2y, u2r):
        self.u_1_x = u1x
        self.u_1_y = u1y
        self.u_1_r = u1r
        self.u_2_x = u2x
        self.u_2_y = u2y
        self.u_2_r = u2r

    @property
    def v1(self):
        return self.f_1_y * np.cos(self.alpha) - self.f_1_x * np.sin(self.alpha)

    @property
    def v2(self):
        return -self.f_2_y * np.cos(self.alpha) + self.f_2_x * np.sin(self.alpha)
