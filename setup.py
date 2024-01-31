#!/usr/bin/env python3
# Digraph3 installation script
# Copyright (C) 2016-2022 Raymond Bisdorff
####################


#from distutils.core import setup # deprecated since Python3.10
from setuptools import setup
CythonInstalled = True
VERSION = '3.12'

try:
    from Cython.Build import cythonize
except:
    print("""
The Cython compiler cannot be imported from the running Python environment!
If you wish to install the cythonized C-compiled modules you need to run:
...$ python3 -m pip install cython from the systems console.
""")
    CythonInstalled = False

if CythonInstalled:
    setup(name='Digraph3',
          version=VERSION,
          #version_command='svn info --show-item revision',
          py_modules=['arithmetics','digraphsTools','digraphs','perfTabs',
            'outrankingDigraphs','performanceQuantiles','mpOutrankingDigraphs',
                      'sortingDigraphs','votingProfiles',
            'linearOrders','transitiveDigraphs','dynamicProgramming',
            'graphs','pairings','randomNumbers','randomDigraphs',
            'randomPerfTabs', 'ratingDigraphs',
                      'sparseOutrankingDigraphs','xmcda'],
          ext_modules=cythonize("cython/*.pyx",language_level=3),
          license='digraph3_copyright.html',
          url='https://digraph3.readthedocs.io/en/latest/index.html',
          description='Lets you add bipolar graph and digraphs methods to your applications',
          author='Raymond Bisdorff',
          author_email='raymond.bisdorff@uni.lu',
          contact='https://rbisdorff.github.io/',
          )
else:
    setup(name='Digraph3',
          version=VERSION,
          #version_command='svn info --show-item revision',
          py_modules=['arithmetics','digraphsTools','digraphs','perfTabs',
                      'outrankingDigraphs','performanceQuantiles',
                      'mpOutrankingDigraphs',
            'sortingDigraphs','votingProfiles','dynamicProgramming',
            'linearOrders','transitiveDigraphs','graphs','randomNumbers',
            'randomDigraphs','randomPerfTabs','ratingDigraphs',
                      'sparseOutrankingDigraphs',
            'xmcda'],
          license='digraph3_copyright.html',
          url='https://digraph3.readthedocs.io/en/latest/index.html',
          description='Lets you add bipolar graph and digraphs methods to your applications',
          author='Raymond Bisdorff',
          author_email='raymond.bisdorff@uni.lu',
          contact='https://rbisdorff.github.io/',
          )
    
    

