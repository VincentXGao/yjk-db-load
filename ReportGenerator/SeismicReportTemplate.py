from typing import List

class ChapterTemplate:
    def __init__(self, title,paragraph:List,table=None,picture=None,*args, **kwargs):
        self.title = title
        self.paragraph = paragraph
        self.table = table
        self.picture = picture

class SRTemplate:
    # 前情提要
    FIRST_INFO = lambda model_name : f"*{{本报告内容针对模型“{model_name}”，请注意核对模型名称！}}"
    # 小震章节提要
    SEISMIC_CHAPTER_TITLE = ChapterTemplate(
        title = lambda index : f"{index}.小震弹性分析的主要结果",
        paragraph= lambda index, yjk_version :[
            f"本模型弹性计算分析和构件设计软件采用YJK{yjk_version}，结构计算模型如图{index}.0.1所示，结构计算假定如下：",
            "1. *{XXXX作为上部结构的嵌固端；}",
            "2. 计算结构整体指标按刚性板假定，构件验算时按弹性板设计。",
            "*{(这里需要一张图片！)}"
        ],
        picture=lambda index : f"图{index}.0.1 YJK计算模型示意图"
    )
    # 嵌固层
    SEISMIC_EMBEDDING = ChapterTemplate(
        title = lambda index, sub_index : f"{index}.{sub_index} 嵌固层",
        paragraph= lambda index, sub_index  :[
            "采用《高层建筑混凝土结构技术规程》附录E剪切刚度的计算公式，"+
            "计算地下室顶板上下两层的侧向刚度比值。地下室范围的墙、柱构件取至塔楼外三个梁跨。"+
            f"计算结果见表{index}.{sub_index}.1，表明*{{地下室的刚度满足结构嵌固端的要求，"+
            "结构分析将嵌固端选取在地下室顶板是合理的。}",
        ],
        table=lambda index, sub_index  : f"表{index}.{sub_index}.1 嵌固层验算", 
    )