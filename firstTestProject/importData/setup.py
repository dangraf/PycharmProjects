""" setup """
from setuptools import setup, find_packages

setup(
    name='importData',
    version='0.0.1',
    url='https://github.com/fmfn/BayesianOptimization',
    packages=find_packages(),
    author='Daniel Grafström',
    author_email="dangraf@hotmail.com",
    description='Bitcoin historical data package',
    install_requires=[
        "pandas >= 0.18.1",
        "numpy >= 1.12.1",
        "pyvalid >= 0.9",
    ],
)
