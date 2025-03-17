from typing import List


class DocTable:
    def init_content(self):
        self.context = [["None"] * self.column_num for _ in range(self.row_num)]
        self.merged_cells = set()

    def __init__(self, row_num, column_num):
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

    def merge_cells(self, i, j, k, p):
        # 检查合并范围是否合法
        if i < 0 or i >= self.row_num or j < 0 or j >= self.column_num:
            raise ValueError("起始单元格超出表格范围")
        if k < 0 or k >= self.row_num or p < 0 or p >= self.column_num:
            raise ValueError("结束单元格超出表格范围")
        if i > k or (i == k and j > p):
            raise ValueError("起始单元格必须在结束单元格之前")

        # 检查是否与已合并的单元格冲突
        for start_row, start_col, end_row, end_col in self.merged_cells:
            if (i <= end_row and k > start_row) and (j <= end_col and p > start_col):
                raise ValueError("合并范围与已合并的单元格冲突")

        self.merged_cells.add((i, j, k, p))
