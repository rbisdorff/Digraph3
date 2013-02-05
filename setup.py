#!/usr/bin/python
# browserauth installation script
#

from distutils.core import setup

setup(name='digraphs',
      version='Python3: 2.0',
      py_modules=['digraphs','perfTabs','outrankingDigraphs','sortingDigraphs','votingDigraphs','linearOrders','iqagent'],
      license='http://ernst-schroeder.uni.lu/Digraph/digraph_copyright.html',
      url='http://ernst-schroeder.uni.lu/Digraph/',
      description='Lets you add bipolar digraph methods to your applications',
      author='Raymond Bisdorff',
      author_email='raymond.bisdorff@uni.lu',
      contact='http://charles-sanders-peirce.uni.lu/bisdorff/',
      )

