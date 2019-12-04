#!/usr/bin/env python3
# browserauth installation script
#

from distutils.core import setup
CythonInstalled = True
try:
    from Cython.Build import cythonize
except:
    print("""
The Cython compiler cannot be imported from the running Python environment!
If you wish tu install the cythonized C-compiled modules you need to run:
...$ pip install cython
from the systems console.
""")
    CythonInstalled = False 

if CythonInstalled:
    setup(name='Digraph3',
          version="Python3.7",
          #version_command='svn info --show-item revision',
          py_modules=['arithmetics','digraphsTools','digraphs','perfTabs',
                      'outrankingDigraphs','performanceQuantiles',\
            'sortingDigraphs','votingProfiles',\
            'linearOrders','transitiveDigraphs',\
            'graphs','htmlmodel','randomNumbers','randomDigraphs',\
            'randomPerfTabs', 'sparseOutrankingDigraphs','xmcda'],
          ext_modules=cythonize("cython/*.pyx",language_level=3),
          license='http://leopold-loewenheim.uni.lu/Digraph3/digraph3_copyright.html',
          url='http://leoopold-loewenheim.uni.lu/docDigraph3/',
          description='Lets you add bipolar graph and digraphs methods to your applications',
          author='Raymond Bisdorff',
          author_email='raymond.bisdorff@uni.lu',
          contact='http://leopold-loewenheim.uni.lu/bisdorff/',
          )
else:
    setup(name='Digraph3',
          version="Python3.7",
          #version_command='svn info --show-item revision',
          py_modules=['arithmetics','digraphsTools','digraphs','perfTabs',
                      'outrankingDigraphs','performanceQuantiles',\
            'sortingDigraphs','votingProfiles',\
            'linearOrders','transitiveDigraphs','graphs','htmlmodel','randomNumbers',\
            'randomDigraphs','randomPerfTabs','sparseOutrankingDigraphs',\
                      'xmcda'],
          license='http://leopold-loewenheim.uni.lu/Digraph3/digraph3_copyright.html',
          url='http://leoopold-loewenheim.uni.lu/docDigraph3/',
          description='Lets you add bipolar graph and digraphs methods to your applications',
          author='Raymond Bisdorff',
          author_email='raymond.bisdorff@uni.lu',
          contact='http://leopold-loewenheim.uni.lu/bisdorff/',
          )
    
    

