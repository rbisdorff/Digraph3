#!/zsr/bin/env python3
#cython: language_level(3)
from distutils.core import setup, Extension
from Cython.Build import cythonize

ext = Extension(name="cOutrankingDigraphs",
                          sources=["cOutrankingDigraphs.pyx"],
			  )

setup(
      name='cDigraph3',
      version='Python3.5+/Cython',
      license='http://leopold-loewenheim.uni.lu/Digraph3/digraph3_copyright.html',
      url='http://leoopold-loewenheim.uni.lu/docDigraph3/',
      description='Lets you add bipolar graph and digraphs methods to your applications',
      author='Raymond Bisdorff',
      author_email='raymond.bisdorff@uni.lu',
      contact='http://leopold-loewenheim.uni.lu/bisdorff/',
      ext_modules=cythonize(ext,language_level=3),
)
