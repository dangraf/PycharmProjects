from setuptools import setup, find_packages

setup(
    name='Projects',
    packages=['Projects.Scraper',
              'Projects.mongo_data',
              'Projects.mailposi',
              'Projects.arrayOperations',
              'Projects.importData'],
    author='Daniel Grafström',
    author_email="dangraf@hotmail.com",
    description='Random packages',
    install_requires=[
        "schedule",
        "mongoengine",
        "requests",
        "configparser",
        "newspaper3k",
        "pandas",
        "numpy",
        "matplotlib",
    ],
)
