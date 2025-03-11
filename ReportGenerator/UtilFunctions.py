from docx.oxml.xmlchemy import BaseOxmlElement
from docx.oxml.ns import qn, nsdecls

# 网上找的代码，有点东西
# https://stackoverflow.com/questions/33069697/how-to-setup-cell-borders-with-python-docx
# 这个是github上的讨论帖，在讨论帖中找到的
# https://github.com/python-openxml/python-docx/issues/1306
def set_cell_border(cell, **kwargs):
    """
    Set cell`s border
    Usage:

    set_cell_border(
        cell,
        top={"sz": 12, "val": "single", "color": "#FF0000", "space": "0"},
        bottom={"sz": 12, "color": "#00FF00", "val": "single"},
        start={"sz": 24, "val": "dashed", "shadow": "true"},
        end={"sz": 12, "val": "dashed"},
    )
    """
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()

    # check for tag existnace, if none found, then create one
    tc_borders = tc_pr.first_child_found_in("w:tcBorders")
    if tc_borders is None:
        tc_borders = BaseOxmlElement('w:tcBorders')
        tc_pr.append(tc_borders)

    # list over all available tags
    for edge in ('start', 'top', 'end', 'bottom', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)

            # check for tag existnace, if none found, then create one
            element = tc_borders.find(qn(tag))
            if element is None:
                element = BaseOxmlElement(tag)
                tc_borders.append(element)

            # looks like order of attributes is important
            for key in ["sz", "val", "color", "space", "shadow"]:
                if key in edge_data:
                    element.set(qn('w:{}'.format(key)), str(edge_data[key]))
            
def analysis_sub_and_super_script(context:str):
    """根据字符串中的'_'与'^'标志的上下标（上下标需要被{}包围起来），将字符串分隔并返回上下标结果
    返回的sub_or_super列表中，0代表常规字符，1代表下标，2代表上标，3代表highlighted
    Args:
        context (str): 输入的文字
    """
    contexts = []
    sub_or_super = [0]
    i = 0
    j = 0
    length = len(context)
    flag = False
    index_for_flag = {
        "_" : 1,
        "^" : 2,
        "*" : 3
    }
    
    for c in context:
        if (c in index_for_flag.keys()) and (j <length and context[j+1] =='{'):
            flag = True
            contexts.append(context[i:j])
            sub_or_super.append(index_for_flag[c])
            i = j  + 2
        if flag and c == "}":
            contexts.append(context[i:j])
            sub_or_super.append(0)
            i = j+1
            flag = False
        j+=1
    contexts.append(context[i:j])
    return contexts, sub_or_super

def add_comma_in_num_str(num:int):
    if not isinstance(num, int):
        raise ValueError("Only int number can be added.")
    num_str = str(num)[::-1]
    result = ""
    for i in range(len(num_str)):
        if i>0 and i%3 == 0 and num_str[i] !="-":
            result = "," + result
        result = num_str[i] + result
    return result
