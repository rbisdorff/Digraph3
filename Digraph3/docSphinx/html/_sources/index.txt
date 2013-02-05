.. graphs documentation master file, created by
   sphinx-quickstart on Mon Jan  2 22:15:21 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Technical Documentation of the Digraph resources!
=================================================
:Author: Raymond Bisdorff, University of Luxembourg FSTC/CSC
:Version: $Revision: 1.2 $
:Copyright: R. Bisdorff 2012

.. _Introduction-label:

Introduction
------------

This Technical Manual describes the Python implementation ($Revision: 1.2 $) of generic resources for computing kernels and other qualified choices in bipolar-valued outranking digraphs. This computing ressource is useful in the filed of algorithmic decision sciences problems

Developping the Rubis decision support methodology is an ongoing research project of Raymond Bisdorff <http://charles-sanders-peirce.uni.lu/bisdorff/>, University of Luxembourg.

The Python following modules are based on the optimized in-built ``set`` class and therefore require at least  version 2.4.0 of Python.

The basic idea of these Python modules is to make easy python interactive sessions or write short Python scripts for computing all kind of results from a bipolar valued outranking digraph. These include such features as maximal independent or irredundant choices, maximal dominant or absorbent choices etc. 

The Python development of these computing ressources offers the advantage of an easy to write and maintain OOP source code as expected from a performing scripting language without loosing on efficiency in execution times compared to compiled languages such as C++ or Java. 

The Digraph source code is split into five interdependant modules, where the ``digraphs`` module is the master source.

:ref:`digraphs-label`
     main part of the source code with the top ``Digraph`` and the old version (-Rev:1.630) ``BipolarOutrankingDigraph`` classes; 
:ref:`outrankingDigraphs-label`
     New version ``BipolarOutrankingDigraph`` classes; 
:ref:`perfTabs-label` 
     everything needed for handling Rubis Performance Tableaux;
:ref:`votingDigraphs-label` 
     additional classes and methods for computing with election results;
:ref:`sortingDigraphs-label`
     additional tools for solving sorting problems;
:ref:`linearOrders-label` 
     additional tools for solving ranking problems.


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

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`



