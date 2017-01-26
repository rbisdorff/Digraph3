#!/usr/bin/env python3
# browserauth installation script
#

from distutils.core import setup

setup(name='Digraph3',
      version='Python3.5+',
      py_modules=['arithmetics','digraphsTools','digraphs','perfTabs','outrankingDigraphs',\
        'sortingDigraphs','votingDigraphs',\
        'linearOrders','weakOrders',\
        'iqagent','graphs','htmlmodel','randomNumbers','randomDigraphs','randomPerfTabs',
        'bigOutrankingDigraphs','sparseOutrankingDigraphs'],
      license='http://leopold-loewenheim.uni.lu/Digraph3/digraph3_copyright.html',
      url='http://leoopold-loewenheim.uni.lu/docDigraph3/',
      description='Lets you add bipolar graph and digraphs methods to your applications',
      author='Raymond Bisdorff',
      author_email='raymond.bisdorff@uni.lu',
      contact='http://leopold-loewenheim.uni.lu/bisdorff/',
      )

