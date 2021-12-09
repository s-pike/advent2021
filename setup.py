from setuptools import setup, find_packages

setup(
   name='aoc2021',
   version='1.0',
   description='Module containing supporting function for advent of code 2021',
   author='Stephen Pike',   
   packages=find_packages(include=['aoc2021']),  #same as name
)