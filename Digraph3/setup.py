#!/usr/bin/python
# browserauth installation script
#

from distutils.core import setup

setup(name='Digraph3',
      version='Python3.4rev1020',
      py_modules=['digraphs','perfTabs','outrankingDigraphs',\
        'sortingDigraphs','votingDigraphs',\
        'linearOrders','weakOrders',\
        'iqagent','graphs','htmlmodel','randomNumbers'],
      license='http://leopold-loewenheim.uni.lu/Digraph3/digraph3_copyright.html',
      url='http://leoopold-loewenheim.uni.lu/Digraph3/',
      description='Lets you add bipolar graph and digraphs methods to your applications',
      author='Raymond Bisdorff',
      author_email='raymond.bisdorff@uni.lu',
      contact='http://charles-sanders-peirce.uni.lu/bisdorff/',
      )

