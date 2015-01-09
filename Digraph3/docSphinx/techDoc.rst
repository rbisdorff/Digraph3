Technical Reference of the Digraph3 modules
===========================================
:Author: Raymond Bisdorff, University of Luxembourg FSTC/CSC
:Version: Revision: Python 3.4
:Copyright: R. Bisdorff 2013-2014

.. _Technical-label:

Introduction
------------

**Dowloading the Digraph3 ressources**

Two downlaod options are given:
    
1. Either (easiest under Linux or Mac OS-X), by using a subversion client::
..$svn co http://leopold-loewenheim.uni.lu/svn/repos/Digraph3
       
2. Or, download and extract the latest distribution tar.gz archive::
http://leopold-loewenheim.uni.lu/svn/repos/Digraph3/dist/digraphs-Python3-xxx.tar.gz 

Developping the Rubis decision support methodology is an ongoing research project of Raymond Bisdorff <http://charles-sanders-peirce.uni.lu/bisdorff/>, University of Luxembourg.

To be fully functional, the Digraph3 resources mainly need the `graphviz <http://graphviz.org>`_ tools and the `R statistics resources <http://www.r-project.org>`_ to be installed. When exploring digraph isomorphisms, the `nauty <http://www.cs.sunysb.edu/~algorith/implement/nauty/implement.shtml>`_ isomorphism testing program is required. two specific criteria and actions clustering methods of the Digraph class furthermore require the `calmat <http://leopold-loewenheim.uni.lu/svn/repos/Calmat/>`_ matrix computing resource to be installed. 

**Organisation of the Digraph3 python3 source code**

The Digraph3 source code is split into several interdependent modules of which the ``digraphs`` module is the master module.

* :ref:`digraphs-label`  
     Main part of the Digraph3 source code with the root `Digraph <techDoc.html#digraphs.Digraph>`_ class;
* :ref:`graphs-label`
     Specialization for undirected graphs with the root `Graph <techDoc.html#graphs.Graph>`_ class and a brigde to the ``digraphs`` module resources;
* :ref:`outrankingDigraphs-label`
     New Python3 specific root `OutrankingDigraph <techDoc.html#outrankingDigraphs.OutrankingDigraph>`_ class and specializations; 
* :ref:`perfTabs-label` 
     Everything needed for handling Multiple Criteria Decision Aid performance tableaux with root `PerformaceTableau <techDoc.html#perfTabs.PerformanceTableau>`_ class;
* :ref:`votingDigraphs-label` 
     Additional classes and methods for computing election results with main `LinearVotingProfile <techDoc.html#votingDigraphs.LinearVotingProfile>`_ class;
* :ref:`sortingDigraphs-label`
     Additional tools for solving sorting problems with the root `SortingDigraph <techDoc.html#sortingDigraphs.SortingDigraph>`_ class;
* :ref:`linearOrders-label` 
     Additional tools for solving linearly ranking problems with the root `LinearOrder <techDoc.html#linearOrders.LinearOrder>`_ class;
* :ref:`weakOrders-label` 
     Additional tools for solving ranking by choosing problems with root `WeakOrder <techDoc.html#weakOrders.WeakOrder>`_ class.
* :ref:`randomNumbers-label` 
     Various home brewed random number generators like discrete and extended triangular.
* :ref:`randomDigraphs-label` 
     Various implemented random digraph models.

.. toctree::
   :maxdepth: 2

.. _digraphs-label:

digraphs module
---------------

A tutorial with coding examples is available here: :ref:`Digraphs-Tutorial-label`

.. automodule:: digraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _graphs-label:

graphs module
---------------

A tutorial with coding examples is available here: :ref:`Graphs-Tutorial-label`

.. automodule:: graphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _perfTabs-label:

perfTabs module
---------------

.. automodule:: perfTabs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

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
-----------------

.. automodule:: weakOrders
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Introduction-label`

.. _randomDigraphs-label:

randomDigraphs module
---------------------

.. automodule:: randomDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Introduction-label`

.. _randomNumbers-label:

randomNumbers module
--------------------

.. automodule:: randomNumbers
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Tutorials
---------

* `Tutorial <tutorial.html>`_


