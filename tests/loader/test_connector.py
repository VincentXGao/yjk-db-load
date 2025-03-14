import unittest
import sys
import os

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from CivilTools.YDBLoader import YDBLoader
from CivilTools.YDBLoader.BuildingDefine import Beam, Column, Section
from CivilTools.YDBLoader.SQLiteConnector import Connector
from CivilTools.YDBLoader.BuildingDefine.Section import ShapeEnum
from CivilTools.YDBLoader.BuildingDefine.Geometry import Joint


class TestConnector(unittest.TestCase):
    def test_is_table_in_db(self):
        file_path = "testfiles/dtlmodel1.ydb"
        existed_table_name = "tblJoint"
        not_existed_table_name = "sdf"
        connector = Connector(file_path)
        result1 = connector.is_table_in_db(existed_table_name)
        self.assertTrue(result1)
        result2 = connector.is_table_in_db(not_existed_table_name)
        self.assertFalse(result2)
