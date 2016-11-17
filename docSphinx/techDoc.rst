Technical Reference of the Digraph3 modules
===========================================
:Author: Raymond Bisdorff, University of Luxembourg FSTC/CSC
:Version: Revision: Python 3.5
:Copyright: `R. Bisdorff <http://leopold-loewenheim.uni.lu/bisdorff/>`_ 2013-2016

.. _Technical-label:

Installation
------------

**Dowloading the Digraph3 ressources**

Three download options are given:

1. Either (easiest under Linux or Mac OS-X), by using a git client::

     ..$ git clone https://github.com/rbisdorff/Digraph3 

2. or a subversion client::

     ..$ svn co http://leopold-loewenheim.uni.lu/svn/repos/Digraph3 

3. Or, with a browser access, download and extract the latest distribution tar.gz archive from this page::

     http://leopold-loewenheim.uni.lu/Digraph3/dist/

On Linux or Mac OS, ..$ cd to the extracted <Digraph3> directory::

     ../Digraph3$ make install

installs (with sudo !!) the digraphs module in the current running python environment. Pythhon 3.5 (or later) environment is recommended::

     ../Digraph3$ make tests

runs a nose test suite in the ./test directory (python3 nose package required  ..$ pip3 install nose )::

     ../Digraph3$ make verboseTests

runs a verbose (with stdout not captured) nose test suite::

     ../Digraph3$ make pTests

runs the nose test suite in multiple processing mode when the GNU `parallel <https://www.gnu.org/software/parallel/>`_ shell tool is installed and multiple cores are detected.

To be fully functional, the Digraph3 resources mainly need the `graphviz <http://graphviz.org>`_ tools and the `R statistics resources <http://www.r-project.org>`_ to be installed. When exploring digraph isomorphisms, the `nauty <http://www.cs.sunysb.edu/~algorith/implement/nauty/implement.shtml>`_ isomorphism testing program is required. Two specific criteria and actions clustering methods of the `OutrankingDigraph <techDoc.html#outrankingDigraphs.OutrankingDigraph>`_ class furthermore require the `calmat <http://leopold-loewenheim.uni.lu/svn/repos/Calmat/>`_ matrix computing resource to be installed. 

**Organisation of the Digraph3 python3 source code**

The Digraph3 source code is split into several interdependent modules of which the ``digraphs`` module is the master module.

* :ref:`digraphs-label`  
     Main part of the Digraph3 source code with the root `Digraph <techDoc.html#digraphs.Digraph>`_ class;
* :ref:`randomDigraphs-label` 
     Various implemented random digraph models.
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
     Additional random number generators, not available in the standard python library.
* :ref:`randomPerfTabs-label` 
     Various implemented random performance tableau models.
* :ref:`sparseOutrankingDigraphs-label` 
     Sparse implementation design for large outranking digraphs (order > 1000).

Developping the Rubis decision support methodology is an ongoing research project of Raymond Bisdorff <http://leopold-loewenheim.uni.lu/bisdorff/>, University of Luxembourg.

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

.. _randomPerfTabs-label:
      
randomPerfTabs module
----------------------

A tutorial with coding examples is available here: :ref:`RandomPerformaceTableau-Tutorial-label`

.. automodule:: randomPerfTabs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _outrankingDigraphs-label:

outrankingDigraphs module
-------------------------

A tutorial with coding examples is available here: :ref:`OutrankingDigraphs-Tutorial-label`

.. automodule:: outrankingDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _sparseOutrankingDigraphs-label:

sparseOutrankingDigraphs module
--------------------------------

.. automodule:: sparseOutrankingDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _sortingDigraphs-label:

sortingDigraphs module
----------------------

.. automodule:: sortingDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _votingDigraphs-label:

votingDigraphs module
---------------------

A tutorial with coding examples is available here: :ref:`VotingDigraphs-label`

.. automodule:: votingDigraphs
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _linearOrders-label:

linearOrders module
-------------------

A tutorial with coding examples is available here: :ref:`LinearVoting-Tutorial-label`

.. automodule:: linearOrders
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _weakOrders-label:

weakOrders module
------------------

.. automodule:: weakOrders
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _randomNumbers-label:

randomNumbers module
----------------------

.. automodule:: randomNumbers
   :member-order: alphabetical
   :no-inherited-members:
   :members:

Back to the :ref:`Technical-label`

.. _randomDigraphs-label:

randomDigraphs module
----------------------

.. automodule:: randomDigraphs
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


