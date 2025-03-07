# yjk-db-load

这是一个用于加载 YJK 软件中，以`.ydb`结尾的数据库文件的 Python 库，可以加载的文件包括 `dtlmodel.ydb`（基础建模数据库）和`dsnModel.ydb`（计算结果数据库）。

A python package to load `.ydb` files created by YJK, including `dtlmodel.ydb` (which contains the basic building information), and `dsnModel.ydb` (which conatins the calculate result of the model).

## 安装: Installation

最新发布的稳定版（包括其依赖）可以通过 PyPI 进行下载：

The latest stable release (and required dependencies) can be installed from PyPI:

```shell
pip install yjk-db-load
```

## 快速上手: Quick Start

你可以轻易地从`.ydb`文件中提取出你想要的数据：

You can eaily extract the data you want from `.ydb` files:

```python
# 导入本模块
# import this lib
from YDBLoader import YDBLoader

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

## Others

我将持续更新，并且尽快完善本 python 库，如果你有任何问题或者建议，请随时通过邮箱联系我：`just_gxy@163.com`.

This package will be updated and completed soon.

If you have any questions or suggestion, please let me know.

You may contact with me via e-mail: `just_gxy@163.com.`
