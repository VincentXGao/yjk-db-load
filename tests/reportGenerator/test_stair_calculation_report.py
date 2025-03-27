import unittest
import sys
import os

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from CivilTools.YDBLoader import YDBLoader
from CivilTools.YDBLoader.BuildingDefine import Beam, Column, Section
from CivilTools.YDBLoader.BuildingDefine.StairPart import Position, StairPart
from CivilTools.YDBLoader.BuildingDefine.Section import ShapeEnum
from CivilTools.ReportGenerator import StairCalculationReport, add_comma_in_num_str
from CivilTools.FigureGenerator import StairCalculationSheetPNGPlotter


class TestUtilFunctions(unittest.TestCase):
    def test_add_comma_for_int(self):
        creator = StairCalculationReport()

        position1 = Position(0, 2180, 0, 1910, 5030, 6850)
        sp1 = StairPart(position1, 13)
        sp1.left_thick = sp1.main_thick = sp1.right_thick = 130
        position2 = Position(0, 2180, 0, 1910, 5030, 6850)
        sp2 = StairPart(position2, 13)
        sp2.set_beam_offset(1, 500)
        position3 = Position(0, 2180, 0, 1910, 5030, 6850)
        sp3 = StairPart(position3, 13)
        sp3.set_beam_offset(2, 500)
        position4 = Position(0, 2180, 0, 1910, 5030, 6850)
        sp4 = StairPart(position4, 13)
        sp4.set_beam_offset(1, 500)
        sp4.set_beam_offset(2, 500)

        # creator.set_stair_data([sp1, sp2])
        # creator.set_calculate_info()
        # creator.create()
        # creator.save_to_file("testfiles/stair_calculation_report.docx")

    def test_stair_figure_plot(self):
        position1 = Position(0, 2180, 0, 1910, 5030, 6850)
        sp1 = StairPart(position1, 13)
        sp1.left_thick = sp1.main_thick = sp1.right_thick = 130
        position2 = Position(0, 2180, 0, 1910, 5030, 6850)
        sp2 = StairPart(position2, 13)
        sp2.set_beam_offset(1, 500)
        position3 = Position(0, 2180, 0, 1910, 5030, 6850)
        sp3 = StairPart(position3, 13)
        sp3.set_beam_offset(2, 500)
        position4 = Position(0, 2180, 0, 1910, 5030, 6850)
        sp4 = StairPart(position4, 13)
        sp4.set_beam_offset(1, 500)
        sp4.set_beam_offset(2, 500)
        i = 1
        for sp in [sp1, sp2, sp3, sp4]:
            plotter = StairCalculationSheetPNGPlotter(sp)
            plotter.plot_moment([0, -200, 500, -200, 0])
            plotter.save(f"testfiles/stair_plot/test_shear_{i}.png")
            i += 1
