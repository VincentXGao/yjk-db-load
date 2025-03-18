from typing import List
from ..YDBLoader.BuildingDefine import Period


X_DIRECTION = "X向"
Y_DIRECTION = "Y向"


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


def period_para_analysis(period_result: Period, chapter_index: int, sub_index: int):
    first_para = __period_first_para(period_result, chapter_index, sub_index)
    second_para = __period_second_para(period_result)
    return [first_para, second_para]


def __period_first_para(period_result: Period, chapter_index: int, sub_index: int):
    type_1 = period_result.periods[0].direction
    type_2 = period_result.periods[1].direction
    type_3 = period_result.periods[2].direction
    first_para = (
        f"表{chapter_index}.{sub_index}.1为强制刚性楼板假定下计算得到的结构模态信息，"
    )
    if type_1.upper() == "X" and type_2.upper() == "Y" and type_3.upper() == "Z":
        z_x = period_result.periods[2].time / period_result.periods[0].time
        z_y = period_result.periods[2].time / period_result.periods[1].time
        first_para += (
            "前两阶振型分别为X、Y向平动振型，第三阶振型为Z向扭转振型；"
            + f"结构第一扭转周期与第一、第二平动周期的比值分别为{z_x:.2f}和{z_y:.2f}。"
        )
    elif type_1.upper() == "Y" and type_2.upper() == "X" and type_3.upper() == "Z":
        z_y = period_result.periods[2].time / period_result.periods[0].time
        z_x = period_result.periods[2].time / period_result.periods[1].time
        first_para += (
            "前两阶振型分别为Y、X向平动振型，第三阶振型为Z向扭转振型；"
            + f"结构第一扭转周期与第一、第二平动周期的比值分别为{z_y:.2f}和{z_x:.2f}。"
        )
    elif type_1.upper() == "X" and type_2.upper() == "Z" and type_3.upper() == "Y":
        z_x = period_result.periods[1].time / period_result.periods[0].time
        first_para += (
            "第一阶振型为X向平动，第二阶振型为Z向扭转，第三阶振型为Y向平动；"
            + f"结构第一扭转周期与第一平动周期的比值分别为{z_x:.2f}。"
        )
    elif type_1.upper() == "Y" and type_2.upper() == "Z" and type_3.upper() == "X":
        z_y = period_result.periods[1].time / period_result.periods[0].time
        first_para += (
            "第一阶振型为Y向平动，第二阶振型为Z向扭转，第三振阶型为X向平动；"
            + f"结构第一扭转周期与第一平动周期的比值分别为{z_y:.2f}。"
        )
    elif type_1.upper() == "Z" and type_2.upper() == "X" and type_3.upper() == "Y":
        first_para += "*{第一阶振型为Z向扭转，第二、三阶振型分别为X、Y向平动，请注意复核计算结果；}"
    else:
        first_para += "*{第一阶振型为Z向扭转，第二、三阶振型分别为Y、X向平动，请注意复核计算结果；}"
    first_para += f"结构前三振型如图{chapter_index}.{sub_index}.1所示。"
    return first_para


def __period_second_para(period_result: Period):
    total_participate_x = sum([p.mass_participate_x for p in period_result.periods])
    total_participate_y = sum([p.mass_participate_y for p in period_result.periods])
    if total_participate_x >= 0.9 and total_participate_y >= 0.9:
        second_para = (
            "从上表可以看出，X、Y方向平动的质量参与系数均大于90%，满足规范要求。"
        )
    elif total_participate_x >= 0.9:
        second_para = "从上表可以看出，X方向平动的质量参与系数大于90%，*{但Y方向不满足，可酌情增加计算振型数量。}"
    elif total_participate_y >= 0.9:
        second_para = "从上表可以看出，Y方向平动的质量参与系数大于90%，*{但X方向不满足，可酌情增加计算振型数量。}"
    else:
        second_para = "从上表可以看出，*{X、Y方向平动的质量参与系数均小于90%，可酌情增加计算振型数量。}"
    return second_para


