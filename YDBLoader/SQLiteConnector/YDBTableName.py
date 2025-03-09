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


class YDBTableName():
    JOINT_TABLE_NAME = "tblJoint"
    JOINT_TABLE_USEFUL_COLUMNS = [ID,"X","Y",STD_FLR_ID]
    
    GRID_TABLE_NAME = "tblGrid"
    GRID_TABLE_USEFUL_COLUMNS = [ID,JOINT_ID_1,JOINT_ID_2]
    """ 
    0-ID , 
    1-Joint1_ID , 
    2-Joint2_ID ,
    """
    
    COLUMN_SECTION_TABLE_NAME = "tblColSect"
    BEAM_SECTION_TABLE_NAME = "tblBeamSect"
    SECTION_TABLE_USEFUL_COLUMNS = [ID,"Mat","Kind","ShapeVal"]
    
    COLUMN_TABLE_NAME = "tblColSeg"
    COLUMN_TABLE_USEFUL_COLUMNS = [ID,JOINT_ID,SECTION_ID,ECC_X,ECC_Y,ROTATION]
    """ 
    0-ID , 
    1-Joint_ID , 
    2-Section_ID ,
    3-EccX ,
    4-EccY ,
    5-Rotation
    """
    
    BEAM_TABLE_NAME = "tblBeamSeg"
    BEAM_TABLE_USEFUL_COLUMNS = [ID,GRID_ID,SECTION_ID,ECC,"HDiff1","HDiff2"]
    """ 
    0-ID , 
    1-Grid_ID , 
    2-Section_ID ,
    3-Ecc ,
    4-HDiff1 ,
    5-HDiff2
    """

    RESULT_PERIOD_TABLE = "calEigenInf"
    RESULT_PERIOD_USEFUL_COLUMNS = ["ModuleID","EigenNo","Period","Angle","CoeffInf","mInf"]

