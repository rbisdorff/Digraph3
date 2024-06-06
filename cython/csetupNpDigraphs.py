#!/usr/bin/env python3
#cython: language_level(3)
from setuptools import setup
from Cython.Build import cythonize
#from distutils.extension import Extension
from setuptools.extension import Extension
from Cython.Distutils import build_ext

setup(
  name = "cnpBipolarDigraphs",
  cmdclass = {"build_ext": build_ext},
  ext_modules =
  [
    Extension("cnpBipolarDigraphs",
              ["cnpBipolarDigraphs.pyx"],
              extra_compile_args = ["-O0", "-fopenmp"],
              extra_link_args=['-fopenmp']
              )
  ]
)

