from typing import List


class ChapterTemplate:
    def __init__(
        self,
        title,
        paragraph: List,
        table=None,
        picture=None,
        table_context=None,
        *args,
        **kwargs,
    ):
        self.title = title
        self.paragraph = paragraph
        self.table = table
        self.picture = picture
        self.table_context = table_context


class SRTemplate:
    # 前情提要
    FIRST_INFO = (
        lambda model_name: f"*{{本报告内容针对模型“{model_name}”，请注意核对模型名称！}}"
    )
    # 小震章节提要
    SEISMIC_CHAPTER_TITLE = ChapterTemplate(
        title=lambda index: f"{index}.小震弹性分析的主要结果",
        paragraph=lambda index, yjk_version: [
            f"本模型弹性计算分析和构件设计软件采用YJK{yjk_version}，结构计算模型如图{index}.0.1所示，结构计算假定如下：",
            "1. *{XXXX作为上部结构的嵌固端；}",
            "2. 计算结构整体指标按刚性板假定，构件验算时按弹性板设计。",
            "*{(这里需要一张图片！)}",
        ],
        picture=lambda index: f"图{index}.0.1 YJK计算模型示意图",
    )
    # 嵌固层
    SEISMIC_EMBEDDING = ChapterTemplate(
        title=lambda index, sub_index: f"{index}.{sub_index} 嵌固层",
        paragraph=lambda index, sub_index: [
            "采用《高层建筑混凝土结构技术规程》附录E剪切刚度的计算公式，"
            + "计算地下室顶板上下两层的侧向刚度比值。地下室范围的墙、柱构件取至塔楼外三个梁跨。"
            + f"计算结果见表{index}.{sub_index}.1，表明*{{地下室的刚度满足结构嵌固端的要求，"
            + "结构分析将嵌固端选取在地下室顶板是合理的。}",
        ],
        table=lambda index, sub_index: f"表{index}.{sub_index}.1 嵌固层验算",
        table_context=[
            [
                "-",
                "X向剪切刚度(kN/m)",
                "Y向剪切刚度(kN/m)",
                r"层高H_{i}(m)",
                "X向剪切刚度比",
                "Y向剪切刚度比",
                "结论",
            ],
            [
                "首层",
                "-",
                "-",
                "-",
                "-",
                "-",
                "-",
            ],
            [
                "地下一层",
                "-",
                "-",
                "-",
                "-",
                "-",
                "-",
            ],
        ],
    )

    # 结构质量
    PROJECT_MASS = ChapterTemplate(
        title=lambda index, sub_index: f"{index}.{sub_index} 结构质量",
        paragraph=lambda index, sub_index, **kwargs: [
            f"本塔楼结构重力荷载代表值为{kwargs["total_mass"]}吨，"
            + f"地上部分的结构楼板面积为{kwargs["total_area"]}平方米，"
            + f"按结构楼板折算的重量约为{kwargs["average_load"]:.2f}kN/m2。"
            + f"其中恒载及活载详情见表{index}.{sub_index}.1。",
        ],
        table=lambda index, sub_index: f"表{index}.{sub_index}.1 结构质量组成",
        table_context=lambda **kwargs: [
            [
                "类别",
                "数值(t)",
                "占比",
                "单位楼板面积重量\r（kN/m^{2})",
            ],
            [
                "恒载",
                "-",
                "-",
                "-",
            ],
            [
                "活载*0.5",
                "-",
                "-",
                "-",
            ],
            [
                "总质量(D+0.5L)",
                "-",
                "-",
                "-",
            ],
        ],
    )

    # 振型与周期
    PERIOD = ChapterTemplate(
        title=lambda index, sub_index: f"{index}.{sub_index} 振型与周期",
        paragraph=lambda index, sub_index, **kwargs: [
            f"表{index}.{sub_index}.1为强制刚性楼板假定下计算得到的结构模态信息，"
            + f"结构前三振型如图{index}.{sub_index}.1所示。",
            "从上表可以看出，X、Y方向平动的质量参与系数均大于90%，满足规范要求。",
        ],
        table=lambda index, sub_index: f"表{index}.{sub_index}.1 结构模态信息",
        table_context=lambda **kwargs: [
            [
                "振型号",
                "周期",
                "平动系数(X+Y)",
                "扭转系数",
                "X向平动质量参与系数(累计)",
                "Y向平动质量参与系数(累计)",
            ],
            [
                "1",
                "-",
                "-",
                "-",
                "-",
                "-",
            ],
            [
                "2",
                "-",
                "-",
                "-",
                "-",
                "-",
            ],
            [
                "3",
                "-",
                "-",
                "-",
                "-",
                "-",
            ],
            [
                "4",
                "-",
                "-",
                "-",
                "-",
                "-",
            ],
            [
                "5",
                "-",
                "-",
                "-",
                "-",
                "-",
            ],
            [
                "6",
                "-",
                "-",
                "-",
                "-",
                "-",
            ],
            [
                "7",
                "-",
                "-",
                "-",
                "-",
                "-",
            ],
            [
                "8",
                "-",
                "-",
                "-",
                "-",
                "-",
            ],
            [
                "9",
                "-",
                "-",
                "-",
                "-",
                "-",
            ],
        ],
    )

    # 楼层剪重比
    SHEAR_MASS_RATIO = ChapterTemplate(
        title=lambda index, sub_index: f"{index}.{sub_index} 楼层剪重比",
        paragraph=lambda index, sub_index, **kwargs: [
            f"本塔楼结构重力荷载代表值为{kwargs["total_mass"]}吨，"
            + f"地上部分的结构楼板面积为{kwargs["total_area"]}平方米，"
            + f"按结构楼板折算的重量约为{kwargs["average_load"]:.2f}kN/m2。"
            + f"其中恒载及活载详情见表{index}.{sub_index}.1。",
        ],
        table=lambda index, sub_index: f"表{index}.{sub_index}.1 结构质量组成",
        table_context=lambda **kwargs: [
            [
                "类别",
                "数值(t)",
                "占比",
                "单位楼板面积重量\r（kN/m^{2})",
            ],
            [
                "恒载",
                "-",
                "-",
                "-",
            ],
            [
                "活载*0.5",
                "-",
                "-",
                "-",
            ],
            [
                "总质量(D+0.5L)",
                "-",
                "-",
                "-",
            ],
        ],
    )

    # 楼层剪力及倾覆力矩
    SHEAR_AND_MOMENT = ChapterTemplate(
        title=lambda index, sub_index: f"{index}.{sub_index} 楼层剪力及倾覆力矩",
        paragraph=lambda index, sub_index, **kwargs: [
            f"本塔楼结构重力荷载代表值为{kwargs["total_mass"]}吨，"
            + f"地上部分的结构楼板面积为{kwargs["total_area"]}平方米，"
            + f"按结构楼板折算的重量约为{kwargs["average_load"]:.2f}kN/m2。"
            + f"其中恒载及活载详情见表{index}.{sub_index}.1。",
        ],
        table=lambda index, sub_index: f"表{index}.{sub_index}.1 结构质量组成",
        table_context=lambda **kwargs: [
            [
                "类别",
                "数值(t)",
                "占比",
                "单位楼板面积重量\r（kN/m^{2})",
            ],
            [
                "恒载",
                "-",
                "-",
                "-",
            ],
            [
                "活载*0.5",
                "-",
                "-",
                "-",
            ],
            [
                "总质量(D+0.5L)",
                "-",
                "-",
                "-",
            ],
        ],
    )

    # 框架倾覆力矩占比
    HORIZENTAL_MOMENT_RATIO_FOR_COLUMN = ChapterTemplate(
        title=lambda index, sub_index: f"{index}.{sub_index} 框架倾覆力矩占比",
        paragraph=lambda index, sub_index, **kwargs: [
            f"本塔楼结构重力荷载代表值为{kwargs["total_mass"]}吨，"
            + f"地上部分的结构楼板面积为{kwargs["total_area"]}平方米，"
            + f"按结构楼板折算的重量约为{kwargs["average_load"]:.2f}kN/m2。"
            + f"其中恒载及活载详情见表{index}.{sub_index}.1。",
        ],
        table=lambda index, sub_index: f"表{index}.{sub_index}.1 结构质量组成",
        table_context=lambda **kwargs: [
            [
                "类别",
                "数值(t)",
                "占比",
                "单位楼板面积重量\r（kN/m^{2})",
            ],
            [
                "恒载",
                "-",
                "-",
                "-",
            ],
            [
                "活载*0.5",
                "-",
                "-",
                "-",
            ],
            [
                "总质量(D+0.5L)",
                "-",
                "-",
                "-",
            ],
        ],
    )

    # 结构位移与层间位移
    DISP_AND_DRIFT = ChapterTemplate(
        title=lambda index, sub_index: f"{index}.{sub_index} 结构位移与层间位移",
        paragraph=lambda index, sub_index, **kwargs: [
            f"本塔楼结构重力荷载代表值为{kwargs["total_mass"]}吨，"
            + f"地上部分的结构楼板面积为{kwargs["total_area"]}平方米，"
            + f"按结构楼板折算的重量约为{kwargs["average_load"]:.2f}kN/m2。"
            + f"其中恒载及活载详情见表{index}.{sub_index}.1。",
        ],
        table=lambda index, sub_index: f"表{index}.{sub_index}.1 结构质量组成",
        table_context=lambda **kwargs: [
            [
                "类别",
                "数值(t)",
                "占比",
                "单位楼板面积重量\r（kN/m^{2})",
            ],
            [
                "恒载",
                "-",
                "-",
                "-",
            ],
            [
                "活载*0.5",
                "-",
                "-",
                "-",
            ],
            [
                "总质量(D+0.5L)",
                "-",
                "-",
                "-",
            ],
        ],
    )

    # 侧向刚度比
    HORIZENTAL_STIFFNESS_RATIO = ChapterTemplate(
        title=lambda index, sub_index: f"{index}.{sub_index} 侧向刚度比",
        paragraph=lambda index, sub_index, **kwargs: [
            f"本塔楼结构重力荷载代表值为{kwargs["total_mass"]}吨，"
            + f"地上部分的结构楼板面积为{kwargs["total_area"]}平方米，"
            + f"按结构楼板折算的重量约为{kwargs["average_load"]:.2f}kN/m2。"
            + f"其中恒载及活载详情见表{index}.{sub_index}.1。",
        ],
        table=lambda index, sub_index: f"表{index}.{sub_index}.1 结构质量组成",
        table_context=lambda **kwargs: [
            [
                "类别",
                "数值(t)",
                "占比",
                "单位楼板面积重量\r（kN/m^{2})",
            ],
            [
                "恒载",
                "-",
                "-",
                "-",
            ],
            [
                "活载*0.5",
                "-",
                "-",
                "-",
            ],
            [
                "总质量(D+0.5L)",
                "-",
                "-",
                "-",
            ],
        ],
    )

    # 扭转位移比
    ROTATION_RATIO = ChapterTemplate(
        title=lambda index, sub_index: f"{index}.{sub_index} 扭转位移比",
        paragraph=lambda index, sub_index, **kwargs: [
            f"本塔楼结构重力荷载代表值为{kwargs["total_mass"]}吨，"
            + f"地上部分的结构楼板面积为{kwargs["total_area"]}平方米，"
            + f"按结构楼板折算的重量约为{kwargs["average_load"]:.2f}kN/m2。"
            + f"其中恒载及活载详情见表{index}.{sub_index}.1。",
        ],
        table=lambda index, sub_index: f"表{index}.{sub_index}.1 结构质量组成",
        table_context=lambda **kwargs: [
            [
                "类别",
                "数值(t)",
                "占比",
                "单位楼板面积重量\r（kN/m^{2})",
            ],
            [
                "恒载",
                "-",
                "-",
                "-",
            ],
            [
                "活载*0.5",
                "-",
                "-",
                "-",
            ],
            [
                "总质量(D+0.5L)",
                "-",
                "-",
                "-",
            ],
        ],
    )
    # 刚重比
    STIFFNESS_MASS_RATIO = ChapterTemplate(
        title=lambda index, sub_index: f"{index}.{sub_index} 刚重比",
        paragraph=lambda index, sub_index, **kwargs: [
            f"本塔楼结构重力荷载代表值为{kwargs["total_mass"]}吨，"
            + f"地上部分的结构楼板面积为{kwargs["total_area"]}平方米，"
            + f"按结构楼板折算的重量约为{kwargs["average_load"]:.2f}kN/m2。"
            + f"其中恒载及活载详情见表{index}.{sub_index}.1。",
        ],
        table=lambda index, sub_index: f"表{index}.{sub_index}.1 结构质量组成",
        table_context=lambda **kwargs: [
            [
                "类别",
                "数值(t)",
                "占比",
                "单位楼板面积重量\r（kN/m^{2})",
            ],
            [
                "恒载",
                "-",
                "-",
                "-",
            ],
            [
                "活载*0.5",
                "-",
                "-",
                "-",
            ],
            [
                "总质量(D+0.5L)",
                "-",
                "-",
                "-",
            ],
        ],
    )
    # 楼层侧向受剪承载力比
    SHEAR_CAPACITY_RATIO = ChapterTemplate(
        title=lambda index, sub_index: f"{index}.{sub_index} 楼层侧向受剪承载力比",
        paragraph=lambda index, sub_index, **kwargs: [
            f"本塔楼结构重力荷载代表值为{kwargs["total_mass"]}吨，"
            + f"地上部分的结构楼板面积为{kwargs["total_area"]}平方米，"
            + f"按结构楼板折算的重量约为{kwargs["average_load"]:.2f}kN/m2。"
            + f"其中恒载及活载详情见表{index}.{sub_index}.1。",
        ],
        table=lambda index, sub_index: f"表{index}.{sub_index}.1 结构质量组成",
        table_context=lambda **kwargs: [
            [
                "类别",
                "数值(t)",
                "占比",
                "单位楼板面积重量\r（kN/m^{2})",
            ],
            [
                "恒载",
                "-",
                "-",
                "-",
            ],
            [
                "活载*0.5",
                "-",
                "-",
                "-",
            ],
            [
                "总质量(D+0.5L)",
                "-",
                "-",
                "-",
            ],
        ],
    )
    # 风荷载下的结构舒适度验算
    WIND_ACC = ChapterTemplate(
        title=lambda index, sub_index: f"{index}.{sub_index} 风荷载下的结构舒适度验算",
        paragraph=lambda index, sub_index, **kwargs: [
            f"本塔楼结构重力荷载代表值为{kwargs["total_mass"]}吨，"
            + f"地上部分的结构楼板面积为{kwargs["total_area"]}平方米，"
            + f"按结构楼板折算的重量约为{kwargs["average_load"]:.2f}kN/m2。"
            + f"其中恒载及活载详情见表{index}.{sub_index}.1。",
        ],
        table=lambda index, sub_index: f"表{index}.{sub_index}.1 结构质量组成",
        table_context=lambda **kwargs: [
            [
                "类别",
                "数值(t)",
                "占比",
                "单位楼板面积重量\r（kN/m^{2})",
            ],
            [
                "恒载",
                "-",
                "-",
                "-",
            ],
            [
                "活载*0.5",
                "-",
                "-",
                "-",
            ],
            [
                "总质量(D+0.5L)",
                "-",
                "-",
                "-",
            ],
        ],
    )
