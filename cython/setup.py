##################
# install all cythonized modules inplace with
# ...$python3 setup.py buid_ext --inplace
# (c) R. Bisdorff 2024
#####################
from setuptools import Extension, setup
from Cython.Build import cythonize
import sys

if sys.platform.startswith("win"):
    openmp_arg = '/openmp'
else:
    openmp_arg = '-fopenmp'


ext_modules = [
    Extension(
        "*",
        ["*.pyx"],
        extra_compile_args=[openmp_arg],
        extra_link_args=[openmp_arg],
    ),
    Extension(
        "*",
        ["*.pyx"],
        extra_compile_args=[openmp_arg],
        extra_link_args=[openmp_arg],
    )
]

setup(
    name='parallel-tutorial',
    ext_modules=cythonize(ext_modules,language_level=3),
) 
