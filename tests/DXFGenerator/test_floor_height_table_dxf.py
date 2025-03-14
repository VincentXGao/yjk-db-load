import unittest
import sys
import os

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from CivilTools.YDBLoader import YDBLoader
from CivilTools.YDBLoader.BuildingDefine import Beam, Column, Section
from CivilTools.YDBLoader.BuildingDefine.Section import ShapeEnum
from CivilTools.ReportGenerator import SeismicReport, DocTable
from CivilTools.DXFGenerator import (
    BasicDXF,
    CADLayer,
    CADColor,
    CADLineType,
    FloorHeightTableDXF,
)


class TestFloorHeightTableDXFGenerator(unittest.TestCase):
    def test_floor_height_table_generator(self):
        floor_height_table = FloorHeightTableDXF(15)
        floor_height_table.set_table_title("XX项目8号楼层高表")
        floor_height_table.export_dxf("testfiles/floor_height.dxf")
