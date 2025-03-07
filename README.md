# yjk-db-load

A package to load `.ydb` files created by YJK, including `dtlmodel.ydb` (which contains the basic building information), and `dsnModel.ydb` (which conatins the calculate result of the model).

## Installation

The latest stable release (and required dependencies) can be installed from PyPI:

```shell
pip install yjk-db-load
```

## Quick Start

You can eaily extract the data you want from `.ydb` files

```python
from YDBLoader import YDBLoader

your_ydb_file = r"your_yjk_model/施工图/dtlmodel.ydb"
model = YDBLoader(your_ydb_file)
columns = model.get_columns()
for col in columns:
    print(col.joint)
```

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

This package will be updated and completed soon.

If you have any questions or suggestion, please let me know.

You may contact with me via e-mail: `just_gxy@163.com.`
