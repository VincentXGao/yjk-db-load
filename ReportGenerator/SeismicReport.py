from .BasicGenerator import BasicGenerator
from .DocParagraph import DocParagraph

class SeismicReport(BasicGenerator):
    def __init__(self):
        super().__init__()
        
    def creat_doc(self):
        self.add_big_title("抗震报告！")
        par = DocParagraph("Testsssssss")
        self.add_paragraph(par)
        self.add_blank_paragraph()
        self.add_page_break()
        self.add_paragraph(par)