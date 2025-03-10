from .BuildingDefine import Beam,Column,Joint,ComponentType,Grid
from .BuildingDefine import SinglePeriod, Period, MassResult,SingleMassResult
from .BuildingDefine import ValuePeer, FloorSeismicResult , SeismicResult
from .BuildingDefine.Section import Section,ShapeEnum
from .SQLiteConnector import Connector,YDBTableName,RowDataFactory
from .YDBType import YDBType
import os
from typing import List, Dict

class YDBLoader:

    def __init__(self, file_name:str = None, ydb_type:YDBType = None):
        # default type is ModelType
        if not file_name.endswith(".ydb"):
            raise ValueError("Plase use file ends with .ybd!")
        self.connector = Connector(file_name)
        self.ydb_type = self.__check_ydb_type()
    
    def get_columns(self)->List[Column]:
        columns = []
        sections = self.__get_sections(ComponentType.Column)
        row_data = self.connector.extract_table_by_columns(
            YDBTableName.COLUMN_TABLE_NAME,
            YDBTableName.COLUMN_TABLE_USEFUL_COLUMNS
            )
        for temp_column in row_data:
            temp_col_id = RowDataFactory.extract_int(temp_column,0)
            joint_id = RowDataFactory.extract_int(temp_column,1)
            sect_id = RowDataFactory.extract_int(temp_column,2)
            joint = self.__find_joint_by_id(joint_id)
            sect = [s for s in sections if s.id == sect_id][0]
            new_column = Column(temp_col_id,joint,sect)
            columns.append(new_column)
        return columns
    
    def get_beams(self)->List[Beam]:
        beams = []      
        sections = self.__get_sections(ComponentType.Beam)
        row_data = self.connector.extract_table_by_columns(
            YDBTableName.BEAM_TABLE_NAME,
            YDBTableName.BEAM_TABLE_USEFUL_COLUMNS
            )
        for temp_beam in row_data:
            temp_beam_id = RowDataFactory.extract_int(temp_beam,0)
            grid_id = RowDataFactory.extract_int(temp_beam,1)
            grid = self.__find_grid_by_id(grid_id) 
            sect_id = RowDataFactory.extract_int(temp_beam,2)
            sect = [s for s in sections if s.id == sect_id][0]
            new_beam = Beam(temp_beam_id,grid.start_joint,grid.end_joint,sect)
            beams.append(new_beam)
        return beams

    def __get_sections(self,comp_type:ComponentType):
        table_name = ""
        table_columns = []       
        table_names_for_different_comptype = {
            ComponentType.Column:
                [YDBTableName.COLUMN_SECTION_TABLE_NAME,
                 YDBTableName.SECTION_TABLE_USEFUL_COLUMNS],
            ComponentType.Beam:
                [YDBTableName.BEAM_SECTION_TABLE_NAME,
                 YDBTableName.SECTION_TABLE_USEFUL_COLUMNS],
        }
        if (comp_type not in table_names_for_different_comptype.keys()):
            raise ValueError(f"{comp_type.name} is not suppported yet.")
        # 这里根据不同的构件类型，进行不同的截面数据获取
        table_name = table_names_for_different_comptype[comp_type][0]
        table_columns = table_names_for_different_comptype[comp_type][1]
        row_data = self.connector.extract_table_by_columns(table_name,table_columns)
        sections = []
        for temp_section in row_data:
            temp_section_id = RowDataFactory.extract_int(temp_section,0)
            # 这里的mat暂时没用到
            mat = RowDataFactory.extract_int(temp_section,1)
            kind = RowDataFactory.extract_int(temp_section,2)
            shape_val = RowDataFactory.extract_list(temp_section,3)[1:]
            new_section = Section(temp_section_id,ShapeEnum.ConvertToShapeEnum(kind),shape_val,mat)
            sections.append(new_section)
        return sections

    def __get_joints(self)->Dict[int,Joint]:
        if hasattr(self, 'joint_list'):
            return self.joint_list
        table_name = YDBTableName.JOINT_TABLE_NAME
        useful_columns = YDBTableName.JOINT_TABLE_USEFUL_COLUMNS
        row_data = self.connector.extract_table_by_columns(table_name,useful_columns)
        joint_list = {}
        for temp_joint in row_data:
            temp_joint_id = RowDataFactory.extract_int(temp_joint,0)
            x = RowDataFactory.extract_float(temp_joint,1)
            y = RowDataFactory.extract_float(temp_joint,2)
            std_flr_id = RowDataFactory.extract_int(temp_joint,3)
            new_joint = Joint(temp_joint_id,x,y,std_flr_id)
            joint_list[temp_joint_id] = new_joint
        self.joint_list = joint_list
        return self.joint_list

    def __get_grids(self)->Dict[int,Grid]:
        if hasattr(self, 'grid_list'):
            return self.grid_list
        table_name = YDBTableName.GRID_TABLE_NAME
        useful_columns = YDBTableName.GRID_TABLE_USEFUL_COLUMNS
        row_data = self.connector.extract_table_by_columns(table_name,useful_columns)
        grid_list = {}
        for temp_grid in row_data:
            temp_grid_id = RowDataFactory.extract_int(temp_grid,0)
            start_joint_id = RowDataFactory.extract_int(temp_grid,1)
            end_joint_id = RowDataFactory.extract_int(temp_grid,2)
            s_joint = self.__find_joint_by_id(start_joint_id)
            e_joint = self.__find_joint_by_id(end_joint_id)
            grid = Grid(temp_grid_id,s_joint, e_joint)
            grid_list[temp_grid_id] = grid
        self.grid_list = grid_list
        return self.grid_list        
        
    def __check_ydb_type(self)->YDBType:
        if self.connector.is_table_in_db(YDBTableName.JOINT_TABLE_NAME):
            return YDBType.ModelYDB
        if self.connector.is_table_in_db(YDBTableName.RESULT_PERIOD_TABLE):
            return YDBType.ResultYDB
        raise ValueError("This ydb database is not Model YDB neither Result YDB. Please use correct ydb file.")
    
    def __find_joint_by_id(self,joint_id:int)->Joint:
        joint_list = self.__get_joints()
        try:
            return joint_list[joint_id]
        except KeyError:
            raise ValueError(f"No Joint's ID is {joint_id}.")
    
    def __find_grid_by_id(self,grid_id:int)->Grid:
        grid_list = self.__get_grids()
        try:
            return grid_list[grid_id]
        except KeyError:
            raise ValueError(f"No Joint's ID is {grid_id}.")
    
    def __check_result_model(self, extracting_data_type):
        if self.ydb_type != YDBType.ResultYDB:
            raise TypeError("This model is not ResultYDB file, "+
                            f"dont have {extracting_data_type} result, please retry.")
    
    def get_mass_result(self)->MassResult:
        self.__check_result_model("mass")
        table_name = YDBTableName.RESULT_MASS_TABLE
        useful_columns = YDBTableName.RESULT_MASS_USEFUL_COLUMNS
        row_data = self.connector.extract_table_by_columns(table_name,useful_columns)
        mass_list = []
        for temp_mass in row_data:
            floor_num = RowDataFactory.convert_to_int(temp_mass,0)
            tower_num = RowDataFactory.convert_to_int(temp_mass,1)
            mass_info = RowDataFactory.extract_list(temp_mass,2)
            dead_load = RowDataFactory.convert_to_float(mass_info[1])
            live_load = RowDataFactory.convert_to_float(mass_info[2])
            #  TODO: 需要计算slab的结果
            slab_area = 10
            single_mass = SingleMassResult(floor_num,tower_num,dead_load,live_load,slab_area)
            mass_list.append(single_mass)      
        return MassResult(mass_list)
    
    def get_period_result(self)->Period:
        self.__check_result_model("period")
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

    def get_seismic_result(self)->SeismicResult:
        self.__check_result_model("seismic")
        table_name = YDBTableName.RESULT_FLOOR_DATA_TABLE
        useful_columns = YDBTableName.RESULT_FLOOR_DATA_USEFUL_COLUMNS_SEISMIC
        row_data = self.connector.extract_table_by_columns(table_name,useful_columns)
        floor_result_list = []
        for temp_floor in row_data:
            floor_num = RowDataFactory.extract_int(temp_floor,0)
            tower_num = RowDataFactory.extract_int(temp_floor,1)
            force_x = RowDataFactory.convert_to_float(
                RowDataFactory.extract_list(temp_floor,2)[1])
            force_y = RowDataFactory.convert_to_float(
                RowDataFactory.extract_list(temp_floor,3)[1])
            shear_x = RowDataFactory.convert_to_float(
                RowDataFactory.extract_list(temp_floor,4)[1])
            shear_y = RowDataFactory.convert_to_float(
                RowDataFactory.extract_list(temp_floor,5)[1])
            moment_x = RowDataFactory.convert_to_float(
                RowDataFactory.extract_list(temp_floor,6)[1])
            moment_y = RowDataFactory.convert_to_float(
                RowDataFactory.extract_list(temp_floor,7)[1])
            force = ValuePeer(force_x,force_y)
            shear = ValuePeer(shear_x, shear_y)
            moment = ValuePeer(moment_x,moment_y)
            
            temp_floor_result = FloorSeismicResult(floor_num,tower_num,force,shear,moment)
            floor_result_list.append(temp_floor_result)
        
        return SeismicResult(floor_result_list)


if __name__ == "__main__":
    file_path = "testfiles/dtlmodel1.ydb"
    loader = YDBLoader(file_path)
    columns = loader.get_columns()

    for col in columns:
        print(col.section,col.joint)
        