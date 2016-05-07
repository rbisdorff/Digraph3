#!python
#cython: language_level(3)
from distutils.core import setup, Extension
from Cython.Build import cythonize

ext = Extension(name="cSortingDigraphs",
                          sources=["cSortingDigraphs.pyx"],
			  )

setup(ext_modules=cythonize(ext))
