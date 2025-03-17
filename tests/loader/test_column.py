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


class TestColumn(unittest.TestCase):
    def test_column_init(self):
        sect = Section(1, ShapeEnum.Rect, [111, 222])
        c = Column(1, Joint(1, 1, 1, 1), sect)
        # assert str(c.section) == "adsf"
        # assert c == "s"
