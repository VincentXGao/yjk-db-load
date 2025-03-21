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


class TestMass(unittest.TestCase):
    def test_mass_extract(self):
        file_path = "testfiles/dsnModel_yxy.ydb"
        model = YDBLoader(file_path, YDBType.ResultYDB)
        period = model.get_mass_result()
