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


class TestDocTable(unittest.TestCase):
    def test_table_merge(self):
        row = 9
        column = 10
        table = DocTable(row, column)

        table.merge_cells(0, 0, 2, 2)
        with self.assertRaises(ValueError) as context:
            table.merge_cells(1, 1, 1, 8)
        self.assertIn("合并范围与已合并的单元格冲突", str(context.exception))

        with self.assertRaises(ValueError) as context:
            table.merge_cells(2, 2, 2, 8)
        self.assertIn("合并范围与已合并的单元格冲突", str(context.exception))

        table = DocTable(row, column)
        with self.assertRaises(ValueError) as context:
            table.merge_cells(1, 1, 9, 8)
        self.assertIn("结束单元格超出表格范围", str(context.exception))

        with self.assertRaises(ValueError) as context:
            table.merge_cells(-1, 1, 9, 8)
        self.assertIn("起始单元格超出表格范围", str(context.exception))