def shear_mass_ratio(chapter_index: int, sub_index: int):
    # todo: 这里需要根据设防烈度及基底剪力结果进行判断
    para_context = "剪重比为结构设计的重要指标，按规范7度，0.10g的反应谱计算，"
    para_context += f"结构基底和各楼层剪重比计算具体结果分别见表{chapter_index}.{sub_index}.1和图{chapter_index}.{sub_index}.1。"
    para_context += (
        "计算结果显示，结构两个主向的基底剪力均满足规范1.60%的最小剪重比要求。"
    )

    return para_context


def shear_and_moment(chapter_index: int, sub_index: int):
    para = f"塔楼基底剪力和基底倾覆力矩见下表{chapter_index}.{sub_index}.1。"
    para += f"图{chapter_index}.{sub_index}.1为50年重现期下的风荷载和小震作用下的楼层剪力分布，"
    para += f"图{chapter_index}.{sub_index}.2为50年重现期下的风荷载和小震作用下的倾覆弯矩分布。"
    para += "计算结果显示，"
    para += "在X、Y两个方向，小震作用下的楼层剪力和倾覆弯矩均远大于50年重现期下的风荷载作用，"
    para += "也表明在结构刚度和变形方面，小震起控制作用。"

    return para


def horizental_moment_ratio_for_column(chapter_index: int, sub_index: int):
    para1 = f"图{chapter_index}.{sub_index}.1为结构在双向水平地震作用下，各层框架柱分担的倾覆力矩与各层结构总倾覆力矩的比值（倾覆力矩分担比），"
    para1 += f"表{chapter_index}.{sub_index}.1与表{chapter_index}.{sub_index}.2为结构分别在双向水平地震作用下，各层框架柱分担的剪力、倾覆力矩及其所占比例的具体数值。"

    para2 = "结果表明：在规定水平力下，结构底层框架部分承受的地震倾覆力矩分担比"
    para2 += "在X向和Y向分别为54.8%和48.0%。底层倾覆力矩分担比大于50%，"
    para2 += "按照《高规》第8.1.3条第3款之规定，本工程应按照框架-剪力墙结构进行设计，"
    para2 += "其最大适用高度可比框架结构适当增加，框架部分的抗震等级和轴压比限值宜按框架结构的规定采用。"

    return [para1, para2]


def disp_and_drift(chapter_index: int, sub_index: int):
    para = f"结构在小震与风荷载作用下的最大层间位移角如表{chapter_index}.{sub_index}.1和图{chapter_index}.{sub_index}.1所示。"
    para += "各工况下各楼层位移角均小于规范限值1/800的要求。"
    para += "此外，风荷载下各层层间位移角小于小震作用，小震起控制作用。"

    return para


