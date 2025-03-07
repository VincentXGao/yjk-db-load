from typing import List

class RowDataFactory:
    '''
    This Class is used to extract data form row_data
    '''
    @classmethod
    def extract_int(cls,row_data:List,index:int):
        RowDataFactory.__list_index_check(row_data,index)
        return RowDataFactory.convert_to_int(row_data[index])

    @classmethod
    def extract_float(cls,row_data:List,index:int):
        RowDataFactory.__list_index_check(row_data,index)
        return RowDataFactory.convert_to_float(row_data[index])
    
    @classmethod
    def extract_list(cls, row_data:List,index:int):
        RowDataFactory.__list_index_check(row_data,index)
        try:
            result = list(row_data[index].split(','))
        except SyntaxError:
            raise TypeError(f"Value: {row_data[index]} cannot be converted to list.")
        return result

    @classmethod
    def convert_to_float(cls,string:"str"):
        try:
            result = (float)(string)
        except SyntaxError:
            raise TypeError(f"Value: {string} cannot be converted to float.")
        return result
    
    @classmethod
    def convert_to_int(cls,string:"str"):
        try:
            result = (int)(string)
        except SyntaxError:
            raise TypeError(f"Value: {string} cannot be converted to int.")
        return result
    
    @classmethod
    def __list_index_check(cls,row_data:List,index:int):
        if len(row_data)<=index:
            raise IndexError("Index out of the range.")