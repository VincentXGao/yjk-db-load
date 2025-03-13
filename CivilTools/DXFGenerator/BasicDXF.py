import ezdxf
import warnings
from math import inf
from typing import List, Iterable, Tuple
from .LayerManager import CADLayer, CADColor,CADLineType
from .DrawingAttribs import DrawingAttribs,PolylineAttribs


class BasicDXF:
    file_extension = ".dxf"
    DXF2007 = "AC1021"
    line_type_patterns = {
        CADLineType.Continuous:[1,1],
        CADLineType.CENTER:[1,0.4,-0.2,0.1,-0.3],
        CADLineType.DASHDOT:[1,0.6,-0.2,0,-0.2],
        CADLineType.DASHED:[1,0.7,-0.3]
    }
    """线型及其Pattern定义，Pattern定义可参考ezdxf内的定义
    The simple line type pattern is a list of
    floats :code:`[total_pattern_length, elem1, elem2, ...]`
    where an element > 0 is a line, an element < 0 is a gap and  an
    element == 0.0 is a dot.
    """
    DIM_STYLE_PREFIX = "CT"
    TEXT_STYLE_NAME = "CT2025"
    TEXT_SHX = 'xd-hzs.shx'
    TEXT_BIG_SHX = 'xd-hztxt.shx'
    
    def __init__(self):
        self.doc = ezdxf.new(BasicDXF.DXF2007)
        self.model_space = self.doc.modelspace()
        self.__loaded_line_types = []
        self.__min_point = [inf,inf]
        self.__max_point = [-inf,-inf]
        self.__load_text_type()
        self.__load_dim_type(100)
        
    
    def init_layers(self, layer_list:List[CADLayer]):
        layers = self.doc.layers
        for my_layer in layer_list:
            # 如果图层名称已存在，则不进行新增
            if my_layer.name in [l.dxf.name for  l in layers]:
                warnings.warn(f"Layer {my_layer.name} already existed.")
                continue
            temp_layer = layers.new(name=my_layer.name)
            temp_layer.color = my_layer.color.value
            self.__load_line_type(
                my_layer.line_type.name,
                BasicDXF.line_type_patterns[my_layer.line_type]
            )
            temp_layer.dxf.linetype = my_layer.line_type.name
            self.doc.header['$CLAYER'] = my_layer.name
    
    
    def creat_test(self):
        self._add_polyline([[0,0],[5000,0],[5000,500]],PolylineAttribs("AA"))

    def _add_horizental_line(self, start_x, start_y, length:float,attribs:PolylineAttribs):
        self._add_polyline([[start_x,start_y],[start_x+length,start_y]],attribs)
        
    def _add_vertical_line(self, start_x, start_y, length:float,attribs:PolylineAttribs):
        self._add_polyline([[start_x,start_y],[start_x,start_y+length]],attribs)

    def _add_polyline(self,points:Iterable[Tuple[float, float]], attribs:PolylineAttribs):
        polyline = self.model_space.add_lwpolyline(points,close=attribs.close)
        polyline.dxf.layer = attribs.layer

        max_x = max([pt[0] for pt in points])
        max_y = max([pt[1] for pt in points])
        min_x = min([pt[0] for pt in points])
        min_y = min([pt[1] for pt in points])
        self.__update_boundary(max_x,max_y)
        self.__update_boundary(min_x,min_y)

    def _add_circle(self,center_point:Iterable[float],radius:float,attribs:DrawingAttribs):
        circle = self.model_space.add_circle(center_point,radius)
        circle.dxf.layer = attribs.layer

    def _add_dimension(self,
                       start_point:Iterable[float],
                       end_point:Iterable[float],
                       attribs:DrawingAttribs|None = None
                       ):
        dimension = self.model_space.add_linear_dim((0,0),
                                                    start_point,
                                                    end_point,
                                                    dimstyle="CT-100").render()
        
        if attribs != None:
            # 这里.dimension才是Dimension对象，才有dxf属性
            dimension.dimension.dxf.layer = attribs.layer

            
        
        
        
    def _add_text(self, context:str, insert_point):
        
        text = self.model_space.add_text(context,height=300)
        text.dxf.insert = insert_point
        text.dxf.style = BasicDXF.TEXT_STYLE_NAME
        
        
    
    def _save(self,path:str):
        self.__change_view()
        if not path.endswith(BasicDXF.file_extension):
            path += BasicDXF.file_extension
        for _ in range(10):
            try:
                self.doc.saveas(path)
            except Exception:
                path = path.replace(BasicDXF.file_extension,"1"+BasicDXF.file_extension)
    
    def __change_view(self):
        if (inf in self.__max_point or -inf in self.__min_point):
            return
        
        y_range = self.__max_point[1] - self.__min_point[1]
        x_range = self.__max_point[0] - self.__min_point[0]

        y_middle = (self.__max_point[1] + self.__min_point[1])/2
        # 为了使得内容靠右些，避免左侧panel占位的视觉影响
        x_middle = (self.__max_point[0] + self.__min_point[0]*3)/4
        # 乘以1.1的系数，增加了一些margin
        self.doc.set_modelspace_vport(max(x_range*1.1,y_range*1.1),(x_middle,y_middle))
    
    def __update_boundary(self, x, y):
        temp_x1 = self.__min_point[0]
        temp_y1 = self.__min_point[1]
        self.__min_point = [min(temp_x1,x),min(temp_y1,y)]

        temp_x2 = self.__max_point[0]
        temp_y2 = self.__max_point[1]
        self.__max_point = [max(temp_x2,x),max(temp_y2,y)]



    def __load_line_type(self, name:str, pattern:List[float]):
        if name in self.__loaded_line_types:
            return
        self.doc.linetypes.add(name,pattern)
        self.__loaded_line_types.append(name)
        
    def __load_dim_type(self, scale:int):
        # 获取标注样式表
        dimstyles = self.doc.dimstyles
        # 定义新标注样式的名称
        new_dimstyle_name = f"{BasicDXF.DIM_STYLE_PREFIX}-{scale}"
        # 创建新的标注样式
        new_dimstyle = dimstyles.new(new_dimstyle_name)
        # 设置标注文字样式
        new_dimstyle.dxf.dimtxsty = BasicDXF.TEXT_STYLE_NAME
        # 设置标注文字高度
        new_dimstyle.dxf.dimtxt = 2.5
        # 设置箭头大小
        new_dimstyle.dxf.dimasz = 1
        # 设置标注线超出尺寸界线的长度
        new_dimstyle.dxf.dimexo = 0.625
        # 设置尺寸界线起点偏移量
        new_dimstyle.dxf.dimse1 = 0.625
        #  设置全局比例
        new_dimstyle.dxf.dimscale = scale
        # 保留至整数
        new_dimstyle.dxf.dimrnd = 1
        # 改为建筑箭头
        new_dimstyle.dxf.dimblk = 'ARCHTICK'
        new_dimstyle.dxf.dimblk1 = 'ARCHTICK'
        new_dimstyle.dxf.dimblk2 = 'ARCHTICK'
        self.doc.header['$DIMSTYLE'] = new_dimstyle_name

        
    def __load_text_type(self):
        
        text_styles = self.doc.styles
        # 定义新文字样式的名称
        new_style_name = BasicDXF.TEXT_STYLE_NAME
        # 创建新的文字样式
        new_style = text_styles.new(new_style_name)
        # 设置文字样式的属性
        # 指定字体文件，例如 Arial 字体
        new_style.dxf.font = BasicDXF.TEXT_SHX
        new_style.dxf.bigfont = BasicDXF.TEXT_BIG_SHX
        # 设置文字高度
        new_style.dxf.height = 0
        new_style.dxf.width = 0.7
        # 修改当前选择的文字样式
        self.doc.header['$TEXTSTYLE'] = new_style_name
        
        
        