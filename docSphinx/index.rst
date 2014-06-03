Technical Documentation of the Digraph resources!
=================================================
:Author: Raymond Bisdorff, University of Luxembourg FSTC/CSC
:Version: $Revision: Python 3.3$
:Copyright: R. Bisdorff 2013-2014

.. _Introduction-label:

Introduction
------------

This Technical Manual describes the Python-3 implementation of generic resources for implementing decision aid algorithms in the context of bipolarly-valued outranking digraphs. This computing ressource is useful in the field of algorithmic decision theory and more specifically in outranking based multiple criteria decision aid.

Two downlaod options are given:
    
1. Either (easiest under Linux or Mac OS-X), by using a subversion client::
..$svn co http://leopold-loewenheim.uni.lu/svn/repos/Digraph3
       
2. Or, download and extract the latest distribution tar.gz archive::
http://leopold-loewenheim.uni.lu/svn/repos/Digraph3/dist/digraphs-Python3-xxx.tar.gz 

Developping the Rubis decision support methodology is an ongoing research project of Raymond Bisdorff <http://charles-sanders-peirce.uni.lu/bisdorff/>, University of Luxembourg.

A tutorial with coding examples is available here: :ref:`Tutorial-label`

The basic idea of these Python modules is to make easy python interactive sessions or write short Python scripts for computing all kind of results from a bipolar valued outranking digraph. These include such features as maximal independent or irredundant choices, maximal dominant or absorbent choices etc. 

The Python development of these computing ressources offers the advantage of an easy to write and maintain OOP source code as expected from a performing scripting language without loosing on efficiency in execution times compared to compiled languages such as C++ or Java. 

The Digraph3 source code is split into several interdependant modules, where the ``digraphs`` module is the master source.

:ref:`digraphs-label`
     main part of the source code with the generic ``Digraph`` class; 
:ref:`graphs-label`
     specialization for undirected graphs with brigde to the ``Digraph`` module ressources;
:ref:`outrankingDigraphs-label`
     new Python3 versioned ``BipolarOutrankingDigraph`` classes; 
:ref:`perfTabs-label` 
     everything needed for handling Rubis Performance Tableaux;
:ref:`votingDigraphs-label` 
     additional classes and methods for computing election results;
:ref:`sortingDigraphs-label`
     additional tools for solving sorting problems;
:ref:`linearOrders-label` 
     additional tools for solving linearly ranking problems.
:ref:`weakOrders-label` 
     additional tools for solving ranking by choosing problems.



.. toctree::
   :maxdepth: 2

.. _digraphs-label:

digraphs module
---------------

.. automodule:: digraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Introduction-label`

.. _graphs-label:

graphs module
---------------

A tutorial with coding examples is available here: :ref:`Tutorial-label`

.. automodule:: graphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Introduction-label`

.. _perfTabs-label:

perfTabs module
---------------

.. automodule:: perfTabs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Introduction-label`

.. _outrankingDigraphs-label:

outrankingDigraphs module
-------------------------

.. automodule:: outrankingDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Introduction-label`

.. _votingDigraphs-label:

votingDigraphs module
---------------------

.. automodule:: votingDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Introduction-label`

.. _sortingDigraphs-label:

sortingDigraphs module
----------------------

.. automodule:: sortingDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Introduction-label`

.. _linearOrders-label:

linearOrders module
-------------------

.. automodule:: linearOrders
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Introduction-label`

.. _weakOrders-label:

weakOrders module
-------------------------------

.. automodule:: weakOrders
   :member-order: alphabetical
   :no-inherited-members:
   :members:


Back to the :ref:`Introduction-label`

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
* :ref:`Tutorial-label`


