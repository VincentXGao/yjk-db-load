from setuptools import setup, find_packages

setup(
    name='civil_tools',  # 包的名称
    version='0.0.1',  # 包的版本号
    author='Xinyu Gao (Vincent)',  # 作者姓名
    author_email='just_gxy@163.com',  # 作者邮箱
    description='A powerful tool for civil engineer in their work.',  # 包的简短描述
    long_description=open('README.md',encoding="utf-8").read(),  # 包的详细描述
    long_description_content_type='text/markdown',  # 详细描述的内容类型
    url='https://github.com/VincentXGao/civil-tools',  # 项目的 URL
    packages=find_packages(exclude=['tests']),  # 自动发现并包含所有的包
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],  # 包的分类信息
    install_requires = [
        "numpy>=2.0",
        "python-docx>=1.0",
        "matplotlib>=3.10.0"
    ], # 依赖的库及其最低版本
    python_requires='>=3.6',  # 所需的 Python 版本
)