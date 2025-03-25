from enum import Enum

ID = "ID"
STD_FLR_ID = "StdFlrID"
JOINT_ID = "JtID"
JOINT_ID_1 = "Jt1ID"
JOINT_ID_2 = "Jt2ID"
GRID_ID = "GridID"
SECTION_ID = "SectID"
ECC = "Ecc"
ECC_X = "EccX"
ECC_Y = "EccY"
ROTATION = "Rotation"


FLOOR_NUM = "FlrNo"
TOWER_NUM = "TowNo"
LOAD_CASE_ID = "LDCase"


class YDBTableName:
    JOINT_TABLE_NAME = "tblJoint"
    JOINT_TABLE_USEFUL_COLUMNS = [ID, "X", "Y", STD_FLR_ID]

    GRID_TABLE_NAME = "tblGrid"
    GRID_TABLE_USEFUL_COLUMNS = [ID, JOINT_ID_1, JOINT_ID_2]
    """ 
    0-ID , 
    1-Joint1_ID , 
    2-Joint2_ID ,
    """

    COLUMN_SECTION_TABLE_NAME = "tblColSect"
    BEAM_SECTION_TABLE_NAME = "tblBeamSect"
    SECTION_TABLE_USEFUL_COLUMNS = [ID, "Mat", "Kind", "ShapeVal"]

    COLUMN_TABLE_NAME = "tblColSeg"
    COLUMN_TABLE_USEFUL_COLUMNS = [ID, JOINT_ID, SECTION_ID, ECC_X, ECC_Y, ROTATION]
    """ 
    0-ID , 
    1-Joint_ID , 
    2-Section_ID ,
    3-EccX ,
    4-EccY ,
    5-Rotation
    """

    BEAM_TABLE_NAME = "tblBeamSeg"
    BEAM_TABLE_USEFUL_COLUMNS = [ID, GRID_ID, SECTION_ID, ECC, "HDiff1", "HDiff2"]
    """ 
    0-ID , 
    1-Grid_ID , 
    2-Section_ID ,
    3-Ecc ,
    4-HDiff1 ,
    5-HDiff2
    """

    RESULT_PERIOD_TABLE = "calEigenInf"
    RESULT_PERIOD_USEFUL_COLUMNS = [
        "ModuleID",
        "EigenNo",
        "Period",
        "Angle",
        "CoeffInf",
        "mInf",
    ]
    """
    0-moduleID
    1-EigenNo 
    2-Period Time
    3-Angle
    4-CoeffInf [unknown, xpart_ratio, ypart_ratio, zpart_ratio,
    the sum of then should be 1]
    5-MassInfo [unknown, xmass_participate, ymass_par, zmass_par,
    the sum of all xmass_par should larger than 0.9]
    """

    RESULT_MASS_TABLE = "preFlrTowProp"
    RESULT_MASS_USEFUL_COLUMNS = [FLOOR_NUM, TOWER_NUM, "MassInf"]
    """ 
    0-floor_num , 
    1-tower_num , 
    2-mass_info, list of string, [unknown, dead_load, live_load, plus_load],
    """

    RESULT_FLOOR_DATA_TABLE = "dsnStatFlrData"
    """包含了大多数楼层计算结果，包括风、地震的各类外力、承载力、刚度等等"""
    RESULT_FLOOR_DATA_USEFUL_COLUMNS_SEISMIC = [
        FLOOR_NUM,
        TOWER_NUM,
        "FlrFXInf",
        "FlrFYInf",  # 0 1 2 3
        "FlrVXInf",
        "FlrVYInf",
        "FlrMXInf",
        "FlrMYInf",  # 4 5 6 7
        "CZLXInf",
        "CZLYInf",
    ]
    """ 
    0-floor_num , 
    1-tower_num , 
    2-X方向地震外力,
    3-Y方向地震外力,
    4-X方向地震层间剪力,
    5-Y方向地震层间剪力,
    6-X方向地震倾覆力矩,
    7-Y方向地震倾覆力矩,
    8-X方向抗剪承载力,
    9-Y方向抗剪承载力,
    """

    RESULT_FLOOR_DATA_USEFUL_COLUMNS_STIFFNESS = [
        "StiffShearCutXInf",
        "StiffShearCutYInf",
        "StiffShearDisXInf",
        "StiffShearDisYInf",
        "StiffBendXInf",
        "StiffBendYInf",
    ]
    """ 
    包含了楼层的各类刚度，剪切刚度、剪力位移计算刚度、剪弯刚度
    0-剪切刚度X , 
    1-剪切刚度Y , 
    2-剪力位移计算刚度X,
    3-剪力位移计算刚度Y,
    4-剪弯刚度X,
    5-剪弯刚度Y,
    """

    RESULT_FLOOR_DATA_USEFUL_COLUMNS_WIND = [
        FLOOR_NUM,
        TOWER_NUM,
        "FlrWindFInf",
        "FlrWindVInf",  # 0 1 2 3
        "FlrWindMInf",
    ]
    """ 
    0-floor_num , 
    1-tower_num , 
    2-XY方向顺风外力,
    3-XY方向顺风剪力,
    4-XY方向顺风弯矩,
    """

    DISP_FLOOR_DATA_TABLE = "dsnStatDis"
    """包含了楼层在不同工况下的楼层位移"""

    DISP_FLOOR_DATA_USEFUL_COLUMNS_WIND = [
        FLOOR_NUM,
        TOWER_NUM,
        LOAD_CASE_ID,
        "MaxFlrAngleDis",
        "MinFlrAngleDis",
        "MaxD",
        "MassAveD",
    ]
    """
    0-floor_num , 
    1-tower_num , 
    2-loadCaseID，需要做筛选
    3-最大层间位移,
    4-最小层间位移,
    5-最大位移,
    6-平均位移,
    """

    ADJUST_COEF_TABLE = "dsnStatFlrAdjCoe"
    """楼层调整系数表格"""
    ADJUST_COEF_USEFUL_COLUMN = [FLOOR_NUM, TOWER_NUM, "JZBCoeXInf", "JZBCoeYInf"]
    """
    0-floor_num , 
    1-tower_num , 
    2-X方向剪重比调整系数
    3-Y方向剪重比调整系数
    """

    REAL_FLOOR_TABLE = "pmFlrAssembly"
    """楼层调整系数表格"""
    REAL_FLOOR_USEFUL_COLUMN = ["No", STD_FLR_ID, "Level", "Height"]
    """
    0-楼层编号 , 
    1-标准层ID , 
    2-层底高度
    3-楼层高度
    """
