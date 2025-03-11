import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from YDBLoader import YDBLoader
from YDBLoader.BuildingDefine import Beam,Column, Section
from YDBLoader.BuildingDefine.Section import ShapeEnum
from ReportGenerator import SeismicReport,add_comma_in_num_str


class TestUtilFunctions(unittest.TestCase):
    def test_add_comma_for_int(self):
        self.assertEqual(add_comma_in_num_str(888),"888")
        self.assertEqual(add_comma_in_num_str(546871),"546,871")
        self.assertEqual(add_comma_in_num_str(1546871),"1,546,871")
        self.assertEqual(add_comma_in_num_str(-1546871),"-1,546,871")
        self.assertEqual(add_comma_in_num_str(-546871),"-546,871")
        with self.assertRaises(ValueError) as context:
            add_comma_in_num_str(-546871.58)
        self.assertIn("Only int number can be added." , str(context.exception))
        
        with self.assertRaises(ValueError) as context:
            add_comma_in_num_str("Asfsaf")
        self.assertIn("Only int number can be added." , str(context.exception))

