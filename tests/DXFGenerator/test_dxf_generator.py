import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from CivilTools.YDBLoader import YDBLoader
from CivilTools.YDBLoader.BuildingDefine import Beam,Column, Section
from CivilTools.YDBLoader.BuildingDefine.Section import ShapeEnum
from CivilTools.ReportGenerator import SeismicReport, DocTable
from CivilTools.DXFGenerator import BasicDXF,CADLayer,CADColor,CADLineType
from CivilTools.DXFGenerator.DrawingAttribs import DrawingAttribs

class TestDXFGenerator(unittest.TestCase):
    def test_dxf_generator(self):
        basic = BasicDXF()
        layer_list = [
            CADLayer("AA",CADColor.Green,CADLineType.DASHED),
            CADLayer("BB",CADColor.Yellow,CADLineType.DASHED),
            CADLayer("CC",CADColor.Red,CADLineType.DASHDOT)
            ]
        basic.init_layers(layer_list)
        basic.creat_test()
        basic._add_dimension([500,500],[-500,500],DrawingAttribs("AA"))
        basic._save("testfiles/test_dxf.dxf")