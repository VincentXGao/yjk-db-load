from setuptools import setup, find_packages

setup(
    name='yjk_db_load',  # 包的名称
    version='0.0.2',  # 包的版本号
    author='Xinyu Gao (Vincent)',  # 作者姓名
    author_email='just_gxy@163.com',  # 作者邮箱
    description='A package to load .ydb files created by YJK.',  # 包的简短描述
    long_description=open('README.md').read(),  # 包的详细描述
    long_description_content_type='text/markdown',  # 详细描述的内容类型
    url='https://github.com/VincentXGao/yjk-db-load',  # 项目的 URL
    packages=['src.YDBLoader'],  # 自动发现并包含所有的包
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],  # 包的分类信息
    python_requires='>=3.6',  # 所需的 Python 版本
)