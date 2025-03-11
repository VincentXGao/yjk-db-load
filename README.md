# Civil_Tools

这是一个针对结构工程师开发的，集成了模型设计、结果分析、绘制图纸、出具计算书等多个模块的工具包。

具体包含：

- [YDB 数据库加载工具](#YDBLoader) ( `YDBLoader` )
- [各类图纸绘制工具](#DXFGenerator) ( `DXFGenerator` )
- [各类报告计算书生成工具](#ReportGenerator) ( `ReportGenerator` )
- [各类数据图片绘制工具](#FigureGenerator) ( `FigureGenerator` )

## 安装: Installation

最新发布的稳定版（包括其依赖）可以通过 PyPI 进行下载：

The latest stable release (and required dependencies) can be installed from PyPI:

<div style=" border: 1px solid #ff0000; padding: 10px; border-radius: 5px; margin-bottom: 10px">
    <strong>注意：</strong> pip时使用的模块的名字是 <strong>civil-tools-v </strong>！
    <br>
    <strong>Notice：</strong> The module name for pip is <strong>civil-tools-v</strong> !
</div>

```shell
pip install civil-tools-v
```

<a id="YDBLoader"></a>

## 快速上手: Quick Start

### YDB 数据库加载工具 ( `YDBLoader` )

这是一个用于加载 YJK 软件中，以`.ydb`结尾的数据库文件的 Python 库，可以加载的文件包括 `dtlmodel.ydb`（基础建模数据库）和`dsnModel.ydb`（计算结果数据库）。

A python package to load `.ydb` files created by YJK, including `dtlmodel.ydb` (which contains the basic building information), and `dsnModel.ydb` (which conatins the calculate result of the model).

你可以轻易地从`.ydb`文件中提取出你想要的数据：

You can eaily extract the data you want from `.ydb` files:

```python
# 导入本模块
# import this lib
from CivilTools.YDBLoader import YDBLoader

# 定义你的.ydb文件路径
# define your .ydb file path
your_ydb_file = r"your_yjk_model/施工图/dtlmodel.ydb"

# 根据文件数据，创建model
# create model by data
model = YDBLoader(your_ydb_file)

# 通过内置的各种方法，获取你需要的数据
# get the data you want, by various built-in funcitons
columns = model.get_columns()
for col in columns:
    print(col.joint)
```

运行上述代码，你应该可以看到如下的输出：

The code is expected to print the data like follow:

```
Joint(id:1003):[x:54.9286,y:61.9286]:stdFlrId:1001
Joint(id:1004):[x:54.9286,y:9061.9286]:stdFlrId:1001
Joint(id:1005):[x:54.9286,y:18061.9286]:stdFlrId:1001
Joint(id:1006):[x:9054.9286,y:61.9286]:stdFlrId:1001
Joint(id:1007):[x:9054.9286,y:9061.9286]:stdFlrId:1001
Joint(id:1008):[x:9054.9286,y:18061.9286]:stdFlrId:1001
Joint(id:1009):[x:18054.9286,y:61.9286]:stdFlrId:1001
Joint(id:1010):[x:18054.9286,y:9061.9286]:stdFlrId:1001
Joint(id:1011):[x:18054.9286,y:18061.9286]:stdFlrId:1001
Joint(id:1012):[x:27054.9286,y:61.9286]:stdFlrId:1001
Joint(id:1013):[x:27054.9286,y:9061.9286]:stdFlrId:1001
Joint(id:1014):[x:27054.9286,y:18061.9286]:stdFlrId:1001
```

<a id="DXFGenerator"></a>

### 各类图纸绘制工具 ( `DXFGenerator` )

这是一个用于绘制各类结构相关图纸的工具，包括各类节点详图、大样，甚至整层楼的模板图等等。

但是这个模块暂时处于待开发状态....

<a id="ReportGenerator"></a>

### 各类报告计算书生成工具 ( `ReportGenerator` )

这是一个用于生成各类文本的工具，目前包括：

- 抗震审查报告（根据 YJK 计算结果生成）
- 混凝土板式楼梯计算书

你可以轻易地从`CivilTools.ReportGenerator`中导出并使用它：

```python

from CivilTools.ReportGenerator import SeismicReport

report = SeismicReport()
report.creat_doc()
report.save("seismic_review_report.docx")

```

```python

from CivilTools.ReportGenerator import StairCalculationReport

report = StairCalculationReport()
report.set_stair_data()
report.set_calculate_info()
report.create()
report.save("stair_calculation_sheet.docx")

```

目前版本中的内容仍待持续完善...

<a id="FigureGenerator"></a>

### 各类数据图片绘制工具 ( `FigureGenerator` )

这是一个用于绘制各类图标的工具，完善中...

## Others

我将持续更新，并且尽快完善本 python 库，如果你有任何问题或者建议，请随时通过邮箱联系我：`just_gxy@163.com`.

This package will be updated and completed soon.

If you have any questions or suggestion, please let me know.

You may contact with me via e-mail: `just_gxy@163.com.`
