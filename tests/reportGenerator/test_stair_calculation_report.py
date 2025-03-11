import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from CivilTools.YDBLoader import YDBLoader
from CivilTools.YDBLoader.BuildingDefine import Beam,Column, Section
from CivilTools.YDBLoader.BuildingDefine.Section import ShapeEnum
from CivilTools.ReportGenerator import StairCalculationReport,add_comma_in_num_str


class TestUtilFunctions(unittest.TestCase):
    def test_add_comma_for_int(self):
        creator = StairCalculationReport()
        creator.set_stair_data()
        creator.set_calculate_info()
        creator.create()
        creator.save_to_file("testfiles/stair_calculation_report.docx")







