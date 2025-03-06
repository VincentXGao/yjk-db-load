from typing import List

class RowDataFactory:
    '''
    This Class is used to extract data form row_data
    '''
    @classmethod
    def Extract_int(cls,row_data:List,index:int):
        RowDataFactory.__list_index_check(row_data,index)
        try:
            result = (int)(row_data[index])
        except:
            raise TypeError(f"Value: {row_data[index]} cannot be converted to int.")
        return result


    @classmethod
    def Extract_float(cls,row_data:List,index:int):
        RowDataFactory.__list_index_check(row_data,index)
        try:
            result = (float)(row_data[index])
        except:
            raise TypeError(f"Value: {row_data[index]} cannot be converted to float.")
        return result
    
    @classmethod
    def Extract_list(cls, row_data:List,index:int):
        RowDataFactory.__list_index_check(row_data,index)
        try:
            result = list(row_data[index].split(','))
        except:
            raise TypeError(f"Value: {row_data[index]} cannot be converted to list.")
        return result


    @classmethod
    def __list_index_check(cls,row_data:List,index:int):
        if len(row_data)<=index:
            raise IndexError("Index out of the range.")