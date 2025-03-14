import unittest
import sys
import os

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from CivilTools.YDBLoader import YDBLoader
from CivilTools.YDBLoader.BuildingDefine import Beam, Column, Section
from CivilTools.YDBLoader.BuildingDefine.Section import ShapeEnum
from CivilTools.ReportGenerator import SeismicReport


class TestSeismicReport(unittest.TestCase):
    def test_generate_paper(self):
        report = SeismicReport()
        report.creat_doc()
        report.save("testfiles/MyReport.docx")
