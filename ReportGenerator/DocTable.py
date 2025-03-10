from typing import List

class DocTable:
    def init_content(self):
        self.context = []
        for i in range(self.row_num):
            self.context.append([])
            for _ in range(self.column_num):
                self.context[i].append("")
    
    def __init__(self,row_num, column_num):
        self.row_num = row_num
        self.column_num = column_num
        self.title = None
        self.no_grid = False
        self.all_bold = False
        self.init_content()
    
    def set_table_title(self, title):
        self.title = title    
        
        
    def set_table_context(self, context):
        if len(context) == self.row_num and len(context[0]) == self.column_num:
            self.context = context
        else:
            raise ValueError("输入的内容行列数量不对")

    def set_merge_lines(self, lines: List[int]):
        self.merge_lines = lines