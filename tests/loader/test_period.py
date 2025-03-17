import unittest
import sys
import os

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from CivilTools.YDBLoader import YDBLoader, YDBType
from CivilTools.YDBLoader.BuildingDefine import Beam, Column, Section
from CivilTools.YDBLoader.SQLiteConnector import Connector
from CivilTools.YDBLoader.BuildingDefine.Section import ShapeEnum


class TestPeriod(unittest.TestCase):
    def test_period_extract(self):
        file_path = "testfiles/dsnModel_yxy.ydb"
        model = YDBLoader(file_path, YDBType.ResultYDB)
        period = model.get_period_result()
        assert len(period.periods) != 0
        self.assertAlmostEqual(period.periods[0].time, 0.6056121912)

    def test_period_extract_for_non_result_ydb(self):
        file_path = "testfiles/dtlmodel_yxy.ydb"
        model = YDBLoader(file_path)
        with self.assertRaises(TypeError) as context:
            model.get_period_result()
        self.assertIn("This model is not ResultYDB file", str(context.exception))
