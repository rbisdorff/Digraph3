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
...$ python3 -m pip install cython
from the systems console.
""")
    CythonInstalled = False

if CythonInstalled:
    setup(name='Digraph3',
          version="Python3.9.1",
          #version_command='svn info --show-item revision',
          py_modules=['arithmetics','digraphsTools','digraphs','perfTabs',
                      'outrankingDigraphs','performanceQuantiles',\
            'sortingDigraphs','votingProfiles',\
            'linearOrders','transitiveDigraphs',\
            'graphs','randomNumbers','randomDigraphs',\
            'randomPerfTabs', 'sparseOutrankingDigraphs','xmcda'],
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
          version="Python3.9.1",
          #version_command='svn info --show-item revision',
          py_modules=['arithmetics','digraphsTools','digraphs','perfTabs',
                      'outrankingDigraphs','performanceQuantiles',\
            'sortingDigraphs','votingProfiles',\
            'linearOrders','transitiveDigraphs','graphs','randomNumbers',\
            'randomDigraphs','randomPerfTabs','sparseOutrankingDigraphs',\
                      'xmcda'],
          license='digraph3_copyright.html',
          url='https://digraph3.readthedocs.io/en/latest/index.html',
          description='Lets you add bipolar graph and digraphs methods to your applications',
          author='Raymond Bisdorff',
          author_email='raymond.bisdorff@uni.lu',
          contact='https://rbisdorff.github.io/',
          )
    
    