class SRTemplate:
    # 前情提要
    FIRST_INFO = (
        lambda model_name: f"*{{本报告内容针对模型“{model_name}”，请注意核对模型名称！}}"
    )
    # 小震章节提要
    SEISMIC_CHAPTER_TITLE = ChapterTemplate(
        title=lambda index: f"{index}.小震弹性分析的主要结果",
        paragraph=lambda index, yjk_version: [
            f"本模型弹性计算分析和构件设计软件采用YJK-{yjk_version}，结构计算模型如图{index}.0.1所示，结构计算假定如下：",
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
            + f"按结构楼板折算的重量约为{kwargs["average_load"]}kN/m^{{2}}。"
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
                f"{kwargs['dead_mass']}",
                f"{kwargs['dead_percentage']}",
                f"{kwargs['dead_average']}",
            ],
            [
                "活载*0.5",
                f"{kwargs['live_mass']}",
                f"{kwargs['live_percentage']}",
                f"{kwargs['live_average']}",
            ],
            [
                "总质量(D+0.5L)",
                f"{kwargs['total_mass']}",
                f"{kwargs['total_percentage']}",
                f"{kwargs['total_average']}",
            ],
        ],
    )

    # 振型与周期
    PERIOD = ChapterTemplate(
        title=lambda index, sub_index: f"{index}.{sub_index} 振型与周期",
        paragraph=period_para_analysis,
        table=lambda index, sub_index: f"表{index}.{sub_index}.1 结构模态信息",
        table_context=[
            [
                "振型号",
                "周期",
                "平动系数(X+Y)",
                "扭转系数",
                "X向平动质量参与系数(累计%)",
                "Y向平动质量参与系数(累计%)",
            ],
        ],
        picture=lambda index, sub_index: f"图{index}.{sub_index}.1 结构前三振型示意图",
    )

    # 楼层剪重比
    SHEAR_MASS_RATIO = ChapterTemplate(
        title=lambda index, sub_index: f"{index}.{sub_index} 楼层剪重比",
        paragraph=shear_mass_ratio,
        table=lambda index, sub_index: f"表{index}.{sub_index}.1 结构基底剪重比",
        table_context=lambda **kwargs: [
            [
                "方向",
                "基底剪力(kN)",
                "重力荷载代表值(kN)",
                "剪重比",
            ],
            [
                X_DIRECTION,
                "-",
                "-",
                "-",
            ],
            [
                Y_DIRECTION,
                "-",
                "-",
                "-",
            ],
        ],
        picture=lambda index, sub_index: f"图{index}.{sub_index}.1 地震作用下各楼层剪重比",
    )

    # 楼层剪力及倾覆力矩
    SHEAR_AND_MOMENT = ChapterTemplate(
        title=lambda index, sub_index: f"{index}.{sub_index} 楼层剪力及倾覆力矩",
        paragraph=shear_and_moment,
        table=lambda index, sub_index: f"表{index}.{sub_index}.1 结构基底总剪力和倾覆力矩",
        table_context=lambda **kwargs: [
            [
                "--",
                "--",
                "YJK",
                "YJK",
            ],
            [
                "--",
                "项目",
                X_DIRECTION,
                Y_DIRECTION,
            ],
            [
                "风荷载",
                "基底剪力(kN)",
                "-",
                "-",
            ],
            [
                "风荷载",
                "基地倾覆力矩(MN·m)",
                "-",
                "-",
            ],
            [
                "多遇地震",
                "基底剪力(kN)",
                "-",
                "-",
            ],
            [
                "多遇地震",
                "基地倾覆力矩(MN·m)",
                "-",
                "-",
            ],
        ],
        picture=lambda index, sub_index: [
            f"图{index}.{sub_index}.1 风荷载和小震作用下的楼层剪力",
            f"图{index}.{sub_index}.2 风荷载和小震作用下的楼层倾覆力矩",
        ],
    )

    # 框架倾覆力矩占比
    HORIZENTAL_MOMENT_RATIO_FOR_COLUMN = ChapterTemplate(
        title=lambda index, sub_index: f"{index}.{sub_index} 框架倾覆力矩占比",
        paragraph=horizental_moment_ratio_for_column,
        table=lambda index, sub_index: [
            f"表{index}.{sub_index}.1 外框柱剪力及倾覆力矩分担比（X向）",
            f"表{index}.{sub_index}.2 外框柱剪力及倾覆力矩分担比（Y向）",
        ],
        table_context=lambda **kwargs: [
            [
                "层号",
                "剪力(kN)",
                "剪力分担比",
                "弯矩(kN*m)",
                "弯矩分担比",
            ],
        ],
        picture=lambda index, sub_index: f"图{index}.{sub_index}.1 各楼层的框架剪力和弯矩分比",
    )

    # 结构位移与层间位移
    DISP_AND_DRIFT = ChapterTemplate(
        title=lambda index, sub_index: f"{index}.{sub_index} 结构位移与层间位移",
        paragraph=disp_and_drift,
        table=lambda index, sub_index: f"表{index}.{sub_index}.1 楼层最大层间位移角",
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
        picture=lambda index, sub_index: f"图{index}.{sub_index}.1 结构楼层层间位移角",
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
