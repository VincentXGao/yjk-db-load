import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from CivilTools.YDBLoader import YDBLoader
from CivilTools.YDBLoader.BuildingDefine import Beam
from CivilTools.YDBLoader.SQLiteConnector import Connector


class TestYDBLoader(unittest.TestCase):
    def test_connector_status(self):
        file_path = "testfiles/dtlmodel1.ydb"
        connector = Connector(file_path)
        connector.connect()
        connector.extract_table("tblJoint")
        connector.close()

    def test_connector_file_not_exist(self):
        file_path_not_exist = "not_existed_file_path"
        connector = Connector()
        with self.assertRaises(AttributeError) as context:
            connector.set_db_file(file_path_not_exist)
        self.assertEqual(str(context.exception),"The file_path is not existed, please check your file path. ")

    
    def test_extract_seismic_result(self):
        file_path = "testfiles/dsnModel_yxy.ydb"
        model = YDBLoader(file_path)
        model.get_seismic_result()
