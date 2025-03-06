import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.YDBLoader import YDBLoader
from src.YDBLoader.BuildingDefine.Beam import Beam


class TestYDBLoader(unittest.TestCase):
    def test_connector_status(self):
        loader = YDBLoader()
        result = loader.sum(2, 3)
        assert result == 5

    def test_add_2(self):
        loader = YDBLoader()
        result = loader.get_beams()
        assert isinstance(result, Beam)

    def test_add3(self):
        loader = YDBLoader()
        result = loader.sum(2, 3)
        assert result == 5