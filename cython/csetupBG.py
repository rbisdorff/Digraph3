#!python
#cython: language_level(3)
from distutils.core import setup, Extension
from Cython.Build import cythonize

ext = Extension(name="cBigOutrankingDigraphs",
                          sources=["cBigOutrankingDigraphs.py"],
			  )

setup(ext_modules=cythonize(ext))
