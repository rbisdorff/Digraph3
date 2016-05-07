#!python
#cython: language_level(3)
from distutils.core import setup, Extension
from Cython.Build import cythonize

ext = Extension(name="cOutrankingDigraphs",
                          sources=["cOutrankingDigraphs.pyx"],
			  )

setup(ext_modules=cythonize(ext))
