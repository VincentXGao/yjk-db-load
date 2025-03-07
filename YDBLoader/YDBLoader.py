from .BuildingDefine import Beam,Column,Joint,ComponentType
from .BuildingDefine.Section import Section,ShapeEnum
from .BuildingDefine.GlobalResult import SinglePeriod, Period
from .SQLiteConnector import Connector,YDBTableName,RowDataFactory
from .YDBType import YDBType
import os
from typing import List

class YDBLoader:

    def __init__(self, file_name = None, ydb_type:YDBType = None):
        # default type is ModelType
        self.ydb_type = ydb_type if ydb_type !=None else YDBType.ModelYDB
        self.connector = Connector(file_name)
        
    def sum(self,x,y):
        return x+y
    
    def get_beams(self):
        a = Beam()
        return a
    
    def get_columns(self)->List[Column]:
        columns = []
        joints = self.__get_joints()
        sections = self.__get_sections(ComponentType.Column)
        row_data = self.connector.extract_table_by_columns(YDBTableName.COLUMN_TABLE_NAME,YDBTableName.COLUMN_TABLE_USEFUL_COLUMNS)
        for temp_column in row_data:
            temp_col_id = RowDataFactory.extract_int(temp_column,0)
            joint_id = RowDataFactory.extract_int(temp_column,1)
            sect_id = RowDataFactory.extract_int(temp_column,2)
            joint = [i for i in joints if i.id == joint_id][0]
            sect = [s for s in sections if s.id == sect_id][0]
            new_column = Column(temp_col_id,joint,sect)
            columns.append(new_column)
        return columns


    def __get_sections(self,comp_type:ComponentType):
        table_name = ""
        table_columns = []
        # 这里根据不同的构件类型，进行不同的截面数据获取
        if comp_type == ComponentType.Column:
            table_name = YDBTableName.COLUMN_SECTION_TABLE_NAME
            table_columns = YDBTableName.COLUMN_SECTION_TABLE_USEFUL_COLUMNS
        row_data = self.connector.extract_table_by_columns(table_name,table_columns)
        sections = []
        for temp_section in row_data:
            temp_section_id = RowDataFactory.extract_int(temp_section,0)
            # 这里的mat暂时没用到
            mat = RowDataFactory.extract_int(temp_section,1)
            kind = RowDataFactory.extract_int(temp_section,2)
            shape_val = RowDataFactory.extract_list(temp_section,3)[1:]
            new_section = Section(temp_section_id,ShapeEnum.ConvertToShapeEnum(kind),shape_val)
            sections.append(new_section)
        return sections

    def __get_joints(self):
        table_name = YDBTableName.JOINT_TABLE_NAME
        useful_columns = YDBTableName.JOINT_TABLE_USEFUL_COLUMNS
        row_data = self.connector.extract_table_by_columns(table_name,useful_columns)
        joint_list = []
        for temp_joint in row_data:
            temp_joint_id = RowDataFactory.extract_int(temp_joint,0)
            x = RowDataFactory.extract_float(temp_joint,1)
            y = RowDataFactory.extract_float(temp_joint,2)
            std_flr_id = RowDataFactory.extract_int(temp_joint,3)
            new_joint = Joint(temp_joint_id,x,y,std_flr_id)
            joint_list.append(new_joint)
        return joint_list
        
    def get_period_result(self):
        if self.ydb_type != YDBType.ResultYDB:
            raise TypeError("This model is not ResultYDB file, please retry ")
        table_name = YDBTableName.RESULT_PERIOD_TABLE
        useful_columns = YDBTableName.RESULT_PERIOD_USEFUL_COLUMNS
        row_data = self.connector.extract_table_by_columns(table_name,useful_columns)
        periods = []
        for temp_period in row_data:
            module_id = RowDataFactory.extract_int(temp_period,0)
            if module_id !=1:
                continue
            period_index = RowDataFactory.extract_int(temp_period,1)
            time = RowDataFactory.extract_float(temp_period,2)
            angle = RowDataFactory.extract_float(temp_period,3)
            coeff = RowDataFactory.extract_list(temp_period,4)
            mass_participate = RowDataFactory.extract_list(temp_period,5)
            period = SinglePeriod(period_index,time,angle
                                  ,RowDataFactory.convert_to_float(coeff[1])
                                  ,RowDataFactory.convert_to_float(coeff[2])
                                  ,RowDataFactory.convert_to_float(coeff[-1])
                                  ,RowDataFactory.convert_to_float(mass_participate[1])
                                  ,RowDataFactory.convert_to_float(mass_participate[2])
                                  ,RowDataFactory.convert_to_float(mass_participate[-1])
                                  )
            periods.append(period)
        return Period(periods)

if __name__ == "__main__":
    file_path = "testfiles/dtlmodel1.ydb"
    loader = YDBLoader(file_path)
    columns = loader.get_columns()

    for col in columns:
        print(col.section,col.joint)
        