import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from YDBLoader import YDBLoader
from YDBLoader.BuildingDefine import Beam,Column, Section
from YDBLoader.BuildingDefine.Section import ShapeEnum

class TestColumn(unittest.TestCase):
    def test_section_init(self):
        for shape in ShapeEnum:
            Section(1,(ShapeEnum)(shape.value),[111,222])
        with self.assertRaises(ValueError) as context:
            Section(1,(ShapeEnum)(999),[111,222])
        self.assertIn("not a valid ShapeEnum" , str(context.exception))
        
    def test_section_str(self):
        for shape in ShapeEnum:
            s = Section(1,(ShapeEnum)(shape.value),[111,222])
            print(s)
